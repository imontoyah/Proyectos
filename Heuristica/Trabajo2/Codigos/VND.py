import numpy as np
import time
from Solutions import ex_ruido, ex_grasp
from neighborhood import two_opt, two_opt_ruido, insertion, exchange, perturbation
np.warnings.filterwarnings('ignore')

# Process the initial solution to obtain a list of numpy arrays of each route of the multitrip problem
def process_route(routes, distance):
  vectores = []
  dist_total = []
  for route in routes:
    vector = [0]
    for i in range(len(route)):
      if route[i] == 0:
        if i != 0 and i != len(route)-1:
          vector.append(0)
          vectores.append(np.array(vector))
          vector = [0]
      else:
        vector.append(route[i])
    if vector:
      vector.append(0)
      vectores.append(np.array(vector))
  
  for i in range(len(vectores)):
    dist_route = []
    for j in range(len(vectores[i])-1):
      dist_route.append(distance[vectores[i][j]][vectores[i][j+1]])
    dist_total.append(sum(dist_route))
  
  return vectores, dist_total

# Assign which car is going to do each route 
def assign_routes(duplas_ordenadas, R):
  # Divide the list in R equal parts 
  partes = np.array_split(duplas_ordenadas, R)
  rutas = []
  distancias = []
  for parte in partes:
    # Create a route for each car, that consists of the concatenation of several routes
    ruta = np.concatenate([d[1][:-1] for d in parte] + [np.array([0])])
    distancia = sum([d[0] for d in parte])

    rutas.append(ruta)
    distancias.append(distancia)
  return rutas, distancias

# This function will return the route and the total distance of each car
def neighborhood(route, distances, request, R, Q, neighborhood_type): #x debe ser un numpy array
  [route, obj] = process_route(route,distances)
  optimal_pair = []
  # If the neighborhood type is 1, then we will apply 2-opt
  if neighborhood_type == 1:
    for i in range(len(route)):
      [best_sub_route, best_sub_fo] = two_opt(route[i], obj[i], distances)
      element = (best_sub_fo, best_sub_route)
      optimal_pair.append(element)
  # If the neighborhood type is 2, then we will apply insertion
  elif neighborhood_type == 2:
    [best_route, best_fo] = insertion(route, obj, request, distances, Q)
    optimal_pair = list(zip(best_fo, best_route))
  # If the neighborhood type is 3, then we will apply exchange
  else:
    [best_route, best_fo] = exchange(route, obj, request, distances, Q)
    optimal_pair = list(zip(best_fo, best_route))
  
  [car_routes, car_distances] = assign_routes(optimal_pair,R)
  return car_routes, car_distances

# This function will return the route and the total distance of each car
def neighborhood_mixed(route, distances, request, R, Q, neighborhood_type, param_num, param_ruido): #x debe ser un numpy array
  [route, obj] = process_route(route,distances)
  optimal_pair = []
  # If the neighborhood type is 1, then we will apply 2-opt
  if neighborhood_type == 1:
    for i in range(len(route)):
      [best_sub_route, best_sub_fo] = two_opt_ruido(route[i], obj[i], distances, param_ruido)
      element = (best_sub_fo, best_sub_route)
      optimal_pair.append(element)
  # If the neighborhood type is 2, then we will apply insertion
  elif neighborhood_type == 2:
    [best_route, best_fo] = perturbation(route, obj, request, distances, Q, param_num)
    optimal_pair = list(zip(best_fo, best_route))
  # If the neighborhood type is 3, then we will apply exchange
  else:
    [best_route, best_fo] = insertion(route, obj, request, distances, Q)
    optimal_pair = list(zip(best_fo, best_route))
  
  [car_routes, car_distances] = assign_routes(optimal_pair,R)
  return car_routes, car_distances

def func_VND(file_path, param, start_time, time_limit):   #max_iter es el numero de vecindarios
  [initial_route, initial_dist, dist, request, R, Th, Q, timer] = ex_ruido(file_path, param)
  solution = initial_route
  best_Th = initial_dist
  aux_init = [x > Th for x in initial_dist]
  cons_len_init = [int(x) if x else 0 for x in aux_init]
  rest_Th = sum(cons_len_init)
  best_fo = sum(initial_dist)
  neigh_type = 1
  n = 3
  
  while((time.time()-start_time)<time_limit and neigh_type <= n):
    [neighbor, neigh_Th_dist] = neighborhood(solution, dist, request, R, Q, neigh_type)
    neigh_aux = [x > Th for x in neigh_Th_dist]
    cons_len_neigh = [int(x) if x else 0 for x in neigh_aux]

    if(sum(neigh_Th_dist) < best_fo and sum(cons_len_neigh)<=rest_Th): 
      solution = neighbor
      best_Th = neigh_Th_dist
      rest_Th = sum(cons_len_neigh)
      best_fo = sum(neigh_Th_dist)

      neigh_type = 1
    else:
        neigh_type += 1
  
  return solution, best_Th, R, Th

def func_VND_mixed(file_path, param_grasp, param_num, param_ruido, start_time, time_limit):   
  sol_final = []
  while((time.time()-start_time)<time_limit):
    [initial_route, initial_dist, dist, request, R, Th, Q, timer] = ex_grasp(file_path, param_grasp)
    solution = initial_route
    best_Th = initial_dist
    aux_init = [x > Th for x in best_Th]
    cons_len_init = [int(x) if x else 0 for x in aux_init]
    rest_Th = sum(cons_len_init)
    best_fo = sum(best_Th)
    neigh_type = 1
    n = 3
    while((time.time()-start_time)<time_limit and neigh_type <= n):
      [neighbor, neigh_Th_dist] = neighborhood_mixed(solution, dist, request, R, Q, neigh_type, param_num, param_ruido)
      neigh_aux = [x > Th for x in neigh_Th_dist]
      cons_len_neigh = [int(x) if x else 0 for x in neigh_aux]

      if(sum(neigh_Th_dist) < best_fo and sum(cons_len_neigh)<=rest_Th): 
        solution = neighbor
        best_Th = neigh_Th_dist
        rest_Th = sum(cons_len_neigh)
        best_fo = sum(neigh_Th_dist)

        neigh_type = 1
      else:
          neigh_type += 1
    sol_final.append((sum(best_Th), best_Th, solution))
  duplas_ordenadas = sorted(sol_final, key=lambda x: x[0])
  dist_Th = duplas_ordenadas[0][1]
  final_solution = duplas_ordenadas[0][2]

  return final_solution, dist_Th, R, Th


