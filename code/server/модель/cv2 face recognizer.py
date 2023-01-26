import cv2
import wx
import numpy as np

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # frame[0:240, 0:640] = frame[240:480, 0:640]
    cv2.imshow('camera', frame)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()


# img = cv2.imread('test2.jpg', -1)
# # img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
#
# cv2.imshow('hot', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# print(img.shape)


# class MyFrame(wx.Frame):
#     def __init__(self):
#         wx.Frame.__init__(self, None, -1, "Video Test")
#         self.cap = cv2.VideoCapture(0)
#         self.Show()
#         self.OnTimer()
#
#
#     def OnTimer(self):
#         cap = cv2.VideoCapture(0)
#         face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#
#         while True:
#             ret, frame = cap.read()
#             frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#             faces = face_cascade.detectMultiScale(gray, 1.1, 5)
#             for (x, y, w, h) in faces:
#                 cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
#
#             # frame[0:240, 0:640] = frame[240:480, 0:640]
#             wxImg = wx.ImageFromBuffer(frame.shape[1], frame.shape[0], frame)
#             self.Refresh()
#             self.Update()
#
# app = wx.App()
# frame = MyFrame()
# app.MainLoop()
