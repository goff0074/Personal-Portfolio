import numpy as np
from keras.datasets import mnist
from matplotlib import pyplot
from numpy.linalg import norm
import ssl

# Disable SSL certificate verification
ssl._create_default_https_context = ssl._create_unverified_context

(X_train, y_train), (X_test, y_test) = mnist.load_data()

X_train = X_train[:600,:,:].astype("float32")/255 # Scale images to the [0,1] range
y_train = y_train[:600]
N_train = X_train.shape[0]
X_train = X_train.reshape((N_train,28*28))

X_test = X_test[:100,:,:].astype("float32")/255 # Scale images to the [0,1] range
y_test = y_test[:100]
N_test = X_test.shape[0]
X_test = X_test.reshape((N_test,28*28))

print("Trainset X shape: " + str(X_train.shape))
print("train label y shape: " + str(y_train.shape))
print("Testset X shape: " + str(X_test.shape))
print("test label y shape: " + str(y_test.shape))

def visualization(idx_lst,data,label):
  '''
  This function is used to visualize original dataset X or cluster representative matrix Z
  '''
  N = data.shape[0]
  for idx in idx_lst:
    pyplot.imshow(data.reshape((N,28,28))[idx], cmap=pyplot.get_cmap('gray'))
    pyplot.show()
    print("The corresponding label of this image is {}".format(label[idx]))

v1 = X_train[1]
v2 = X_train[8]
w = X_test[5]
print(v1.shape)
print(w.shape)

def knn(X_train,y_train,X_test,y_test,k = 7):
  N_train = X_train.shape[0]
  N_test = X_test.shape[0]
  y_predict = -np.ones((N_test, 1), dtype=int)
  ###### YOUR CODE STARTS HERE #####
  for i in range(N_test):
    x = X_test[[i], :]
    d = np.zeros((N_train, 1))
    for j in range(N_train):
      d[j] = np.linalg.norm(x - X_train[[j], :])
    idx = np.argsort(d.flatten())[:k]
    common_label = np.bincount(y_train[idx].flatten())
    predict_label = np.argmax(common_label) 
    y_predict[i] = predict_label

  ###################################
  return y_predict

# Updated here v1.6
y_predict = knn(X_train,y_train,X_test,y_test,7)
y_predict = y_predict.flatten()
predict_acc = np.sum((y_predict-y_test)==0)/N_test
print("The prediction accuracy = {}%, which should be greater than 80%".format(predict_acc*100))