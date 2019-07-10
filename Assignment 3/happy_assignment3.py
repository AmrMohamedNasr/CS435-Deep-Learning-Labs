# -*- coding: utf-8 -*-
"""Happy_Assignment3

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vfWotXxqDbNxuDD-iRNCo37UAHRlcEiN

# Convolutional Neural Networks

## Happy Face Classification

Classify each picture as happy or not
"""

import numpy as np
from keras import layers
from keras.layers import Input, Dense, Activation, ZeroPadding2D, BatchNormalization, Flatten, Conv2D
from keras.layers import AveragePooling2D, MaxPooling2D, Dropout, GlobalMaxPooling2D, GlobalAveragePooling2D
from keras.models import Model, Sequential
from keras.preprocessing import image
from keras.optimizers import Adam, SGD
from keras.utils import layer_utils
from keras.utils.data_utils import get_file
from keras.applications.imagenet_utils import preprocess_input
import pydot
from IPython.display import SVG
from keras.utils.vis_utils import model_to_dot
from keras.utils import plot_model
import h5py
import keras.backend as K
K.set_image_data_format('channels_last')
import matplotlib.pyplot as plt
from matplotlib.pyplot import imshow
from sklearn.model_selection import train_test_split
import time
import keras
# %matplotlib inline

"""## Load Dataset Module"""

def load_dataset():
    path_to_train = "assignment3_train.h5"
    path_to_test = "assignment3_test.h5"
    train_dataset = h5py.File(path_to_train)
    train_x = np.array(train_dataset['train_set_x'][:])
    train_y = np.array(train_dataset['train_set_y'][:])

    test_dataset = h5py.File(path_to_test)
    test_x = np.array(test_dataset['test_set_x'][:])
    test_y = np.array(test_dataset['test_set_y'][:])

    # y reshaped
    train_y = train_y.reshape((1, train_x.shape[0]))
    test_y = test_y.reshape((1, test_y.shape[0]))

    return train_x, train_y, test_x, test_y

"""## Model Creation Modules"""

def HappyModel(input_shape, reg):
    """
    Implementation of the HappyModel.
    
    Arguments:
    input_shape -- shape of the images of the dataset

    Returns:
    model -- a Model() instance in Keras
    """
    dropOut = reg
    ### START CODE HERE ###
    X0 = Input(shape=input_shape)
    X = Conv2D(8, 3)(X0)
    X = BatchNormalization()(X)
    X = Activation('relu')(X)
    X = Conv2D(16, 3)(X)
    X = BatchNormalization()(X)
    X = Activation('relu')(X)
    X = MaxPooling2D()(X)
    X = Conv2D(32, 3)(X)
    X = BatchNormalization()(X)
    X = Activation('relu')(X)
    X = Conv2D(64, 3)(X)
    X = BatchNormalization()(X)
    X = Activation('relu')(X)
    X = MaxPooling2D()(X)
    X = Conv2D(128, 3)(X)
    X = BatchNormalization()(X)
    X = Activation('relu')(X)
    X = Conv2D(256, 3)(X)
    X = BatchNormalization()(X)
    X = Activation('relu')(X)
    X = MaxPooling2D()(X)
    X = Flatten()(X)
    X = Dense(1024)(X)
    X = BatchNormalization()(X)
    X = Activation('relu')(X)
    if (reg):
      X = dropOut(X)
    X = Dense(128)(X)
    X = BatchNormalization()(X)
    X = Activation('relu')(X)
    if (reg):
      X = dropOut(X)
    X = Dense(10)(X)
    X = BatchNormalization()(X)
    X = Activation('relu')(X)
    if (reg):
      X = dropOut(X)
    X = Dense(1)(X)
    X = Activation('sigmoid')(X)
    ### END CODE HERE ###
    model = Model(inputs = X0, outputs = X)
    return model
def readyMadeModel(input_shape, arch, reg, freeze, weights):
    model = Sequential()
    X0 = Input(shape=input_shape)
    pre_model = arch(weights=weights, include_top=False, input_tensor=X0)
    if freeze:
      for layer in pre_model.layers:
        layer.trainable = False
    model.add(pre_model)
    model.add(Flatten())
    model.add(Dense(1024))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    if (reg):
      model.add(reg)
    model.add(Dense(128))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    if (reg):
      model.add(reg)
    model.add(Dense(10))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    if (reg):
      model.add(reg)
    model.add(Dense(1))
    model.add(Activation('sigmoid'))
    return model
