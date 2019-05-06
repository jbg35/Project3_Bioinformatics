import re
import sys
import pandas as pd 
import numpy as np
import csv
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score
from sklearn import tree, neighbors, datasets, linear_model

cmap_light = ListedColormap(['#FFAAAA', '#AAFFAA', '#AAAAFF'])
cmap_bold = ListedColormap(['#FF0000', '#00FF00', '#0000FF'])

with open("ALL_vs_AML_train_set_38_sorted.cls", "r", newline='') as csvfile:
    training_vector = list(csv.reader(csvfile, delimiter = ' '))
training_vector = training_vector[1]
while('' in training_vector) : 
    training_vector.remove('') 
for i in range(len(training_vector)):
    training_vector[i] = int(training_vector[i])
with open("Leuk_ALL_AML.test.cls", "r", newline='') as csvfile:
    leuk_vector = list(csv.reader(csvfile, delimiter = ' '))
leuk_vector = leuk_vector[1]
while('' in leuk_vector) : 
    leuk_vector.remove('') 
for i in range(len(leuk_vector)):
    leuk_vector[i] = int(leuk_vector[i])


####### TOP50 PLOT ########
top50 = pd.read_csv('testoutputTop50Ascending.csv')
top50 = top50.drop(columns=['Accession', 'P-VALUE\n'], axis=0)
top50 = top50.transpose()

features = list(top50)
top50['FEATURE'] = training_vector

X = np.array(top50.ix[:, 0:2])

y = np.array(top50['FEATURE']) 

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
h = 10

knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X_train, y_train)
pred = knn.predict(X_test)

x_min, x_max = X_train[:, 0].min() - 100, X_train[:, 0].max() + 100
y_min, y_max = X_train[:, 1].min() - 100, X_train[:, 1].max() + 100
xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                     np.arange(y_min, y_max, h))

Z = knn.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)
plt.figure()
plt.pcolormesh(xx, yy, Z, cmap=cmap_light)

# Plot also the training points
plt.scatter(X[:, 0], X[:, 1], c=y, cmap=cmap_bold,
            edgecolor='k', s=20)
plt.xlim(xx.min(), xx.max())
plt.ylim(yy.min(), yy.max())
plt.title("AML_ALL")
plt.show()




##### LEUK PLOT #######
leuk_test = pd.read_csv('LEUK_TOP50.csv')

leuk_test = leuk_test.drop(columns=['Accession'],axis=0)
leuk_test = leuk_test.transpose()
testing = list(leuk_test)
leuk_test['FEATURE'] = leuk_vector

X = np.array(leuk_test.ix[:, 0:2])

y = np.array(leuk_test['FEATURE']) 


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
h = 10

knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X_train, y_train)
pred = knn.predict(X_test)

x_min, x_max = X_train[:, 0].min() - 100, X_train[:, 0].max() + 100
y_min, y_max = X_train[:, 1].min() - 100, X_train[:, 1].max() + 100
xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                     np.arange(y_min, y_max, h))

Z = knn.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)
plt.figure()
plt.pcolormesh(xx, yy, Z, cmap=cmap_light)

plt.scatter(X[:, 0], X[:, 1], c=y, cmap=cmap_bold,
            edgecolor='k', s=20)
plt.xlim(xx.min(), xx.max())
plt.ylim(yy.min(), yy.max())
plt.title("ALL AML")
plt.show()
