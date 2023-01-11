import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from mlxtend.plotting import plot_decision_regions
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import ConfusionMatrixDisplay, classification_report, confusion_matrix
from sklearn import metrics
from imblearn.under_sampling import NearMiss
from trans import PCA, transform
from plot import knn_comparison, plotScatter
from sklearn.metrics import RocCurveDisplay

def cleanData(data):
  data = data.replace(['Yes'],1)
  data = data.replace(['Yes (during pregnancy)'],0.8)
  data = data.replace(['No'],0)
  data = data.replace(['Male'],1)
  data = data.replace(['Female'],0)
  data = data.replace(['Excellent'],1)
  data = data.replace(['Very good'],0.75)
  data = data.replace(['Good'],0.5)
  data = data.replace(['Fair'],0.25)
  data = data.replace(['Poor'],0)
  data = data.replace(['No, borderline diabetes'],0.7)
  data = data.replace(['18-24'],21)
  data = data.replace(['25-29'],27)
  data = data.replace(['30-34'],32)
  data = data.replace(['35-39'],37)
  data = data.replace(['40-44'],42)
  data = data.replace(['45-49'],47)
  data = data.replace(['50-54'],52)
  data = data.replace(['55-59'],57)
  data = data.replace(['60-64'],62)
  data = data.replace(['65-69'],67)
  data = data.replace(['70-74'],72)
  data = data.replace(['75-79'],77)
  data = data.replace(['80 or older'],82)
  data=(data-data.min())/(data.max()-data.min())
  return data
# def trainData(data):
def main():
  predict= "HeartDisease"
  data=pd.read_csv("/Users/mariajosebernal/Documents/EAFIT/2022-1/Modelación y simulación/Proyecto/Python/heart_2020_cleaned.csv")
  data=data.drop(columns=["Race"])
  data=cleanData(data)
  y=data[predict]
  # y.value_counts().plot(kind='bar')
  # plt.show()
  X=data.drop(columns=[predict])
  X=PCA(X, 2)
  X=pd.DataFrame(X)
  
  n=815
  pr=1 
  
  print("1")
  x_train, x_test, y_train, y_test= train_test_split(X, y, test_size= 0.1, random_state=0)

  undersample = NearMiss(version=1,sampling_strategy=pr, n_neighbors=3)
  print("2")
  x_train,y_train= undersample.fit_resample(x_train,y_train)
  print("p1")
  print(len(x_train))
  weights='distance'
  classifier= KNeighborsClassifier(n_neighbors=n) 

  classifier.fit(x_train.values, y_train.values)
  # knn_comparison(x_train, y_train,classifier)
  
  y_pred= classifier.predict(x_test)
  # error=[]
  # xerror=[]
  # for i in range(1, 20):
  #   print(str(i)+ " de 20")
  #   knn = KNeighborsClassifier(n_neighbors=50*i)
  #   knn.fit(x_train.values, y_train.values)
  #   pred_i = knn.predict(x_test)
  #   xerror.append(50*i)
  #   error.append(metrics.roc_auc_score(y_test, pred_i))
  #   print(error[i-1])

  # plt.figure(figsize=(12, 6))
  # plt.plot(xerror, error, color='red', linestyle='dashed', marker='o',
  #         markerfacecolor='blue', markersize=10)
  # plt.title('AUC vs K-Value')
  # plt.xlabel('K-Value')
  # plt.ylabel('AUC')
  # plt.show()
  
  print(confusion_matrix(y_test, y_pred))
  print("k: " + str(n))
  print("proporcion: " + str(pr))
  print(classification_report(y_test, y_pred))
  print(metrics.f1_score(y_test, y_pred))
  print(metrics.roc_auc_score(y_test, y_pred))
  metrics.plot_roc_curve(classifier, x_test, y_test)
  plt.show()
main()