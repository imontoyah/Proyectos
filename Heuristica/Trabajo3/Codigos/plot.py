import matplotlib.pyplot as plt
import numpy as np
import random

def plt_routes(x,y,route):
  fig, ax = plt.subplots()
  ax.scatter(x[1:], y[1:])  # plot the nodes 
  ax.scatter(x[0], y[0], color='red')  # plot the deposit
  color = ['skyblue', 'orchid', 'yellowgreen', 'gold', 'navy', 'slategray']

  for i in range(len(route)):
    xcoor = []
    ycoor = []
    for j in range(len(route[i])):
      n = route[i][j]
      xcoor.append(x[n])
      ycoor.append(y[n])

    color_code = random.randint(0, 0xFFFFFF)
    #color = '#' + hex(color_code)[2:].zfill(6)

    ax.plot(xcoor, ycoor, color=color[i], label="Vehiculo"+str(i+1))

  # adjust the axis title and show the plot
  ax.set_xlabel('Position X', fontsize=15)
  ax.set_ylabel('Position Y', fontsize=15)
  ax.set_title('Route VND', fontsize=18, fontweight='bold')
  plt.legend(bbox_to_anchor=(1, 1), loc='upper left')
  plt.show()

def plt_times(files, times1, times2, times3, times4):
  plt.plot(files, times1 ,'o', label="Constructivo",color='skyblue')
  plt.plot(files, times2 ,'o', label="Grasp",color='orchid')
  plt.plot(files, times3 ,'o', label="Ruido",color='goldenrod')
  plt.plot(files, times4 ,'o', label="VND",color='yellowgreen')
  plt.xlabel("Instances",fontsize=15)
  plt.ylabel("Run time",fontsize=15)
  plt.title("Comparison between runtime algorithms",fontsize=18, fontweight='bold')
  plt.legend()
  plt.show()

def plt_times_2(files, times1, times2, times3, times4, times5, times6):
  plt.plot(files, times1 ,'o', label="Constructivo",color='skyblue')
  plt.plot(files, times2 ,'o', label="Ruido",color='navy')
  plt.plot(files, times3 ,'o', label="Grasp",color='slategray')
  plt.plot(files, times4 ,'o', label="VND",color='yellowgreen')
  plt.plot(files, times5 ,'o', label="VND modificado",color='orchid')
  plt.plot(files, times6 ,'o', label="Algoritmo memético",color='goldenrod')
  plt.xlabel("Instances",fontsize=15)
  plt.ylabel("Run time",fontsize=15)
  plt.title("Comparison between runtime algorithms",fontsize=18, fontweight='bold')
  plt.legend(loc="upper left")
  plt.show()

def plt_dist_2(files, dist1, dist2, cota_min):
  gap_constr = []
  gap_grasp = []
  for i in range(len(dist1)):
    gap_constr.append((dist1[i]-cota_min[i])/cota_min[i])
    gap_grasp.append((dist2[i]-cota_min[i])/cota_min[i])

  plt.plot(files, gap_constr ,'o', label="Algoritmo memético",color='skyblue')
  plt.plot(files, gap_grasp ,'o', label="Teórico", color='orchid')
  #plt.plot(files, cota_min ,'o', label="Cota min",color='palegreen')
  plt.xlabel("Instances",fontsize=15)
  plt.ylabel("GAP distance",fontsize=15)
  plt.title("Comparison of the GAP distance",fontsize=18,fontweight='bold')
  plt.legend()
  plt.show()

  return gap_constr, gap_grasp

def plt_dist(files, dist1, dist2, dist3, dist4, cota_min):
  gap_constr = []
  gap_grasp = []
  gap_ruido = []
  gap_VND = []
  for i in range(len(dist1)):
    gap_constr.append((dist1[i]-cota_min[i])/cota_min[i])
    gap_grasp.append((dist2[i]-cota_min[i])/cota_min[i])
    gap_ruido.append((dist3[i]-cota_min[i])/cota_min[i])
    gap_VND.append((dist4[i]-cota_min[i])/cota_min[i])

  plt.plot(files, gap_constr ,'o', label="25",color='skyblue')
  plt.plot(files, gap_grasp ,'o', label="50", color='orchid')
  plt.plot(files, gap_ruido ,'o', label="75",color='goldenrod')
  plt.plot(files, gap_VND ,'o', label="100",color='yellowgreen')
  #plt.plot(files, cota_min ,'o', label="Cota min",color='palegreen')
  plt.xlabel("Instances",fontsize=15)
  plt.ylabel("GAP distance",fontsize=15)
  plt.title("Comparison of the GAP distance",fontsize=18,fontweight='bold')
  plt.legend()
  plt.show()

  return gap_constr, gap_grasp, gap_ruido, gap_VND


