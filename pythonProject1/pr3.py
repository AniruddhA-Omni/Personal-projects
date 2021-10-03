import sklearn
from sklearn import datasets
from sklearn import svm
from sklearn import metrics
import tensorflow as tf

cancer = datasets.load_breast_cancer()
features = cancer.feature_names
labels = cancer.target_names

#print(features,"\n\n")
#print(labels)

X = cancer.data
y = cancer.target

x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y, test_size=0.2)

classes = ['malignant','benign']

clf = svm.SVC(kernel="linear", C = 2)
clf.fit(x_train, y_train)

y_predict = clf.predict(x_test)
acc = metrics.accuracy_score(y_test, y_predict)
for i in range(len(y_predict)):
    print("Predicted: ", classes[y_predict[i]], "Target: ", classes[y_test[i]])
print("\n")
print(acc)

print(tf.test.is_gpu_available())
