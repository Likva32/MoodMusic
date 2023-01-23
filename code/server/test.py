#!/usr/bin/env python
# coding: utf-8

# In[16]:


from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ModelCheckpoint
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# ### Load the FER2013 dataset
# 

# In[2]:


data = pd.read_csv("fer2013.csv")



# ### Split the data into training, validation, and test sets

# In[3]:


train_data = data[data.Usage == "Training"]
validation_data = data[data.Usage == "PublicTest"]
test_data = data[data.Usage == "PrivateTest"]


# ### Convert the data to numpy arrays

# In[4]:


x_train = np.array([np.fromstring(image, np.uint8, sep=' ') for image in train_data.pixels])
y_train = np.array(train_data.emotion)
x_val = np.array([np.fromstring(image, np.uint8, sep=' ') for image in validation_data.pixels])
y_val = np.array(validation_data.emotion)
x_test = np.array([np.fromstring(image, np.uint8, sep=' ') for image in test_data.pixels])
y_test = np.array(test_data.emotion)


# ### Reshape the data to 48x48 images

# In[5]:


x_train = x_train.reshape(x_train.shape[0], 48, 48, 1)
x_val = x_val.reshape(x_val.shape[0], 48, 48, 1)
x_test = x_test.reshape(x_test.shape[0], 48, 48, 1)


# ### Normalize the data

# In[7]:


x_train = x_train.astype('float32') / 255
x_val = x_val.astype('float32') / 255
x_test = x_test.astype('float32') / 255


# ### One-hot encode the labels

# In[8]:


num_classes = 7
y_train = np_utils.to_categorical(y_train, num_classes)
y_val = np_utils.to_categorical(y_val, num_classes)
y_test = np_utils.to_categorical(y_test, num_classes)


# ### Data augmentation

# In[11]:


data_gen = ImageDataGenerator(rotation_range=10, zoom_range=0.1, width_shift_range=0.1,
                              height_shift_range=0.1, horizontal_flip=True, fill_mode='nearest')
data_gen.fit(x_train)


# ### Define the model

# In[12]:


# Define the model
model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(48, 48, 1)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(num_classes, activation='softmax'))


# ### Compile the model

# In[13]:


model.compile(loss='categorical_crossentropy', optimizer=Adam(), metrics=['accuracy'])


# ### Define a callback to save the best model

# In[14]:


checkpointer = ModelCheckpoint(filepath='model.h5', save_best_only=True)


# ### Train the model

# In[15]:


model.fit_generator(data_gen.flow(x_train, y_train, batch_size=32), steps_per_epoch=len(x_train) / 32,
                    epochs=2, validation_data=(x_val, y_val), callbacks=[checkpointer])


# ### Evaluate the model on the test set

# In[17]:


score = model.evaluate(x_test, y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])


# ### Select a few images from the test set

# In[45]:


num_images = 10
random_indices = np.random.randint(x_test.shape[0], size=num_images)
test_images = x_test[random_indices]
test_labels = y_test[random_indices]


# ### Use the model to predict the emotions for the selected images

# In[46]:


predictions = model.predict(test_images)
predicted_labels = np.argmax(predictions, axis=1)


# ### Display the images and the predicted emotions

# In[47]:


emotion_labels = {
    0: 'Angry',
    1: 'Disgust',
    2: 'Fear',
    3: 'Happy',
    4: 'Sad',
    5: 'Surprise',
    6: 'Neutral'
}

fig, axes = plt.subplots(1, num_images, figsize=(20, 20))
for i in range(num_images):
    ax = axes[i]
    ax.imshow(test_images[i, :, :, 0], cmap='gray')
    ax.axis('off')
    ax.set_title(emotion_labels[predicted_labels[i]])
plt.show()


# In[ ]:




