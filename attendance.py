import cv2
import face_recognition
import os
import numpy as np
from datetime import datetime
import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase
import csv
from firebase import firebase

path = 'E:\pythonProject\opencv\Images'         #Change the path
images = []
classNames = []
myList = os.listdir(path)
len = len(myList)
print(myList)
print(len)

emailfrom = "mortyproject123@gmail.com"
emailto = "mortyproject123@gmail.com"
fileToSend = "E:\pythonProject\opencv\list_of_student.csv"
username = "mortyproject123@gmail.com"
password = "mortyproject"

msg = MIMEMultipart()
msg["From"] = emailfrom
msg["To"] = emailto
msg["Subject"] = "Attendance List"
msg.preamble = "Attendance List"

ctype, encoding = mimetypes.guess_type(fileToSend)
if ctype is None or encoding is not None:
    ctype = "application/octet-stream"

maintype, subtype = ctype.split("/", 1)

fp = open(fileToSend, "rb")
attachment = MIMEBase(maintype, subtype)
attachment.set_payload(fp.read())
fp.close()
encoders.encode_base64(attachment)

attachment.add_header("Content-Disposition", "attachment", filename=fileToSend)
msg.attach(attachment)

server = smtplib.SMTP("smtp.gmail.com:587")
server.starttls()
server.login(username, password)

FBconnection = firebase.FirebaseApplication('https://pythontest-68309.firebaseio.com/', None)

for cls in myList:
    current_img = cv2.imread(f'{path}/{cls}')
    images.append(current_img)
    classNames.append(os.path.splitext(cls)[0])

print(classNames)


def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


def markStudent(name):
    with open('list_of_student.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        reader = csv.reader(f, delimiter=",")
        data = [l for l in reader]
        row_count = sum(1 for row in reader)
        # print(row_count)
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M%S')
            f.writelines(f'\n{name},{dtString}')
            data_to_upload = {
                "Name": name
            }
            result = FBconnection.post('/MyTestData', name)
        if row_count == (len - 1):
            server.sendmail(emailfrom, emailto, msg.as_string())
            server.quit()


encodeListKnown = findEncodings(images)
print("Encoding Completed")

cap = cv2.VideoCapture(0)
while True:
    success, img = cap.read()
    img_small = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    img_small = cv2.cvtColor(img_small, cv2.COLOR_BGR2RGB)
    face_in_frame = face_recognition.face_locations(img_small)
    encode_frame = face_recognition.face_encodings(img_small, face_in_frame)
    for encodeFace, facLoc in zip(encode_frame, face_in_frame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        face_distance = face_recognition.face_distance(encodeListKnown, encodeFace)
        print(face_distance)
        matchIndex = np.argmin(face_distance)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            print(name)
            y1, x2, y2, x1 = facLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, (y2 - 35)), (x2, y2), (0, 255, 0))
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            markStudent(name)

    cv2.imshow('WEbCam', img)
    cv2.waitKey(1)
