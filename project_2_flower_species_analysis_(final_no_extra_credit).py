# -*- coding: utf-8 -*-
"""Project 2 - Flower Species Analysis (Final - No Extra Credit).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1lGswZ9M9jTfKv61umAVYNCxthsL3G3XG
"""

# Commented out IPython magic to ensure Python compatibility.
#----------------------------------------
#  CSC 315 / 615 Spring 2023
#  Project 2 Flower Species Analysis
#
# <<Chris Eagar>>
#----------------------------------------


# %matplotlib inline
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
import numpy as np
import pandas as pd



#----
# Define your functions here
#----

def PlotGraph(xaxis, yaxis, centroids):

  varietylist = list(df['variety'])
  varietyset = set(varietylist)


  #create ax as a subplot
  fig, ax = plt.subplots()


  for variety in varietyset:
    mask = df['variety'] == variety
    filtered = df[mask]

    if(variety == 'Setosa'):
      color = 'red'
    elif(variety == 'Versicolor'):
      color = 'violet'
    else:
      color = 'blue'
    ax.plot(filtered[xaxis], filtered[yaxis], 'o', color = color)


  for variety in centroids:
    centroid = centroids[variety]
    ax.plot(centroid[0], centroid[1], 'X', color='black', markersize=20)
    ax.text(centroid[0], centroid[1]-0.4, variety, ha='center', fontsize=10)

  #label axes and title
  ax.set_xlabel(xaxis, fontsize=10)
  ax.set_ylabel(yaxis, fontsize=10)
  ax.set_title(xaxis + ' vs. ' + yaxis, fontsize=15)




def CentroidLocater(xaxis, yaxis):

  varietylist = list(df['variety'])
  varietyset = set(varietylist)

  SetosaXTotal = 0
  SetosaYTotal = 0
  VersicolorXTotal = 0
  VersicolorYTotal = 0
  VirginicaXTotal = 0
  VirginicaYTotal = 0

  for variety in varietyset:

    mask = df['variety'] == variety
    filtered = df[mask]
    array = filtered.loc[:, [xaxis, yaxis]].values

    if(variety == 'Setosa'):
      SetosaXTotal += filtered[xaxis].sum()
      SetosaYTotal += filtered[yaxis].sum()
    elif(variety == 'Versicolor'):
      VersicolorXTotal += filtered[xaxis].sum()
      VersicolorYTotal += filtered[yaxis].sum()
    else:
      VirginicaXTotal += filtered[xaxis].sum()
      VirginicaYTotal += filtered[yaxis].sum()

  SetosaXMean = SetosaXTotal / len(df[df['variety'] == 'Setosa'])
  SetosaYMean = SetosaYTotal / len(df[df['variety'] == 'Setosa'])

  VersicolorXMean = VersicolorXTotal / len(df[df['variety'] == 'Versicolor'])
  VersicolorYMean = VersicolorYTotal / len(df[df['variety'] == 'Versicolor'])

  VirginicaXMean = VirginicaXTotal / len(df[df['variety'] == 'Virginica'])
  VirginicaYMean = VirginicaYTotal / len(df[df['variety'] == 'Virginica'])

  return {'Setosa': (SetosaXMean, SetosaYMean),
          'Versicolor': (VersicolorXMean, VersicolorYMean),
          'Virginica': (VirginicaXMean, VirginicaYMean)}


#----
# Read the Iris data
#----
df = pd.read_csv("iris.csv")

#----
# Run your main code here
#----


centroids = CentroidLocater('sepal.width', 'sepal.length')
PlotGraph('sepal.width', 'sepal.length', centroids)

centroids = CentroidLocater('petal.length', 'sepal.length')
PlotGraph('petal.length', 'sepal.length', centroids)

centroids = CentroidLocater('petal.length', 'sepal.width')
PlotGraph('petal.length', 'sepal.width', centroids)

centroids = CentroidLocater('petal.width', 'sepal.length')
PlotGraph('petal.width', 'sepal.length', centroids)

centroids = CentroidLocater('petal.width', 'sepal.width')
PlotGraph('petal.width', 'sepal.width', centroids)

centroids = CentroidLocater('petal.width', 'petal.length')
PlotGraph('petal.width', 'petal.length', centroids)