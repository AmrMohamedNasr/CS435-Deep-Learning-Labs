import tensorflow as tf
tf.enable_eager_execution()
import matplotlib.pyplot as plt
import numpy as np
import random
from progressbar import progressbar

def build_fc_model():
  fc_model = tf.keras.Sequential([
      tf.keras.layers.Flatten(),
      # TODO: Define the rest of the model.
  ])
  return fc_model

def build_cnn_model():
    cnn_model = tf.keras.Sequential([
       # TODO: Define the model.
    ])
    return cnn_model

mnist = tf.keras.datasets.mnist
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()
train_images = np.expand_dims(train_images, axis=-1)/255.
train_labels = np.int64(train_labels)
test_images = np.expand_dims(test_images, axis=-1)/255.
test_labels = np.int64(test_labels)

plt.figure(figsize=(10,10))
random_inds = np.random.choice(60000,36)
for i in range(36):
    plt.subplot(6,6,i+1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    image_ind = random_inds[i]
    plt.imshow(np.squeeze(train_images[image_ind]), cmap=plt.cm.binary)
    plt.xlabel(train_labels[image_ind])
    
model = build_fc_model()
BATCH_SIZE = 64
EPOCHS = 5
# TODO compile and fit the model with the appropriate parameters.


#TODO: Use the evaluate method to test the model.


print('Test accuracy:', test_acc)

cnn_model = build_cnn_model()
print(cnn_model.summary())

#TODO: Compile and fit the CNN model.

#TODO: Use the evaluate method to test the model.

print('Test accuracy:', test_acc)
predictions = cnn_model.predict(test_images)

predictions[0]

#TODO: identify the digit with the highest confidence prediction for the first image in the test dataset

test_labels[0]