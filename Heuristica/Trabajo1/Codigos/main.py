import os
import glob
import time
from Constructive import constructive
from Ruido import noising
from Grasp import grasp
from plot import plt_routes, plt_times, plt_dist
from files import read, to_excel_constr, to_excel_grasp, to_excel_noising, dataFrame

# Constructive algorithm
def ex_constr(files):
  results = []
  distances_constr = []
  run_vec_constr = []
  cote_dist = []
  lista = []
  #Loop through each file and read its contents
  for file_path in files:
    start_time = time.time()        
    [n,Q,R,Th,nodes,request,dist,x,y] = read(file_path)           # Read a single file of the folder mtVRP Instances
    distance_cote = dist

    # Minimun cote
    minimun_cote = 0
    for i in range(len(distance_cote)):
      minimun_cote = minimun_cote + min(distance_cote[i])
    cote_dist.append(minimun_cote)

    [Th_dist, route] = constructive(n,Q,R,Th,nodes,request,dist)  # Execute the constructive algorithm 
    end_time = time.time()
    run_time = round(end_time - start_time,2)

    for i in range(len(Th_dist)):
      Th_dist[i] = round(Th_dist[i], 2)

    distances_constr.append(round(sum(Th_dist),2))    # Add the distance of every instances in distances
    run_vec_constr.append(run_time)          # Add the run time of every instances in run_vec
    constr = dataFrame(results, Th, Th_dist, route, run_time, R)  # Make a data frame with the output data
    lista.append(file_path[16:])
  
  return constr, lista, distances_constr, run_vec_constr, cote_dist

# Noising algorithm
def ex_noising(files):
  results = []
  distances_noising = []
  run_vec_noising = []
  lista = []
  cote_dist = []
  for file_path in files:
    best_route = []
    best_dist = []
    best_time = 0
    total_distance = 1e9
    Th_best = 0
    R_best = 0
    n = 1000
    restric = 1e9
    run_time = 0
    start_time = time.time()   
    [n,Q,R,Th,nodes,request,dist,x,y] = read(file_path)      # Read a single file of the folder mtVRP Instances     
    #Run n times noising and get the best results
    for i in range(n):
      dist_nois = dist.copy()
      a=-1
      b=1
      [Th_dist, route] = noising(n,Q,R,Th,nodes,request,dist_nois,a,b)
      aux = [x > Th for x in Th_dist]
      cons_len = [int(x) if x else 0 for x in aux]

    if(sum(cons_len)<restric and sum(Th_dist)<total_distance):
      restric = sum(cons_len)
      best_route = route
      best_dist = Th_dist
      best_time = run_time
      total_distance = sum(Th_dist)
      Th_best = Th
      R_best = R
    end_time = time.time()
    run_time = round(end_time - start_time,2)
    for i in range(len(best_dist)):
      best_dist[i] = round(best_dist[i], 2)

    distances_noising.append(round(sum(best_dist),2))
    run_vec_noising.append(run_time)
    lista.append(file_path[16:])
    constr = dataFrame(results, Th, best_dist, best_route, run_time, R)
  return constr, lista, distances_noising, run_vec_noising

# Grasp algorithm
def ex_grasp(files):
  results = []
  distances_grasp = []
  lista = []
  run_vec_grasp = []
  for file_path in files:
    best_route = []
    best_dist = []
    best_time = 0
    total_distance = 1e9
    Th = 0
    R = 0
    n = 1000
    restric = 1e9
    run_time = 0
    start_time = time.time()  
    [n1,Q1,R1,Th1,nodes1,request1,dist1,x1,y1] = read(file_path)           # Read a single file of the folder mtVRP Instances
    #Run n times grasp and gets the best results
    for i in range(n): 
      dist_grasp = dist1.copy()
      k = 2
      [Th_dist, route] = grasp(n1,Q1,R1,Th1,nodes1,request1,dist_grasp,k)

      aux = [x > Th1 for x in Th_dist]
      cons_len = [int(x) if x else 0 for x in aux]

    if(sum(cons_len)<restric and sum(Th_dist)<total_distance):
      restric = sum(cons_len)
      best_route = route
      best_dist = Th_dist
      best_time = run_time
      total_distance = sum(Th_dist)
      Th = Th1
      R = R1
    end_time = time.time()
    run_time = round(end_time - start_time,2)

    for i in range(len(best_dist)):
      best_dist[i] = round(best_dist[i], 2)

    distances_grasp.append(round(sum(best_dist),2))    # Add the distance of every instances in distances
    run_vec_grasp.append(run_time)          # Add the run time of every instances in run_vec
    lista.append(file_path[16:])
    constr = dataFrame(results, Th, best_dist, best_route, run_time, R)  # Make a data frame with the output data
  return constr, lista, distances_grasp, run_vec_grasp

# Read all the folder with each of the instances
folder_path = "mtVRP Instances"
file_extension = ".txt"

#Get a list of all files in the folder with the specified extension
files = glob.glob(os.path.join(folder_path, f"*{file_extension}"))
files.sort()      

# Execute the three algorithms
[r_constr, lista, distances_constr, run_vec_constr, cote_dist] = ex_constr(files)
# [r_ruido, lista, distances_noising, run_vec_noising] = ex_noising(files)
# [r_grasp, lista, distances_grasp, run_vec_grasp] = ex_grasp(files)

# Make an excel to store the results
# to_excel_constr(r_constr, lista)
# to_excel_noising(r_ruido, lista)
# to_excel_grasp(r_grasp, lista)

# Plot the solution of the three algorithms
#plt_times(lista, run_vec_constr, run_vec_grasp, run_vec_noising) 
#plt_dist(lista, distances_constr, distances_grasp, distances_noising, cote_dist)