def vggRandomModel(input_shape, reg):
    return readyMadeModel(input_shape, keras.applications.VGG16, reg, None, None)
def vggPretrainedModel(input_shape, reg):
    return readyMadeModel(input_shape, keras.applications.VGG16, reg, None, 'imagenet')
def vggFrozenModel(input_shape, reg):
    return readyMadeModel(input_shape, keras.applications.VGG16, reg, True, 'imagenet')
def resRandomModel(input_shape, reg):
    return readyMadeModel(input_shape, keras.applications.ResNet50, reg, None, None)
def resPretrainedModel(input_shape, reg):
    return readyMadeModel(input_shape, keras.applications.ResNet50, reg, None, 'imagenet')
def resFrozenModel(input_shape, reg):
    return readyMadeModel(input_shape, keras.applications.ResNet50, reg, True, 'imagenet')

"""## Experiment code to be able to run different configurations"""

def run_experiment(build_model, optimizer, X, y, verbose = 0, reg = None):
  #Create, compile and fit the model
  ### START CODE HERE ### 
  model = build_model(X.shape[1:], reg)
  BATCH_SIZE = 64
  EPOCHS = 30
  train_X, val_X, train_y, val_y = train_test_split(X, y, train_size=0.8, random_state=3)
  
  model.compile(loss='binary_crossentropy', metrics=['accuracy'], optimizer=optimizer)
  
  start = time.time()
  history = model.fit(train_X, train_y, verbose=verbose, batch_size=BATCH_SIZE, epochs=EPOCHS, validation_data = (val_X, val_y) )
  end = time.time()
  
  #model.summary()
  
  # Plot training & validation accuracy values
  plt.plot(history.history['acc'])
  plt.plot(history.history['val_acc'])
  plt.title('Model accuracy')
  plt.ylabel('Accuracy')
  plt.xlabel('Epoch')
  plt.legend(['Train', 'Test'], loc='upper left')
  plt.show()

  # Plot training & validation loss values
  plt.plot(history.history['loss'])
  plt.plot(history.history['val_loss'])
  plt.title('Model loss')
  plt.ylabel('Loss')
  plt.xlabel('Epoch')
  plt.legend(['Train', 'Test'], loc='upper left')
  plt.show()
  print('Last validation loss : ', history.history['val_loss'][-1], ' | last training loss : ', history.history['loss'][-1])
  print('Last validation accuracy : ', history.history['val_acc'][-1], ' | last training accuracy : ', history.history['acc'][-1])
  print('Time taken in training : ', end - start, ' sec')
  return model, history.history['val_acc'][-1]

"""## Get best configuration from model dictionary according to highest validation accuracy"""

def get_best_configuration(models):
  maxVal = 0
  maxkey = ''
  for key,(model, value) in models.items():
    if (value > maxVal):
      maxkey = key
      maxVal = value
  return maxkey

"""## Model Evaluation Code"""

def evaluate_model(model, test_X, test_y):
  BATCH_SIZE = 64
  start = time.time()
  test_loss, test_acc = model.evaluate(test_X, test_y, verbose = 0, batch_size = BATCH_SIZE)
  end = time.time()
  print('Test loss:', test_loss)
  print('Test accuracy:', test_acc)
  print('Time taken in testing : ', end - start, ' sec')

"""## Dataset Setup"""

!wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1npiX3A9S8wGzVeK-r1iRLCCcLxDubUN_' -O assignment3_train.h5
!wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=17zOTEwEDjSqIYNvDpZokbCdE5IfcRGQ0' -O assignment3_test.h5

X_train_orig, Y_train_orig, X_test_orig, Y_test_orig = load_dataset()

# Normalize image vectors
X_train = X_train_orig/255.
X_test = X_test_orig/255.

# Reshape
Y_train = Y_train_orig.T
Y_test = Y_test_orig.T

