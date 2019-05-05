import re
import sys
import pandas as pd 
import numpy as np
import csv
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
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
    training_vector = list(csv.reader(csvfile, delimiter = ' '))
training_vector = training_vector[1]
while('' in training_vector) : 
    training_vector.remove('') 
for i in range(len(training_vector)):
	training_vector[i] = int(training_vector[i])
#print(training_vector)
with open("Leuk_ALL_AML.test.cls", "r", newline='') as csvfile:
    leuk_vector = list(csv.reader(csvfile, delimiter = ' '))
leuk_vector = leuk_vector[1]
while('' in leuk_vector) : 
    leuk_vector.remove('') 
for i in range(len(leuk_vector)):
	leuk_vector[i] = int(leuk_vector[i])
#print(leuk_vector)

top50 = pd.read_csv('testoutputTop50Ascending.csv')
top50 = top50.drop(columns=['Accession', 'P-VALUE\n'])
top50 = top50.transpose()
features = list(top50)
top50['FEATURE'] = training_vector


leuk_test = pd.read_csv('LEUK_TOP50.csv')

leuk_test = leuk_test.drop(columns=['Accession'])
leuk_test = leuk_test.transpose()
testing = list(leuk_test)
leuk_test['FEATURE'] = leuk_vector


train = top50[features]
leuk_vec = top50['FEATURE']
leuk_ = leuk_test[features]

knn = KNeighborsClassifier(algorithm='auto', leaf_size=30,
                           metric='minkowski', metric_params=None, n_jobs=1,
                           n_neighbors=1, p=2, weights='uniform')

knn.fit(train, leuk_vec)
PREDICTION = knn.predict(train)
PREDICTION2 = knn.predict(leuk_)
print('PREDCTION USING ORIGINAL VALUES')
print(PREDICTION)
print('PREDICTION USING TESTING VALUES')
print(PREDICTION2)

