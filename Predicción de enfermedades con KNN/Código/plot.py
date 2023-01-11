import matplotlib.pyplot as plt
import pandas as pd
from sklearn import datasets, neighbors
from mlxtend.plotting import plot_decision_regions

def knn_comparison(X,y,clf):
 X = X.values
 y = y.astype(int).values
# Plotting decision region
 plot_decision_regions(X, y, clf=clf, legend=2)
# Adding axes annotations
 plt.xlabel('X')
 plt.ylabel('Y')
 plt.title('Knn areas')
 plt.show()
 
def plotScatter(X,y):
  df2=pd.concat([y,X], axis=1)
  
  plt.scatter(df2['x'][(df2.HeartDisease == 1)],
    df2['y'][(df2.HeartDisease == 1)],
    marker='D',
    color='red',
    label='Enfermos')
  
  plt.scatter(df2['x'][df2.HeartDisease == 0],
    df2['y'][df2.HeartDisease == 0],
    marker='o',
    color='blue',
    label='Sanos')
  
  plt.xlabel('x')
  plt.ylabel('y')
  plt.legend()
  plt.show()