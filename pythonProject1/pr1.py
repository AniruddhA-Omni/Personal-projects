import pandas as pd
import numpy as np
import sklearn
from sklearn import linear_model
from sklearn.utils import shuffle
import matplotlib.pyplot as py
import pickle
from matplotlib import style

data = pd.read_csv("student-mat.csv", sep=";")
#print(data.head())
data = data[["G1", "G2", "G3", "studytime", "failures", "absences"]]
#print(data.head())

predict = "G3"

X = np.array(data.drop([predict], 1))
Y = np.array(data[predict])
x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(X, Y, test_size=0.1)

"""best = 0
for i in range(50):
    x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(X, Y, test_size=0.1)
    linear = linear_model.LinearRegression() #implementing linear regression model
    linear.fit(x_train, y_train) #training the model
    acc = linear.score(x_test, y_test) #testting the model
    print(acc)
    if acc > best:
        with open("studentmodel.pickle", "wb") as f:
            pickle.dump(linear, f)"""

pk_in = open("studentmodel.pickle", "rb")
linear = pickle.load(pk_in)


print("Coeff: ", linear.coef_)
print("Intercept: ", linear.intercept_)

predictions = linear.predict(x_test)

for x in range(len(predictions)):
    print("Predicted: ",round(predictions[x]),"Target: ", y_test[x])

p = 'G2'
style.use('ggplot')
py.scatter(data[p], data['G3'])
py.xlabel(p)
py.ylabel("Final Grade")
py.show()