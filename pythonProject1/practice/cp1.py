import sklearn
import numpy as np
import pandas as pd
from sklearn import svm
from sklearn import metrics
from sklearn import datasets

#here Im using SVm for predicting type of wine

D = datasets.load_wine()
features = D.feature_names
labels = D.target_names
classes = ['Jony Walker', 'Black Dog', 'Royal Stag']
#print(features,"\n\n\n")
#print(labels)


X = D.data
y = D.target

x_train,x_test,y_train,y_test = sklearn.model_selection.train_test_split(X,y,test_size=0.2)

clf = svm.SVC(kernel="linear", C= 2)
clf.fit(x_train,y_train)
y_predict = clf.predict(x_test)
acc = metrics.accuracy_score(y_test, y_predict)

for i in range(len(y_predict)):
    print("Predicted: ",classes[y_predict[i]]," Target: ",classes[y_test[i]])

print("\n\nAccuracy: ",round(acc*100,3),"%")