print ("number of training examples = " + str(X_train.shape[0]))
print ("number of test examples = " + str(X_test.shape[0]))
print ("X_train shape: " + str(X_train.shape))
print ("Y_train shape: " + str(Y_train.shape))
print ("X_test shape: " + str(X_test.shape))
print ("Y_test shape: " + str(Y_test.shape))

"""## My Own Model Experiments"""

own_models = {}

"""### Adam optimizer with no regularization"""

own_models['adam'] = run_experiment(HappyModel, 'adam', X_train, Y_train, reg = None)

"""### SGD with no regularization"""

own_models['sgd'] = run_experiment(HappyModel, 'sgd', X_train, Y_train, reg = None)

"""### SGD with dropout 0.1"""

own_models['sgd_reg_0.1'] = run_experiment(HappyModel, 'sgd', X_train, Y_train, reg = Dropout(0.1))

"""### Adam with dropout 0.1"""

own_models['adam_reg_0.1'] = run_experiment(HappyModel, 'adam', X_train, Y_train, reg = Dropout(0.1))

"""### Adam with learning rate 0.0005 and dropout of 0.1"""

own_models['adam_0.0005_reg_0.1'] = run_experiment(HappyModel, Adam(0.0005), X_train, Y_train, reg = Dropout(0.1))

"""### Adam with dropout of 0.2"""

own_models['adam_reg_0.2'] = run_experiment(HappyModel, 'adam', X_train, Y_train, reg = Dropout(0.1))

"""## Best Model Configuration Evaluation"""

key = get_best_configuration(own_models)
values = own_models[key]
print(key, ' has the best validation accuracy ', values[1])
evaluate_model(values[0], X_test, Y_test)
values[0].summary()

"""## Ready-Made Architectures To Test"""

keras.applications.VGG16(include_top = False, input_shape = X_train.shape[1:]).summary()

keras.applications.ResNet50(include_top = False, input_shape = X_train.shape[1:]).summary()

"""## VGG16 Random Weights"""

vgg16rand_models = {}

"""### Adam with no regularization"""

vgg16rand_models['adam'] = run_experiment(vggRandomModel, 'adam', X_train, Y_train, None)

"""### Adam with dropout 0.2"""

vgg16rand_models['adam_reg_0.2'] = run_experiment(vggRandomModel, 'adam', X_train, Y_train, reg = Dropout(0.2))

"""### Adam with dropout 0.3"""

vgg16rand_models['adam_reg_0.3'] = run_experiment(vggRandomModel, 'adam', X_train, Y_train, reg = Dropout(0.3))

"""## VGG16 random weight evaluation"""

key = get_best_configuration(vgg16rand_models)
values = vgg16rand_models[key]
print(key, ' has the best validation accuracy ', values[1])
evaluate_model(values[0], X_test, Y_test)
values[0].summary()

"""## VGG16 Pretrained weights fine tuning"""

vgg16pre_models = {}

"""### Adam with no regularization"""

vgg16pre_models['adam'] = run_experiment(vggPretrainedModel, 'adam', X_train, Y_train, None)

"""### Adam with dropout 0.1"""

vgg16pre_models['adam_reg_0.1'] = run_experiment(vggPretrainedModel, 'adam', X_train, Y_train, reg = Dropout(0.1))

"""### Adam with dropout 0.2"""

vgg16pre_models['adam_reg_0.2'] = run_experiment(vggPretrainedModel, 'adam', X_train, Y_train, reg = Dropout(0.2))

"""## VGG16 Pretrained Model fine tuning Evaluation"""

key = get_best_configuration(vgg16pre_models)
values = vgg16pre_models[key]
print(key, ' has the best validation accuracy ', values[1])
evaluate_model(values[0], X_test, Y_test)
values[0].summary()

"""## VGG16 Pretrained weights freezing"""

vgg16fre_models = {}

"""### Adam with no regularization"""

vgg16fre_models['adam'] = run_experiment(vggFrozenModel, 'adam', X_train, Y_train, None)

"""### Adam with dropout 0.1"""

vgg16fre_models['adam_reg_0.1'] = run_experiment(vggFrozenModel, 'adam', X_train, Y_train, reg = Dropout(0.1))

"""### Adam with dropout 0.2"""

