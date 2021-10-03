import pandas as pd
import numpy as np
import sklearn
from sklearn import linear_model,preprocessing,datasets
from sklearn.neighbors import KNeighborsClassifier

D = datasets.load_wine()
X = D.data
y = D.target

classes = ['Jony Walker', 'Black Dog', 'Royal Stag']

x_train,x_test,y_train,y_test = sklearn.model_selection.train_test_split(X,y,test_size=0.2)

model = KNeighborsClassifier(n_neighbors=3)

model.fit(x_train,y_train)
acc = model.score(x_test,y_test)
y_predict = model.predict(x_test)

for i in range(len(y_predict)):
    print("Predicted: ",classes[y_predict[i]]," Target: ",classes[y_test[i]])
print(acc)