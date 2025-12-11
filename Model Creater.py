#Model creator - TensorFlow

# Import libraries

import random
import csv
import tensorflow as tf
import cv2


# Variables

IMG_DIR = "data" # Data structure is raw images and CSV in one folder called data for simplicity
CSV_PATH = "data"

DATA_SPLIT = 20 # Percentage of data used for validation



# Open CSV file

with open(CSV_PATH, "r") as file:

  telemetry = csv.reader(file)
  print(CSV_PATH, "opened")


  # Loop - feed image and telemetry into TensorFlow model for each csv line (model.fit)

  next(telemetry)      # Skip header row
  
  for row in telemetry:
    
    imageName = row[1]
    steering = float(row[2])
    throttle = float(row[3])

    
    image = cv2.imread(imageName) # image = cv2.imread(imageName, 0) for greyscale

    
  




# Finish modelling it and put validation data back into model to test accuracy



# Convert the model to TFLite (model.tflite) and save as a file
