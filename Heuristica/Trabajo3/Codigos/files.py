import numpy as np
import pandas as pd
import math

#Function to read data
def read(path):
  cont = np.loadtxt(path)

#Extract the variables of the .txt file
  n = int(cont[0,0])
  R = int(cont[0,1])
  Q = int(cont[0,2])
  Th = int(cont[0,3])

  new_cont = cont[1:]

  nodes = new_cont[:,0]
  x = new_cont[:,1]
  y = new_cont[:,2]
  request = new_cont[:,3]
  dist = distance_matrix(x,y)

  return n,Q,R,Th,nodes,request,dist,x,y

#Euclidean distance
def distance(x0,y0,x1,y1):
  return np.sqrt((x0-x1)**2 + (y0-y1)**2)

#Function to find the distance matrix
def distance_matrix(x,y):
  M = 1e9
  dist = np.zeros((len(x),len(y)))
  for i in range(len(x)):
    for j in range(len(y)):
      if(i==j):
        dist[i,j] = M
      else:
        dist[i,j] = distance(x[i],y[i],x[j],y[j])
  return dist


def dataFrame(results, Th, Th_dist, route, run_time, R):
  data = []
  sum_dist = sum(Th_dist)
  aux = [x > Th for x in Th_dist]
  cons_len = [int(x) if x else 0 for x in aux]

  for i in range(R):
    data.append(np.append(route[i], [Th_dist[i],cons_len[i]]))

  #sorted_data = sorted(data, key=len, reverse=False)
  if(sum(cons_len)>0):
    data.append([sum(Th_dist), run_time, 1])
  else:
    data.append([sum(Th_dist), run_time, 0])

  df = pd.DataFrame(data)
  results.append(df)
  return results

def to_excel_AG(result, lista):
  # Export the DataFrame to an Excel file
  writer = pd.ExcelWriter('mtVRP_IsabellaMontoya_AG.xlsx', engine='xlsxwriter')
  for i, df in enumerate(result):
      df.to_excel(writer, sheet_name=lista[i], na_rep='', header=False, index=False)
  writer.save()
