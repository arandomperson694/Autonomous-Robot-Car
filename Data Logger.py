# Autonomous Robot Car Data Logger

import cv2
import csv
import pygame
import os
import time
from picarx import Picarx


IMG_SIZE = 200Sorr
FPS = 15
LOG_DIR = "data"
IMG_DIR = os.path.join(LOG_DIR, "Images")
CSV_PATH = os.path.join(LOG_DIR, "ThrottleAndSteering.CSV")


MAX_STEER = 30.0
MAX_SPEED = 50.0 # (0-100)

STEER_AXIS = 0
THROTTLE_AXIS = 1 # Both using left joystick
STOP_BUTTON = 0 #Mapped to A key on Xbox



def get_controller_values(joystick):

    pygame.event.pump()

    rawSteer = joystick.get_axis(STEER_AXIS)
    rawThrottle = -(joystick.get_axis(THROTTLE_AXIS))So

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

    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, IMG_SIZE)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, IMG_SIZE)
    cam.set(cv2.CAP_PROP_FPS, FPS)

    pygame.init()
    pygame.joystick.init()

    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(joystick.get_name(), "connected")
    

    try:
        
        while True:
            
            pygame.event.pump()
            if joystick.get_button(STOP_BUTTON):
                print("Stopping drive")
                break


            steering, throttle = get_controller_values(joystick)

            px.set_dir_servo_angle(steering)
            px.forward(throttle)

            ret, frame = cam.read()
            if not ret:
                time.sleep(0.01)
                continue

            frame_resized = cv2.resize(frame, (IMG_SIZE, IMG_SIZE))

            timeStamp = time.time()

            img_name = f"img_{int(timeStamp * 1000)}.png"
            img_path = os.path.join(IMG_DIR, img_name)
            cv2.imwrite(img_path, frame_resized)

            csvWriter.writerow([timeStamp, img_name, steering, throttle])
            csvFile.flush()


            time.sleep(0.05)


    finally:

        px.forward(0)
        cam.release()
        csvFile.close()
        pygame.quit()
        print("Shutdown complete. Data saved to", CSV_PATH)


if __name__ == "__main__":
    main()
                                       
