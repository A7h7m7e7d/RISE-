import cv2
import math
import cvzone
import pywhatkit as kit
import datetime
import requests
import pyautogui
import time
from ultralytics import YOLO

# Function to get location from IP-API
def get_location():
    response = requests.get('http://ip-api.com/json/')
    if response.status_code == 200:
        data = response.json()
        return f"{data['city']}, {data['regionName']}, {data['country']}"
    else:
        return "Location not found"






def centerize_text(image, text, font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=1, font_thickness=2):
    # Read the image
    

    # Get the size of the image
    height, width, _ = image.shape

    # Get the size of the text
    (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, font_thickness)

    # Calculate the position to center the text
    x = int((width - text_width) / 2)
    y = int((height + text_height) / 2)

    # Define the text position and color
    text_position = (x, y)
    text_color = (255, 255, 255)  # White color in BGR

    # Add text to the image
    cv2.putText(image, text, text_position, font, font_scale, text_color, font_thickness)

    # Save the output image
    #cv2.imwrite(output_path, image)

    # Display the image (optional)
    cv2.imshow('Centerized Text Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage
image_path = 'input_image.jpg'
output_path = 'output_image.jpg'
text_to_centerize = 'Centerized Text'









# Load the YOLO model
model = YOLO('../Yolo-Weights/yolov8l.pt')

Path = input("what is the name of the image :")
img = cv2.imread('Images/'+Path+'.png')


# Perform object detection on the image
results = model(img)

# Initialize variables for counting cars and calculating efficiency
car_count_acc = 0
car_count = 0

# Class ID for the "car" class
car_class_id = 2

for r in results:
    boxes = r.boxes

    for box in boxes:
        cls = int(box.cls[0])
        if cls == car_class_id:
            # Bounding Box calculations
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            cvzone.cornerRect(img, (x1, y1, x2-x1, y2-y1))
            # Confidence calculation
            conf = math.ceil((box.conf[0] * 100)) / 100

        # Class Name
        cls = int(box.cls[0])
        if cls == car_class_id:
            if conf < 0.77:
                car_count_acc += 1
            else:
                car_count += 1

# Print the car count and efficiency
print(f"Number of undamaged cars detected: {car_count}")
print(f"Number of cars detected acc: {car_count_acc}")

# Get current location
current_location = get_location()

# Send WhatsApp message if an accident is detected
if car_count_acc != 0:
    print("there is an accident in the street")
    img2 = cv2.resize(img, (0, 0), fx=4, fy=4)

    # Set the text you want to add
    text = "This is an accident"

    # Font settings
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 2
    color = (0, 0, 255)  # Red color
    thickness = 4

    # Calculate the text size
    (text_width, text_height), _ = cv2.getTextSize(text, font, fontScale, thickness)

    # Calculate the center of the image
    center_x = img2.shape[1] // 2 - text_width // 2
    center_y = img2.shape[0] // 2 + text_height // 2

    # Using cv2.putText() method to add text at the center
    cv2.putText(img2, text, (center_x,center_y), font, thickness, color, thickness)


    # Display the image
    centerize_text(img2, text)
    

    now = datetime.datetime.now()
    kit.sendwhatmsg('+20 102 809 5889', f'There is an accident in the street. My current location: {current_location}', now.hour, now.minute + 2)

    # Wait for the browser to open and the message to be typed
    time.sleep(120)  # Adjust this delay as needed

    # Press 'Enter' to send the message
    pyautogui.press('enter')
else:
    img2 = cv2.resize(img, (0, 0), fx=4, fy=4)

    # Set the text you want to add
    text = "safe "

    # Font settings
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 2
    color = (0, 255, 0)  # Red color
    thickness = 4

    # Calculate the text size
    (text_width, text_height), _ = cv2.getTextSize(text, font, fontScale, thickness)

    # Calculate the center of the image
    center_x = img2.shape[1] // 2 - text_width // 2
    center_y = img2.shape[0] // 2 + text_height // 2

    # Using cv2.putText() method to add text at the center

    # Display the image
    centerize_text(img, text)
resized_image = cv2.resize(img, (400,300))
# Display the image with bounding boxes (optional)
cv2.imshow("the windows", )

cv2.waitKey(0)
cv2.destroyAllWindows()
