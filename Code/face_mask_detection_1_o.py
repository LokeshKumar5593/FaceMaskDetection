# -*- coding: utf-8 -*-
"""FACE MASK DETECTION 1.O

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1J6V2WwvUKjr7nmxW_-EcSMiK-AIU_Fes
"""

import os
import numpy as np
import random
from tensorflow.keras.layers import Dense,Dropout,Conv2D,MaxPooling2D,Flatten
from tensorflow.keras.models import Sequential
import cv2
import matplotlib.pyplot as plt

pip install tensorflow

from google.colab import drive
drive.mount('/content/drive')

path='/content/drive/My Drive/Dataset/with_mask'
files=[]
for r,d,f in os.walk(path):
  for file in f:
    files.append(os.path.join(r, file))

path='/content/drive/My Drive/Dataset/without_mask'
for r,d,f in os.walk(path):
  for file in f:
    files.append(os.path.join(r, file))

print(len(files))

y=[1]*5521+[0]*5521
x=[]
for i in range(len(files)):
  img=cv2.imread(files[i])
  res=cv2.resize(img,dsize=(64,64),interpolation=cv2.INTER_CUBIC)
  image=np.array(res)/255
  x.append([image,y[i]])
x=np.array(x)

np.random.shuffle(x)
np.random.shuffle(x)
x,y=np.array(list(map(lambda x: x[0],x))),np.array(list(map(lambda x: x[1],x)))
x.shape

from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.3)

x_train.shape,x_test.shape

y_train.shape,y_test.shape

index=np.random.randint(11042)
plt.imshow(x[index])
y[index]

model = Sequential()
model.add(Conv2D(32,(3,3),activation='relu',input_shape=(64,64,3)))
model.add(MaxPooling2D())
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D())
model.add(Dropout(0.2))
model.add(Flatten())
model.add(Dense(15000,activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(7000,activation='relu'))
model.add(Dense(2000,activation='relu'))
model.add(Dense(300,activation='relu'))

model.add(Dense(1,activation='sigmoid'))

model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])

from tensorflow.keras.callbacks import TensorBoard
import time
tb=TensorBoard(log_dir='logs/new4')

his=model.fit(x_train,y_train,validation_data=(x_test,y_test),epochs=5,callbacks=[tb])

model.evaluate(x_test,y_test)

index=random.randrange(9211,11042)
plt.imshow(x[index].reshape(64,64,3))
res=model.predict(np.array([x[index]]))
if res[0][0]>0.5:
  print('with_mask')
else:
  print('without_mask')
res[0][0]

model.summary()

model.save('Face_Mask_Prediction_1.h5')

model_json=model.to_json()
with open("model.json","w") as file:
  file.write(model_json)

model.save_weights("weights1.h5")

from keras.models import load_model

new_model=load_model('Face_Mask_Prediction_1.h5')
new_model.evaluate(x_test,y_test,verbose=2)

import cv2
import numpy as np
import matplotlib.pyplot as plt
img = cv2.imread('/content/drive/MyDrive/Dataset/without_mask/1.jpg')
img = cv2.resize(img, (64,64))
img = np.reshape(img, (1,64,64,3))
print(img.shape)
print(new_model.predict(img))

!pip install mtcnn

from mtcnn.mtcnn import MTCNN
detector = MTCNN()

labels={0:'MASK',1:'NO MASK', 2:'NO FACE FOUND'}
color={0:(0,255,0),1:(255,0, 0)}

test_images = ['/content/loki_with_out_mask.jpeg','/content/with_mask and without _mask.jpeg','/content/WithOut_mask.jpeg']

def show_images(images):
    n: int = len(images)
    f = plt.figure(figsize=(128, 128))
    for i in range(n):
        # Debug, plot figure
        f.add_subplot(1, n, i + 1)
        plt.imshow(images[i])

    plt.show(block=True)

output_images = []
for file in test_images:
  img = cv2.imread(file)
  img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
  faces = detector.detect_faces(img_rgb)

  index = 1
  try:
      for face in faces:
          (x,y,w,h) = face['box']
          face_img = img_rgb[y:y+h, x:x+w]
          # print(face_img.shape)
          img_resized = cv2.resize(face_img, (64,64))
          img_resized = np.reshape(img_resized, (1,64,64,3))

          result = int(model.predict(img_resized)[0][0])
      
          cv2.rectangle(img,(x,y),(x+w,y+h),color[result],2)
          cv2.rectangle(img,(x,y-40),(x+w,y),color[result],-1)
          cv2.putText(img, labels[result], (x, y-10),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2)
      output_images.append(img)
  except Exception as e:
      print(e)
  index+=1

show_images(output_images)