import numpy as np
import random
import time
import copy
np.warnings.filterwarnings('ignore')

def func_obj(sol, distance):
  obj = 0
  for i in range(len(sol)-1):
    obj += distance[int(sol[i])][int(sol[i+1])]
  return obj

def func_obj_two(ruta1, ruta2, distance):
  obj1 = 0
  obj2 = 0
  for i in range(len(ruta1)-1):
    obj1 += distance[ruta1[i]][ruta1[i+1]]
  for i in range(len(ruta2)-1):
    obj2 += distance[ruta2[i]][ruta2[i+1]]
  return obj1, obj2

def check_capacity(ruta1, ruta2, request, Q):
  found = False
  count1 = 0
  count2 = 0
  for i in range(len(ruta1)):
    count1 += request[ruta1[i]]
  for i in range(len(ruta2)):
    count2 += request[ruta2[i]]
  if(count1<=Q and count2<=Q):
    found = True
  return found

# Neighborhoods
def two_opt_ruido(sol, obj, distance, param_ruido):
  best_dist_opt = obj
  solution_opt = sol.copy()
  solutions = []

  if(len(sol)<=3):
    return solution_opt, best_dist_opt

  for i in range(1,len(sol)-1):
    for j in range(i+1,len(sol)-1):
      temp_sol = sol.copy()
      temp_sol[i:j+1] = np.flip(sol[i:j+1])

      curr_dist_opt = func_obj(temp_sol, distance)
      a = param_ruido[0]
      b = param_ruido[1]
      curr_dist_noising = curr_dist_opt + random.uniform(a,b)
      solutions.append((curr_dist_noising, curr_dist_opt, temp_sol))

  order_sol = sorted(solutions, key=lambda x: x[0])
  best_dist_opt = order_sol[0][1]
  solution_opt = order_sol[0][2]

  return solution_opt, best_dist_opt

def insertion(rutas, dist_rutas, request, m_distances, Q):
  sol_ins = copy.deepcopy(rutas)
  best_dist_ins = copy.deepcopy(dist_rutas)
  
  for ruta in range(len(rutas)):
    if(len(rutas[ruta])>3):
      for i in range(1, len(rutas[ruta])-1):
        nodo = rutas[ruta][i]
        for otra_ruta in range(1, len(rutas)):
          if rutas[otra_ruta] is not rutas[ruta]:
            for j in range(1, len(rutas[otra_ruta])):
              sub_ruta = copy.deepcopy(rutas)
              sub_ruta[ruta] = np.delete(rutas[ruta], i)
              sub_ruta[otra_ruta] = np.insert(sub_ruta[otra_ruta],j,nodo)
              # Primero chequear que sea factible
              found = check_capacity(sub_ruta[ruta], sub_ruta[otra_ruta], request, Q)
              # Si es factible calculo la distancia total de las rutas
              if(found):
                distancia_nueva = copy.deepcopy(dist_rutas)
                [dist1, dist2] = func_obj_two(sub_ruta[ruta], sub_ruta[otra_ruta], m_distances)
                distancia_nueva[ruta] = dist1
                distancia_nueva[otra_ruta] = dist2

                if sum(distancia_nueva) < sum(best_dist_ins):
                  best_dist_ins = distancia_nueva
                  sol_ins = sub_ruta
          else:
            for j in range(i+1,len(rutas[ruta])-1):
              sub_ruta = copy.deepcopy(rutas)
              sub_ruta[ruta] = np.delete(rutas[ruta], i)
              sub_ruta[ruta] = np.insert(sub_ruta[ruta],j,nodo)

              distancia_nueva = copy.deepcopy(dist_rutas)
              dist1 = func_obj(sub_ruta[ruta], m_distances)
              distancia_nueva[ruta] = dist1

              if sum(distancia_nueva) < sum(best_dist_ins):
                best_dist_ins = distancia_nueva
                sol_ins = sub_ruta

  return sol_ins, best_dist_ins

def exchange(rutas, dist_rutas, request, m_distances, Q):
  solution_exc = copy.deepcopy(rutas)
  best_dist_exc = copy.deepcopy(dist_rutas)
  
  for ruta in range(len(rutas)):
    for i in range(1, len(rutas[ruta])-1):
      for otra_ruta in range(ruta, len(rutas)):
        if rutas[otra_ruta] is not rutas[ruta]:
          for j in range(1, len(rutas[otra_ruta])-1):
            sub_ruta = copy.deepcopy(rutas)
            aux = sub_ruta[ruta][i]
            sub_ruta[ruta][i] = sub_ruta[otra_ruta][j]
            sub_ruta[otra_ruta][j] = aux
            
            # Primero revisar que sea factible
            found = check_capacity(sub_ruta[ruta], sub_ruta[otra_ruta], request, Q)
            # Si es factible calculo la distancia total de las rutas
            if(found):
              distancia_nueva = copy.deepcopy(dist_rutas)
              [dist1, dist2] = func_obj_two(sub_ruta[ruta], sub_ruta[otra_ruta], m_distances)
              distancia_nueva[ruta] = dist1
              distancia_nueva[otra_ruta] = dist2

              if sum(distancia_nueva) < sum(best_dist_exc):
                best_dist_exc = distancia_nueva
                solution_exc = sub_ruta
        else:
          for j in range(i+1,len(rutas[ruta])-1):
            sub_ruta = copy.deepcopy(rutas)
            aux = sub_ruta[ruta][i]
            sub_ruta[ruta][i] = sub_ruta[ruta][j]
            sub_ruta[ruta][j] = aux

            distancia_nueva = copy.deepcopy(dist_rutas)
            dist1 = func_obj(sub_ruta[ruta], m_distances)
            distancia_nueva[ruta] = dist1

            if sum(distancia_nueva) < sum(best_dist_exc):
              best_dist_exc = distancia_nueva
              solution_exc = sub_ruta
  return solution_exc, best_dist_exc

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
def neighborhood(route, distances, request, R, Q, neighborhood_type, param_ruido): #x debe ser un numpy array
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
    [best_route, best_fo] = insertion(route, obj, request, distances, Q)
    optimal_pair = list(zip(best_fo, best_route))
  # If the neighborhood type is 3, then we will apply exchange
  else:
    [best_route, best_fo] = exchange(route, obj, request, distances, Q)
    optimal_pair = list(zip(best_fo, best_route))
  
  [car_routes, car_distances] = assign_routes(optimal_pair,R)
  return car_routes, car_distances

def educate(child, start_time, time_limit):   #max_iter es el numero de vecindarios
  solution = child[1]
  best_Th = child[2]
  dist = child[3]
  request = child[4]
  R = child[5]
  Th = child[6]
  Q = child[7]

  aux_init = [x > Th for x in best_Th]
  cons_len_init = [int(x) if x else 0 for x in aux_init]
  rest_Th = sum(cons_len_init)
  best_fo = sum(best_Th)
  neigh_type = 1
  param_ruido = (-5,5)
  n = 3
  
  while((time.time()-start_time)<time_limit and neigh_type <= n):
    [neighbor, neigh_Th_dist] = neighborhood(solution, dist, request, R, Q, neigh_type, param_ruido)
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

  new_child = [sum(best_Th), solution, best_Th, dist, request, R, Th, Q]
  return new_child

