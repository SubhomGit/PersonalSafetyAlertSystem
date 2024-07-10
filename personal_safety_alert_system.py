from email import encoders
from email.mime.base import MIMEBase
import cv2
import numpy as np
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import os

# Set up the webcam
cap = cv2.VideoCapture(0)

# Load the pre-trained model
protoFile = "pose_deploy_linevec.prototxt"
weightsFile = "pose_iter_440000.caffemodel"
net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)

alert_sent = False
log_file = "activity_log.txt"

def send_alert(image_path, recipient_email):
    from_email = "gokuben04@gmail.com"
    from_password = "kfht smnu nycy ajoi"
    subject = "Alert: Unusual Activity Detected"
    body = "An unusual activity has been detected. Please check the attached image."

    msg = MIMEMultipart()
    msg.attach(MIMEText(body, 'plain'))
    msg['From'] = from_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    with open(image_path, 'rb') as f:
        mime = MIMEBase('image', 'png', filename=image_path)
        mime.add_header('Content-Disposition', 'attachment', filename=image_path)
        mime.add_header('X-Attachment-Id', '0')
        mime.add_header('Content-ID', '<0>')
        mime.set_payload(f.read())
        encoders.encode_base64(mime)
        msg.attach(mime)

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(from_email, from_password)
    server.sendmail(from_email, recipient_email, msg.as_string())
    server.quit()

def detect_fall(points):
    if points:
        # Implement your fall detection logic here
        # For example, check if head point y-coordinate is below a certain threshold
        head_point = points[0]
        if head_point and head_point[1] > 400:  # example threshold
            return True
    return False

def process_frame(frame, net):
    inWidth = 368
    inHeight = 368
    inpBlob = cv2.dnn.blobFromImage(frame, 1.0 / 255, (inWidth, inHeight),
                                    (0, 0, 0), swapRB=False, crop=False)
    net.setInput(inpBlob)
    output = net.forward()

    H = output.shape[2]
    W = output.shape[3]
    
    points = []
    for i in range(15):
        probMap = output[0, i, :, :]
        minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)
        
        x = (frame.shape[1] * point[0]) / W
        y = (frame.shape[0] * point[1]) / H
        
        if prob > 0.1 :
            points.append((int(x), int(y)))
        else :
            points.append(None)

    return points

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    points = process_frame(frame, net)
    fall_detected = detect_fall(points)
    
    if fall_detected and not alert_sent:
        image_path = "alert_image.png"
        cv2.imwrite(image_path, frame)
        send_alert(image_path, "subhoms300@gmail.com")
        alert_sent = True
        with open(log_file, "a") as log:
            log.write(f"{datetime.now()}: Fall detected\n")

    for point in points:
        if point:
            cv2.circle(frame, point, 5, (0, 255, 255), -1, cv2.LINE_AA)
    
    cv2.imshow('Frame', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
