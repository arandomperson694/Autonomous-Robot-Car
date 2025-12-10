# Autonomous Robot Car Data Logger

import cv2     #OpenCV
import csv     #File writing
import pygame     #Bluetooth controller
import os     #Directories
import time     #Time
from picarx import Picarx     #SunFounder control


IMG_SIZE = 200     #Resolution
FPS = 15     
LOG_DIR = "data"     # Name of file where we store data
IMG_DIR = os.path.join(LOG_DIR, "Images")
CSV_PATH = os.path.join(LOG_DIR, "ThrottleAndSteering.CSV")


MAX_STEER = 30.0     # 30 degrees
MAX_SPEED = 50.0     # (0-100)

STEER_AXIS = 3     # Right joystick left and right
THROTTLE_AXIS = 1     #  Left joystick up and down
STOP_BUTTON = 0     #Mapped to A key on Xbox



def get_controller_values(joystick):

    pygame.event.pump()     # Get controller

    rawSteer = joystick.get_axis(STEER_AXIS)     # The left stick x axis
    rawThrottle = -(joystick.get_axis(THROTTLE_AXIS))     # Left stick y axis

    steering = float(rawSteer * MAX_STEER)
    throttle = float(rawThrottle * MAX_SPEED)

    return steering, throttle


def main():

    os.makedirs(IMG_DIR, exist_ok=True)
    writeHeader = not os.path.exists(CSV_PATH) # Write header if not already written

    csvFile = open(CSV_PATH, "a", newline="")
    csvWriter = csv.writer(csvFile)
    
    if writeHeader:
        csvWriter.writerow(["Timestamp", "Image Name", "Steering", "Throttle"])


    px = Picarx()

    cam = cv2.VideoCapture(0)     # Use the first camera
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, IMG_SIZE)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, IMG_SIZE)
    cam.set(cv2.CAP_PROP_FPS, FPS)

    pygame.init()
    pygame.joystick.init()     # Initialise the controller

    joystick = pygame.joystick.Joystick(0)     # Use the first controller
    joystick.init()
    print(joystick.get_name(), "connected")
    

    try:
        
        while True:
            
            pygame.event.pump()
            if joystick.get_button(STOP_BUTTON):
                print("Stopping drive")
                break


            steering, throttle = get_controller_values(joystick)     #Get input

            px.set_dir_servo_angle(steering)     #Steer the car
            px.forward(throttle)     # Drive the car

            ret, frame = cam.read()     # Take a picture
            if not ret:
                time.sleep(0.01)
                continue

            frame_resized = cv2.resize(frame, (IMG_SIZE, IMG_SIZE))

            timeStamp = time.time()     # Get current time

            img_name = f"img_{int(timeStamp * 1000)}.png"
            img_path = os.path.join(IMG_DIR, img_name)
            cv2.imwrite(img_path, frame_resized)     # Save the photo

            csvWriter.writerow([timeStamp, img_name, steering, throttle])    # Save the telemetry
            csvFile.flush()

            #time.sleep(1/FPS)    FPS already specified, only use if necessary



    finally:

        px.forward(0)
        cam.release()
        csvFile.close()
        pygame.quit()
        print("Shutdown complete. Data saved to", CSV_PATH)


if __name__ == "__main__":
    main()
                                       
