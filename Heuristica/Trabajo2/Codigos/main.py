import os
import glob
import time
import numpy as np
from Solutions import ex_constr, ex_ruido, ex_grasp
from plot import plt_routes, plt_dist, plt_times
from VND import func_VND, func_VND_mixed
from files import read, dataFrame, to_excel_VND, to_excel_VND_mixed

def ex_VND(files):
  results = []
  lista = []
  distances_vnd = []
  run_vec_vnd = []
  time_limit =  [300, 450, 600, 300, 300, 450, 600, 450, 300, 450, 450, 450]
  #Loop through each file and read its contents
  for j in range(len(files)):
    start_time = time.time()
    param_ruido = (-1,1)
    [car_routes, car_distances, R, Th] = func_VND(files[j], param_ruido, start_time, time_limit[j])
    end_time = time.time()
    run_time = round(end_time - start_time,2)
  
    for i in range(len(car_distances)):
      car_distances[i] = round(car_distances[i], 2)

    distances_vnd.append(round(sum(car_distances),2))    # Add the distance of every instances in distances
    run_vec_vnd.append(run_time)          # Add the run time of every instances in run_vec
    constr = dataFrame(results, Th, car_distances, car_routes, run_time, R)  # Make a data frame with the output data
    lista.append(files[j][16:])
  return constr, lista, distances_vnd, run_vec_vnd 

def ex_VND_mixed(files):
  results = []
  distances_vnd = []
  run_vec_vnd = []
  lista = []
  time_limit = [300, 450, 600, 300, 300, 450, 600, 450, 300, 450, 450, 450]
  #Loop through each file and read its contents
  for j in range(len(files)):
    start_time = time.time()
    param_grasp = 4
    param_cam = 11
    param_ruido = (-5,5)
    [car_routes, car_distances, R, Th] = func_VND_mixed(files[j], param_grasp, param_cam, param_ruido, start_time, time_limit[j])
    end_time = time.time()
    run_time = round(end_time - start_time,2)
  
    for i in range(len(car_distances)):
      car_distances[i] = round(car_distances[i], 2)

    distances_vnd.append(round(sum(car_distances),2))    # Add the distance of every instances in distances
    run_vec_vnd.append(run_time)          # Add the run time of every instances in run_vec
    constr = dataFrame(results, Th, car_distances, car_routes, run_time, R)  # Make a data frame with the output data
    lista.append(files[j][16:])
  
  return constr, lista, distances_vnd, run_vec_vnd 

# Read all the folder with each of the instances
folder_path = "mtVRP Instances"
file_extension = ".txt"

#Get a list of all files in the folder with the specified extension
files = glob.glob(os.path.join(folder_path, f"*{file_extension}"))
files.sort()      

# Execute the algorithms
[r_VND, lista, distances_VND, run_vec_VND] = ex_VND(files)
[r_VND_mix, lista, distances_VND_mix, run_vec_mix] = ex_VND_mixed(files)
# Make an excel with the results
to_excel_VND(r_VND, lista)
to_excel_VND_mixed(r_VND_mix, lista)

#cote_dist = [384.48, 515.34, 515.34, 515.34, 585.74, 585.74, 596.49, 658.59, 658.59, 336.44, 395.03, 395.03]
# Plot the solution of the three algorithms
# plt_times(lista, time_constr, time_grasp, time_ruido, run_vec_VND) 
# plt_dist(lista, distances_constr, distances_grasp, distances_ruido, distances_VND, cote_dist)
