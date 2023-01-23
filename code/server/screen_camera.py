import wx
import cv2
import numpy as np
from keras.models import load_model
from PIL import Image



class Main(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Mood Predictor')
        self.panel = wx.Panel(self)

        # Create a button to take a photo
        self.photo_button = wx.Button(self.panel, label='Take Photo')
        self.photo_button.Bind(wx.EVT_BUTTON, self.on_photo)

        # Create a label to display the predicted mood
        self.mood_label = wx.StaticText(self.panel, label='Mood:')

        # Create a layout for the widgets
        layout = wx.BoxSizer(wx.VERTICAL)
        layout.Add(self.photo_button, 0, wx.ALL | wx.CENTER, 10)
        layout.Add(self.mood_label, 0, wx.ALL | wx.CENTER, 10)
        self.panel.SetSizer(layout)

        self.Show()

    def on_photo(self, event):
        # Open the webcam
        cap = cv2.VideoCapture(0)

        # Take a photo
        ret, frame = cap.read()

        # Close the webcam
        cap.release()

        # Pre-process the image
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.resize(frame, (48, 48))
        print(frame.shape)
        # frame = frame.reshape(1, 48, 48, 1)

        # Convert image to wx.Image
        img = Image.fromarray(frame)
        wx_image = wx.Image(img.width, img.height)
        wx_image.SetData(img.convert('RGB').tobytes())

        # Create a StaticBitmap to display the image
        wx_image = wx_image.Rescale(192, 192)
        self.picture = wx.StaticBitmap(self.panel, bitmap=wx.Bitmap(wx_image))

        # Predict the mood
        frame = frame.reshape(1, 48, 48, 1) #----

        prediction = model.predict(frame)
        predicted_label = np.argmax(prediction, axis=1)


        # Get the label with the highest probability
        mood = emotion_labels[predicted_label[0]]

        # Update the mood label with the predicted mood
        print(mood)
        self.mood_label.SetLabel(f'Mood: {mood}')


if __name__ == '__main__':

    model = load_model('model2.h5')
    emotion_labels = {
        0: 'Angry',
        1: 'Disgust',
        2: 'Fear',
        3: 'Happy',
        4: 'Sad',
        5: 'Surprise',
        6: 'Neutral'
    }
    app = wx.App()
    frame = Main()
    print(type(frame))
    app.MainLoop()
