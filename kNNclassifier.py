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
    data = list(csv.reader(csvfile, delimiter = ' '))
data = data[1]
while('' in data) : 
    data.remove('') 
for i in range(len(data)):
	data[i] = int(data[i])

with open("Leuk_ALL_AML.test.cls", "r", newline='') as csvfile:
    leuk_data = list(csv.reader(csvfile, delimiter = ' '))
leuk_data = leuk_data[1]
while('' in leuk_data) : 
    leuk_data.remove('') 
for i in range(len(leuk_data)):
	leuk_data[i] = int(leuk_data[i])

