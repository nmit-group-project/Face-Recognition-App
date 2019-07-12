# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 12:33:38 2019

@author: Prajna Shetty
"""

from __future__ import absolute_import, division, print_function, unicode_literals
import tensorflow as tf
import os
import matplotlib.pyplot as plt

base_dir= os.path.basename("Data")
folder=len([iq for iq in os.scandir(base_dir)])
new="New"
if not os.path.exists(new):
            os.makedirs(new)

IMAGE_SIZE = 224
BATCH_SIZE = 64

datagen = tf.keras.preprocessing.image.ImageDataGenerator(
    rescale=1./255, 
    validation_split=0.2)

train_generator = datagen.flow_from_directory(
    base_dir,
    target_size=(IMAGE_SIZE, IMAGE_SIZE),
    batch_size=BATCH_SIZE, 
    subset='training')

val_generator = datagen.flow_from_directory(
    base_dir,
    target_size=(IMAGE_SIZE, IMAGE_SIZE),
    batch_size=BATCH_SIZE, 
    subset='validation')

for image_batch, label_batch in train_generator:
  break
image_batch.shape, label_batch.shape

print (train_generator.class_indices)

labels = '\n'.join(sorted(train_generator.class_indices.keys()))

with open('New/labels.txt', 'w') as f:
  f.write(labels)
  
  IMG_SHAPE = (IMAGE_SIZE, IMAGE_SIZE, 3)

# Create the base model from the pre-trained model MobileNet V2
base_model = tf.keras.applications.MobileNetV2(input_shape=IMG_SHAPE,
                                              include_top=False, 
                                              weights='imagenet')

base_model.trainable = False

model = tf.keras.Sequential([
  base_model,
  tf.keras.layers.Conv2D(32, 3, activation='relu'),
  tf.keras.layers.Dropout(0.2),
  tf.keras.layers.GlobalAveragePooling2D(),
  tf.keras.layers.Dense(folder, activation='softmax')
])
      
model.compile(optimizer=tf.keras.optimizers.Adam(), 
  loss='categorical_crossentropy', 
  metrics=['accuracy'])
model.summary()
print('Number of trainable variables = {}'.format(len(model.trainable_variables)))

#Train the models
epochs = 10

history = model.fit(train_generator, 
                    epochs=epochs, 
                    validation_data=val_generator)

#Learning Curves
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

plt.figure(figsize=(8, 8))
plt.subplot(2, 1, 1)
plt.plot(acc, label='Training Accuracy')
plt.plot(val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.ylabel('Accuracy')
plt.ylim([min(plt.ylim()),1])
plt.title('Training and Validation Accuracy')

plt.subplot(2, 1, 2)
plt.plot(loss, label='Training Loss')
plt.plot(val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.ylabel('Cross Entropy')
plt.ylim([0,1.0])
plt.title('Training and Validation Loss')
plt.xlabel('epoch')
plt.show()

base_model.trainable = True

# Let's take a look to see how many layers are in the base model
print("Number of layers in the base model: ", len(base_model.layers))

# Fine tune from this layer onwards
fine_tune_at = 100

# Freeze all the layers before the `fine_tune_at` layer
for layer in base_model.layers[:fine_tune_at]:
  layer.trainable =  False
  
model.compile(loss='categorical_crossentropy',
    optimizer = tf.keras.optimizers.Adam(1e-5),
    metrics=['accuracy'])
model.summary()
print('Number of trainable variables = {}'.format(len(model.trainable_variables)))

history_fine = model.fit(train_generator, 
                         epochs=10,
                         validation_data=val_generator)
saved_model_dir = "New/save/"
tf.saved_model.save(model, saved_model_dir)

converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir)
tflite_model = converter.convert()

with open('New/model.tflite', 'wb') as f:
  f.write(tflite_model)