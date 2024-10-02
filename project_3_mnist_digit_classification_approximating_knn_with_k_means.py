# -*- coding: utf-8 -*-
"""Project 3 - MNIST Digit Classification Approximating KNN with K-Means.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Ud1_pF6HcFu758Nnb6y_nwIIuNKP-Cqu
"""

#----------------------------------------
#  CSC 315 / 615 Spring 2023
#  Project 3 MNIST Digit Classification
#
#  <<Chris Eagar>>
#----------------------------------------


from sre_constants import RANGE_UNI_IGNORE
import matplotlib.pyplot as plt
from IPython import display
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import time
from keras.datasets import mnist
from sklearn.metrics import pairwise_distances_argmin
from sklearn.metrics import confusion_matrix
import seaborn as sn
from sklearn.cluster import KMeans

#
# Any of the following code (or program flow) can be
#   changed freely except the data loading.
#
# This template is designed only to demonstrate
#   how to load data and make certain kinds of plots.
#

#----------------------------------
# Load the data
#----------------------------------
(x_train, y_train), (x_test, y_test) = mnist.load_data() #do not change this line
nClass = 10
nTrain = 60000
nTest  = 10000
sX = 28
sY = 28
dim = sX*sY

# Flatten the training data
x_train = x_train.reshape(nTrain,dim)
x_test  = x_test.reshape(nTest,dim)


#-----------------------------------
# Function to Split the MNIST training data
#-----------------------------------

def SplitTrainData():
  class_images = {}
  for i in range(nClass):
    class_images[i] = []

  for i in range(nTrain):
    image = x_train[i]
    label = y_train[i]
    class_images[label].append(image)

  return class_images


#-----------------------------------
# Function to Split the MNIST test data
#-----------------------------------

def SplitTestData():
  class_images = {}
  for i in range(nClass):
    class_images[i] = []

  for i in range(nTest):
    image = x_test[i]
    label = y_test[i]
    class_images[label].append(image)

  return class_images


#-----------------------------------
# Function to run K-means on each of the 10 groups
#-----------------------------------

def ApproxTrainDataSet():

  class_images_train = SplitTrainData()

  kmeans_centers = {}
  for label, images in class_images_train.items():
    kmeans = KMeans(n_clusters=9, random_state=0, n_init=10)
    kmeans.fit(images)
    kmeans_centers[label] = kmeans.cluster_centers_


  approximate_x = []
  approximate_y = []
  for label, centers in kmeans_centers.items():
    for center in centers:
      approximate_x.append(center)
      approximate_y.append(label)

  return np.array(approximate_x), np.array(approximate_y)


#-----------------------------------
# Function to classify the testing data
#-----------------------------------

def classify_images(x_train, y_train, x_test, y_test):
    # Preprocessing
    x_train = x_train.reshape(nTrain, dim)
    x_test = x_test.reshape(nTest, dim)

    # Approximate training data using k-means
    x_approx, y_approx = ApproxTrainDataSet()

    # Normalize pixel values to [0, 1]
    x_train = x_train.astype('float32') / 255.0
    x_test = x_test.astype('float32') / 255.0
    x_approx = x_approx.astype('float32') / 255.0

    # Train 1-nearest neighbor classifier
    knn = KNeighborsClassifier(n_neighbors=1)
    knn.fit(x_approx, y_approx)

    # Predict labels of test data
    t_start = time.time()
    y_pred = knn.predict(x_test)
    t_end = time.time()

    total_time = t_end-t_start

    # Postprocessing
    y_test = np.array(y_test)
    accuracy = np.mean(y_pred == y_test) * 100

    return accuracy, total_time, y_pred

accuracy, time, y_test_pred = classify_images(x_train, y_train, x_test, y_test)


#-----------------------------------
# Display the histograms
#-----------------------------------

# Split the MNIST training and test data
class_images_train = SplitTrainData()
class_images_test = SplitTestData()

# Create two subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10,10))

# Plot Training histogram
train_data = [len(class_images_train[i]) for i in range(nClass)]
ax1.bar(range(10), train_data, width=1, align='center', edgecolor='black')
ax1.set(xticks=range(10), xlim=[-1, 10])
ax1.set_xlabel('digit 0-9')
ax1.set_ylabel('number of images')
ax1.set_title('training digit frequency')

# Plot Test histogram
test_data = [len(class_images_test[i]) for i in range(nClass)]
ax2.bar(range(10), test_data, width=1, align='center', edgecolor='black')
ax2.set(xticks=range(10), xlim=[-1, 10])
ax2.set_xlabel('digit 0-9')
ax2.set_ylabel('number of images')
ax2.set_title('testing digit frequency')

plt.subplots_adjust(hspace=0.4)

# Display the plot
plt.show()


#-----------------------------------
# Display the digit clusters
#-----------------------------------

dataset = ApproxTrainDataSet()

for digit in range(10):
    fig, axs = plt.subplots(3, 3, figsize=(8,8))
    for i in range(3):
        for j in range(3):
            index = digit*9 + i*3 + j
            img = dataset[0][index].reshape(sX, sY)
            axs[i, j].imshow(img, cmap='gray')
            axs[i, j].axis('off')
            axs[i, j].set_title("Digit " + str(digit) + " Cluster " + str(i*3+j+1), fontsize=8)
    plt.show()

#------------------------
# Display a confusion matrix
#------------------------
confusion = confusion_matrix(y_test, y_test_pred)
fig, ax = plt.subplots(figsize=(8,8))
sn.heatmap(confusion, annot=True, fmt=".4g")
ax.set_xlabel('true')
ax.set_ylabel('predicted')
ax.set_title('test accuracy ' + str(accuracy) + '%' + ' prediction time ' + '{:.2f}'.format(time) + ' seconds')
plt.show()

#------------------------
# Display the closest cluster for the first 20 images
# Could not get the titles for the cluster image to work**
#------------------------

def display_closest_cluster(x_test, y_test, kmeans_centers):
    # Preprocessing
    x_test = x_test.reshape(nTest, dim)
    x_test = x_test.astype('float32') / 255.0

    # Predict the closest cluster center for each test image
    closest_cluster_centers = []
    for i in range(20):
        distances = pairwise_distances_argmin(x_test[i].reshape(1,-1), kmeans_centers[y_test[i]])
        closest_cluster_centers.append(kmeans_centers[y_test[i]][distances][0])

    # Display the test image and closest cluster center for each test image
    fig, axs = plt.subplots(20, 2, figsize=(8,40))
    for i in range(20):
        axs[i][0].imshow(x_test[i].reshape(28,28), cmap='gray')
        axs[i][0].axis('off')
        axs[i][1].imshow(closest_cluster_centers[i].reshape(28,28), cmap='gray')
        axs[i][1].axis('off')
        axs[i][0].set_title('Test Image {} | True Label: {}'.format(i, y_test[i]))
        axs[i][1].set_title('Closest Cluster {} | Cluster Label: {}'.format(i, np.argmin(distances)))
    plt.show()

class_images_train = SplitTrainData()
kmeans_centers = {}
for label, images in class_images_train.items():
    kmeans = KMeans(n_clusters=9, random_state=0, n_init=10)
    kmeans.fit(images)
    kmeans_centers[label] = kmeans.cluster_centers_

display_closest_cluster(x_test, y_test, kmeans_centers)