import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Concatenate, Conv2D, Dense, Flatten, Reshape, Input, Dropout, Activation, MaxPool2D
from tensorflow.keras import Model
from tensorflow.keras.optimizers import Adam
import os
import time
import csv

###Input is the probability from FP/TP classifier + environmental factors, e.g. distance from escape, human density etc. 
###Output will be a vector that states resources that needs to be deployed, e.g. number of people deployed etc. In the training phase, the data for the output vector will be based on how resource allocation was done in the past. 

###dropout refers to the dropout used per layer, applied to every layer except the one right before the softmax
###'relu' activation is used

def severityanalyser(input_shape, output_num, structure, dropout=0.1):
    layer_num=len(structure)
    inputs=Input(shape=input_shape, name='input')
    a=inputs
    for i in range(layer_num):
        a=Dense(units=structure[i], name='dense'+str(i+1))(a)
        a=Activation(activation='relu', name='activation'+str(i+1))(a)
        a=Dropout(rate=dropout, name='dropout'+str(i+1))(a)

    outputs=Dense(units=output_num,name='output')(a)
    return Model(inputs=inputs,outputs=outputs)

###training data split into training set, validation set and test set. Time taken and test accuracy are returned, and model weights are saved @ savedir/weights_label.h5

def trainanalyser(model, save_dir, train, validation, test, train_output, validation_output, test_output, label):
    if os.path.isdir(save_dir)==False:
        os.mkdir(save_dir)
    ###use label to distinguish between different models, for example label='severityanalyser'

    optimizer=Adam(learning_rate=0.001, amsgrad=True)
    model.compile(optimizer=optimizer, loss='mse')

    checkpoint_name=os.path.join(save_dir, 'weights'+label+'.h5')
    checkpoint=tf.keras.callbacks.ModelCheckpoint(checkpoint_name, monitor='val_loss', save_best_only=False, save_weights_only=True)
    csv_name=os.path.join(save_dir, 'loss_v_epoch'+label)
    csv_logger=tf.keras.callbacks.CSVLogger(csv_name)
    early=tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=False)

    t0=time.time()
    model.fit(x=train, y=train_output, batch_size=64, epochs=50, shuffle=True, callbacks=[early, csv_logger, checkpoint], validation_data=(validation, validation_output))
    test_acc=model.evaluate(test, test_output)
    tf=time.time()
    t=tf-t0
    return t, test_acc