vgg16fre_models['adam_reg_0.2'] = run_experiment(vggFrozenModel, 'adam', X_train, Y_train, reg = Dropout(0.2))

"""## VGG16 Pretrained weights freezing evaluation"""

key = get_best_configuration(vgg16fre_models)
values = vgg16fre_models[key]
print(key, ' has the best validation accuracy ', values[1])
evaluate_model(values[0], X_test, Y_test)
values[0].summary()

"""## Resnet random weights"""

resrand_models = {}

"""### Adam with no regularization"""

resrand_models['adam'] = run_experiment(resRandomModel, 'adam', X_train, Y_train, None)

"""### Adam with dropout 0.1"""

resrand_models['adam_reg_0.1'] = run_experiment(resRandomModel, 'adam', X_train, Y_train, reg = Dropout(0.1))

"""### Adam with dropout 0.2"""

resrand_models['adam_reg_0.2'] = run_experiment(resRandomModel, 'adam', X_train, Y_train, reg = Dropout(0.2))

"""## ResNet random weights evaluation"""

key = get_best_configuration(resrand_models)
values = resrand_models[key]
print(key, ' has the best validation accuracy ', values[1])
evaluate_model(values[0], X_test, Y_test)
values[0].summary()

"""## Resnet Pretrained weights fine tuning"""

respre_models = {}

"""### Adam with no regularization"""

respre_models['adam'] = run_experiment(resPretrainedModel, 'adam', X_train, Y_train, None)

"""### Adam with dropout 0.1"""

respre_models['adam_reg_0.1'] = run_experiment(resPretrainedModel, 'adam', X_train, Y_train, reg = Dropout(0.1))

"""### Adam with dropout 0.2"""

respre_models['adam_reg_0.2'] = run_experiment(resPretrainedModel, 'adam', X_train, Y_train, reg = Dropout(0.2))

"""## ResNet pretrained weights fine tuning evaluation"""

key = get_best_configuration(respre_models)
values = respre_models[key]
print(key, ' has the best validation accuracy ', values[1])
evaluate_model(values[0], X_test, Y_test)
values[0].summary()

"""## Resnet Pretrained weights freezing"""

resfre_models = {}

"""### Adam with no regularization"""

resfre_models['adam'] = run_experiment(resFrozenModel, 'adam', X_train, Y_train, None)

"""### Adam with dropout 0.1"""

resfre_models['adam_reg_0.1'] = run_experiment(resFrozenModel, 'adam', X_train, Y_train, reg = Dropout(0.1))

"""### Adam with dropout 0.2"""

resfre_models['adam_reg_0.2'] = run_experiment(resFrozenModel, 'adam', X_train, Y_train, reg = Dropout(0.2))

"""## ResNet Pretrained weights freezing evaluation"""

key = get_best_configuration(resfre_models)
values = resfre_models[key]
print(key, ' has the best validation accuracy ', values[1])
evaluate_model(values[0], X_test, Y_test)
values[0].summary()

"""---
# Conclusion
* Time taken to train:
  * My Model : 20 second
  * VGG16 whole network : 60 second
  * VGG16 freezed and train final layers only : 30 second
  * Resnet whole network : 130-150 second
  * Resnet freezed and train final layers only : 90 second
* Test accuracies:
  * My model : 97.33%
  * VGG16 Random : 55.99%
  * VGG16 Initial Pretrained Weights : 44%
  * VGG16 Frozen : 97.77%
  * Resnet Random : 94%
  * Resnet Initial Pretrained Weights : 92.66%
  * Resnet Frozen : 44%
* Trainable Parameters:
  * My Model : 4.7 Million
  * VGG16 whole Network : 17 Million approximatly
  * VGG16 frozen : 2.2 Million
  * Resnet whole Network : 32 Million
  * Resnet frozen : 8.5 Million
* Adam works much better than SGD for this problem.
* Adding dropout helps a lot at getting the best performance due to its prevention of overfitting since the training set is quite small.
* VGG is very usefull when we freeze its convolutional layers, and bad if we try to train on our small dataset which is the opposite of Resnet which did quite well when trained from scratch and did badly when we froze its layers. Maybe removing the freezing on some of the last layers would help.
"""

