import os
import datetime
import requests
import smtplib
import time

# Get the NASA API key and email from environment variables
NASA_API_KEY = os.getenv("NASA_API_KEY")
MY_GMAIL = os.getenv("MY_GMAIL")

rover_list = ["Curiosity", "Opportunity", "Spirit"]
date = input("Date yyyy-mm-dd: ")
rover = input("Rover: ")
camera = {
    "Front Hazard Avoidance Camera": "FHAZ",
    "Rear Hazard Avoidance Camera": "RHAZ",
    "Navigation Camera": "NAVCAM"
}

response = requests.get(url=f"https://api.nasa.gov/mars-photos/api/v1/rovers/{rover}/photos?earth_date={date}&api_key={NASA_API_KEY}")
print(f"https://api.nasa.gov/mars-photos/api/v1/rovers/{rover}/photos?earth_date={date}&api_key={NASA_API_KEY}")

response.raise_for_status()

query_data = response.json()

panoramic_camera = []
front_hazard_camera = []
rear_hazard_camera = []

# Iterate through each photo and categorize by camera type
for photo in query_data["photos"]:
    camera_name = photo["camera"]["name"]
    img_src = photo["img_src"]
    
    if camera_name == "PANCAM":
        panoramic_camera.append(img_src)
    elif camera_name == "FHAZ":
        front_hazard_camera.append(img_src)
    elif camera_name == "RHAZ":
        rear_hazard_camera.append(img_src)

# Print the lists
print("Panoramic Camera:", panoramic_camera)
print("Front Hazard Camera:", front_hazard_camera)
print("Rear Hazard Camera:", rear_hazard_camera)
