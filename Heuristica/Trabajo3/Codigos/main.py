import os
import glob
import time
import numpy as np
import matplotlib.pyplot as plt
from AG import ex_AG
from Solutions import ex_constr, ex_ruido, ex_grasp
from plot import plt_routes, plt_dist, plt_times, plt_dist_2
from files import read, dataFrame, to_excel_AG

def execute_AG(files):
  results = []
  lista = []
  distances_AG = []
  run_vec_AG = []
  time_limit =  [300, 450, 600, 300, 300, 450, 600, 450, 300, 450, 450, 450]
  for j in range(len(files)):
    print(files[j])
    start_time = time.time()
    best_indiv = ex_AG(files[j], start_time, time_limit[j])
    end_time = time.time()
    run_time = round(end_time - start_time,2)

    car_routes = best_indiv[1]
    car_distances = best_indiv[2]
    R = best_indiv[5]
    Th = best_indiv[6]

    for i in range(len(car_distances)):
      car_distances[i] = round(car_distances[i], 2)

    distances_AG.append(round(sum(car_distances),2))    # Add the distance of every instances in distances
    run_vec_AG.append(run_time)          # Add the run time of every instances in run_vec
    constr = dataFrame(results, Th, car_distances, car_routes, run_time, R)  # Make a data frame with the output data
    lista.append(files[j][16:])
  
  return constr, lista, distances_AG, run_vec_AG 

# Read all the folder with each of the instances
folder_path = "mtVRP Instances"
file_extension = ".txt"

#Get a list of all files in the folder with the specified extension
files = glob.glob(os.path.join(folder_path, f"*{file_extension}"))
files.sort()  

# # Execute the algorithms
[r_AG, lista, distances_AG, run_vec_AG] = execute_AG(files)
to_excel_AG(r_AG, lista)
