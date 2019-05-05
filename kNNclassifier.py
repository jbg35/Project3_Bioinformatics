import re
import sys
import pandas as pd 
import numpy as np
import csv
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn import tree


# 6.     Write a computer program (Python/C++/Java) to implement the kNN classifier. Each group could choice your own favorite distance measures and values for the parameters involved in kNN. For example:
# a.      Use Euclidean distance  to calculate the distance between samples and pick 3 for k
# b.     Use Euclidean distance  to calculate the distance between samples and pick 5 for k
# c.      Use Manhattan distance  to calculate the distance between samples and pick 3 for k
# d.     Calculate distances based on one individual gene, pick 3 for k and then use jury decision (majority rule) for the classification
# e.      Calculate distances based on one individual gene, pick 5 for k and then use jury decision (majority rule) for the classification

# 7.     Use your classifier to classify the testing samples

# 8.     Report your results. 

with open("ALL_vs_AML_train_set_38_sorted.cls", "r", newline='') as csvfile:
    train_labels = list(csv.reader(csvfile, delimiter = ' '))
train_labels = train_labels[1]
while('' in train_labels) : 
    train_labels.remove('') 
for i in range(len(train_labels)):
	train_labels[i] = int(train_labels[i])

with open("Leuk_ALL_AML.test.cls", "r", newline='') as csvfile:
    leuk_labels = list(csv.reader(csvfile, delimiter = ' '))
leuk_labels = leuk_labels[1]
while('' in leuk_labels) : 
    leuk_labels.remove('') 
for i in range(len(leuk_labels)):
	leuk_labels[i] = int(leuk_labels[i])

top50 = pd.read_csv('testoutputTop50Ascending.csv')
top50 = top50.drop(columns=['Accession', 'P-VALUE\n'])
top50 = top50.transpose()
features = list(top50)
top50['FEATURE'] = train_labels
#print(top50)

leuk_test = pd.read_csv('leukoutput.csv')
leuk_test = leuk_test.drop(columns=['Accession', '\n'])
leuk_test = leuk_test.transpose()
testing = list(leuk_test)
leuk_test['FEATURE'] = leuk_labels

train = top50[features]
train_labels = top50['FEATURE']

leuk_ = leuk_test[features]
leuk_labels = leuk_test['FEATURE']

knn = KNeighborsClassifier(algorithm='auto', leaf_size=30,
                           metric='minkowski', metric_params=None, n_jobs=1,
                           n_neighbors=1, p=2, weights='uniform')

knn.fit(train, train_labels)
print(knn.predict(train))

# checking classifier
print("Predictions for train data:")
print(knn.predict(train))
print("Target values for train:")
print(train_labels)
# using the classifier
print("Predictions from the classifier for test:")
print(knn.predict(leuk_))
print("Target values for test:")
print(leuk_labels)
