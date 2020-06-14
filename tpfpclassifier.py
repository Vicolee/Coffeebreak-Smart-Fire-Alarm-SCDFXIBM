
import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Concatenate, Conv2D, Dense, Flatten, Reshape, Input, Dropout, Activation, MaxPool2D
from tensorflow.keras import Model
from tensorflow.keras.optimizers import Adam
import os
import time
import csv

###classifier function generates classifier model. If the input is just feature vector, then computervision=False. If the input includes images, then computervision=True

###input_shape1 is the input length of the feature vector, which includes measures such as CO levels, temperature, etc.
###input_shape2 is the input from CCTV footage at 3 time-stamps, i.e. at the moment of alarm ringing, 1 second after alarm starts and 5 seconds after alarm starts. 
###So input shape will be a*b*9, with a,b corresponding to image dimensions and 9 corresponding to RGB at the 3 instances. 

###classifier with computer vision is generated by this function. 
###classifier works by passing through input1 (feature vector) into a fully connected deep neural network, and input2 (image input) into a Convolutional neural network, i.e. VGG/AlexNet structures,
###the two inputs are flattened and concatenated together before being passed into a softmax layer (0 corresponds to FP, 1 corresponds to TP)

###structure1 is the structure for the deep neural network, i.e. structure1=[50,50,25] would be a network with fully connected dense layers input_shape1-50-50-25
###structure2, filters, kernel_size is the structure for the CNN, i.e.
    ###structure2=['m','d','m','p'], 'm' stands for 'maintain' where there is no downsampling, 'd' stands for 'downsampling', which is done via convolution w stride=(2,2) rather than maxpooling, 'p' stands for max-pooling
    ###filters=[32,32,32,32], represents the filters used in each layer, if 'p' is used, then the corresponding filter number does not matter
    ###kernel_size=[3,3,3,3], represents the kernel size for each layer, if 'p' is used, then the corresponding kernel size does not matter

###dropout refers to the dropout used per layer, applied to every layer except the one right before the softmax
###'relu' activation is used

def classifier(input_shape1, structure1, input_shape2=None, structure2=None, filters=None, kernel_size=None, dropout=0.1, computervision=False):
    if computervision==False:
        layer_num=len(structure1)
        inputs=Input(shape=input_shape1, name='input')
        a=inputs
        for i in range(layer_num):
            a=Dense(units=structure1[i], name='dense'+str(i+1))(a)
            a=Activation(activation='relu', name='activation'+str(i+1))(a)
            a=Dropout(rate=dropout, name='dropout'+str(i+1))(a)

        outputs=Dense(units=1,name='output', activation='softmax')(a)
        return Model(inputs=inputs,outputs=outputs)
    if computervision==True:
        layer_num1=len(structure1)
        layer_num2=len(structure2)

        inputs1=Input(shape=input_shape1, name='input1')
        a=inputs1
        
        inputs2=Input(shape=input_shape2, name='input2')
        b=inputs2

        for i in range(layer_num1):
            a=Dense(units=structure1[i], name='dense'+str(i+1))(a)
            a=Activation(activation='relu', name='activation'+str(i+1))(a)
            a=Dropout(rate=dropout, name='dropout'+str(i+1))(a)
        
        for i in range(layer_num2):
            if structure2[i]=='d':         
                b=Conv2D(filters=filters[i],kernel_size=kernel_size[i],strides=(2,2),padding='same',name='conv'+str(i+1))(b)
                b=Activation(activation='relu', name='activationC'+str(i+1))(b)
                b=Dropout(rate=dropout, name='dropoutC'+str(i+1))(b)
            if structure2[i]=='m':
                b=Conv2D(filters=filters[i],kernel_size=kernel_size[i],strides=1,padding='same',name='conv'+str(i+1))(b)
                b=Activation(activation='relu', name='activationC'+str(i+1))(b)
                b=Dropout(rate=dropout, name='dropoutC'+str(i+1))(b)
            if structure2[i]=='p':
                b=MaxPool2D(pool_size=(2,2), strides=None, padding='same', name='MaxPool'+str(i+1))(b)

        b=Flatten(name='flatten')(b)
        b=Dense(units=input_shape1[-1], name='compress')(b)
        
        concat=Concatenate(name='concat')([a, b])

        outputs=Dense(units=2,name='output', activation='softmax')(concat)
        return Model(inputs=[inputs1, inputs2],outputs=outputs)

###training data split into training set, validation set and test set. Time taken and test accuracy are returned, and model weights are saved @ savedir/weights_label.h5

def trainclassifier(classifier, save_dir, train1, validation1, test1, train_labels, validation_labels, test_labels, label, train2=None, validation2=None, test2=None, computer_vision=False):
    if os.path.isdir(save_dir)==False:
        os.mkdir(save_dir)
    ###use label to distinguish between different models, for example label='_NoComputerVision'

    optimizer=Adam(learning_rate=0.001, amsgrad=True)
    classifier.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])

    checkpoint_name=os.path.join(save_dir, 'weights'+label+'.h5')
    checkpoint=tf.keras.callbacks.ModelCheckpoint(checkpoint_name, monitor='val_loss', save_best_only=False, save_weights_only=True)
    csv_name=os.path.join(save_dir, 'loss_v_epoch'+label)
    csv_logger=tf.keras.callbacks.CSVLogger(csv_name)
    early=tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=False)

    t0=time.time()
    if computer_vision==False:
        classifier.fit(x=train1, y=train_labels, batch_size=64, epochs=50, shuffle=True, callbacks=[early, csv_logger, checkpoint], validation_data=(validation1, validation_labels))
        test_acc=classifier.evaluate(test1, test_labels)
    if computer_vision==True:
        classifier.fit(x=[train1, train2], y=train_labels, batch_size=64, epochs=50, shuffle=True, callbacks=[early, csv_logger, checkpoint], validation_data=([validation1, validation2], validation_labels))
        test_acc=classifier.evaluate([test1,test2], test_labels)
    tf=time.time()
    t=tf-t0
    return t, test_acc