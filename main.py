###PSEUDOCODE 

###Inport sensor data + True/False data
###Partition data into train, validation, test

from tpfpclassifier import classifier, trainclassifier

###generate classifier
classifier=classifier(input_shape1, structure1, input_shape2, structure2, filters, kernel_size, dropout, computervision)
###train classifier
time1, test_acc1=trainclassifier(classifier, save_dir, train1, validation1, test1, train_labels, validation_labels, test_labels, label, train2, validation2, test2, computer_vision)

###Import environment input data + resource allocation output
###classifier.predict(input) to get probability, and add on to input data
###Partition data into train, validation, test

from severityanalysis import severityanalyser, trainanalyser
###generate analyser
analyser=severityanalyser(input_shape, output_num, structure)
###train analyser
trainanalyser(analyser, save_dir, train, validation, test, train_output, validation_output, test_output, label)