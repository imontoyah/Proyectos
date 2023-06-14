import copy
import random
import time
import numpy as np
from itertools import chain
from Solutions import ex_ruido
from VND import process_route, assign_routes, educate

# Initialize population with n members
def initialization(file_path, param, n):
  population = []
  for i in range(n):
    [initial_route, initial_dist, dist, request, R, Th, Q, timer] = ex_ruido(file_path, param)
    population.append((sum(initial_dist), initial_route, initial_dist, dist, request, R, Th, Q))
  return population

def fun_obj2(route, distance):
  Th_dist = []
  for i in range(len(route)):
    dist = 0
    for j in range(len(route[i])-1):
      dist += distance[route[i][j]][route[i][j+1]]
    Th_dist.append(dist)
  return Th_dist

def check_capacity_pert(ruta1, ruta2, request, Q, found):
  count1 = 0
  count2 = 0
  for i in range(len(ruta1)):
    count1 += request[ruta1[i]]
  for i in range(len(ruta2)):
    count2 += request[ruta2[i]]
  if(count1<=Q and count2<=Q):
    found = True
  return found

# Function that make the mutation in the child
def perturbation(sol, Th_dist, request, distances, Q, num_cam):
  while(True):
    sol_mutate = copy.deepcopy(sol)
    parejas=[]
    found = True
    for i in range(num_cam):
      a=random.randint(1,len(sol)-2)
      b=random.randint(1,len(sol[a])-2)
      parejas.append((a,b))

    for i in range(len(parejas)):
      aux = sol_mutate[parejas[i][0]][parejas[i][1]] 
      sol_mutate[parejas[i][0]][parejas[i][1]] = sol_mutate[parejas[(i+1)%len(parejas)][0]][parejas[(i+1)%len(parejas)][1]]
      sol_mutate[parejas[(i+1)%len(parejas)][0]][parejas[(i+1)%len(parejas)][1]] = aux
      found = found and check_capacity_pert(sol_mutate[parejas[i][0]], sol_mutate[parejas[(i+1)%len(parejas)][0]], request, Q, found)

    if(found):
      sol_Th_dist =  fun_obj2(sol_mutate, distances)
      break
  return sol_mutate, Th_dist

# Select the parents of the child
def select_parent(pob):
  num = list(range(0, len(pob)))
  parents = random.sample(num, 4)
  parent1_1 = pob[parents[0]]
  parent1_2 = pob[parents[1]]
  parent2_1 = pob[parents[2]]
  parent2_2 = pob[parents[3]]

  if(parent1_1[0]<parent1_2[0]):
    parent1 = parent1_1
  else:
    parent1 = parent1_2

  if(parent2_1[0]<parent2_2[0]):
    parent2 = parent2_1
  else:
    parent2 = parent2_2

  return parent1, parent2

def assign_depo(route, request, Q, dist):
  new_route =  [0, route[0]]
  Q_act = request[route[0]]
  route.remove(route[0])
  while(len(route)>0):
    if(Q_act+request[route[0]]<Q):
      new_route.append(route[0])
      Q_act = Q_act + request[route[0]]
      route.remove(route[0])
    else:
      new_route.append(0)
      Q_act = 0
  new_route.append(0)

  sublistas = []
  sublista_actual = [0]
  for elemento in new_route:
    if elemento != 0:
      sublista_actual.append(elemento)
    else:
      if len(sublista_actual)>1:
        sublista_actual.append(0)
        sublistas.append(np.array(sublista_actual))
        sublista_actual = [0]

  if len(sublista_actual)>1:
    sublistas.append(0)
    sublistas.append(np.array(sublista_actual))
  
  dist_child1 = fun_obj2(sublistas, dist)
  resultado = list(zip(dist_child1, sublistas))

  return resultado

# Crossover parent and parent2 to get a new route
def crossover(parent1, parent2):
  Q = parent1[7]
  R = parent1[5]
  dist = parent1[3]
  request = parent1[4]
  [route_p1, dist_p1] = process_route(parent1[1], parent1[3])
  [route_p2, dist_p2] = process_route(parent2[1], parent2[3])
  
  p1_wcero = list(chain.from_iterable(route_p1))
  p2_wcero = list(chain.from_iterable(route_p2))

  # Delete the zeros in the list
  p1 = [nodo for nodo in p1_wcero if nodo != 0]
  p2 = [nodo for nodo in p2_wcero if nodo != 0]

  i = int(len(p1)/8)
  j = int(len(p2)/2)
  # Make a list full of -1, and set i:j of child_i equal to parent_i
  child1_route = [-1] * len(p1)
  child2_route = [-1] * len(p2)
  child1_route[i:j] = p1[i:j]
  child2_route[i:j] = p2[i:j]

  faltantes1 = []
  faltantes2 = []
  for k in range(len(p1)):
    if(p2[k] not in child1_route):
      faltantes1.append(p2[k])
    if(p1[k] not in child2_route):
      faltantes2.append(p1[k])
  
  # Add the resting nodes to the child
  child1_route[0:i] = faltantes1[0:i]
  child1_route[j:] = faltantes1[i:]
  child2_route[0:i] = faltantes2[0:i]
  child2_route[j:] = faltantes2[i:]

  # Assign the depot(zeros) to the child
  new_child1 = assign_depo(child1_route, request, Q, dist)
  new_child2 = assign_depo(child2_route, request, Q, dist)

  # Assign the routes to each car
  [ruta1, dist1] = assign_routes(new_child1, R)
  [ruta2, dist2] = assign_routes(new_child2, R)

  # Check which child is better to keep
  if(sum(dist1)<sum(dist2)):
    child_final = [sum(dist1), ruta1, dist1, dist, request, R, parent1[6], Q]
  else:
    child_final = [sum(dist2), ruta2, dist2, dist, request, R, parent1[6], Q]
  
  return parent1

# Function to mutate the child, making param_num exchange in the route
def mutate(child, param_num):
  route = child[1]
  distances = child[3]
  request = child[4]
  R = child[5]
  Th = child[6]
  Q = child[7]

  # The mutation will be a perturbation
  [route, obj] = process_route(route,distances)
  [best_route, best_fo] = perturbation(route, obj, request, distances, Q, param_num)
  optimal_pair = list(zip(best_fo, best_route))
  [car_routes, car_distances] = assign_routes(optimal_pair,R)

  new_child = [sum(car_distances), car_routes, car_distances, distances, request, R, Th, Q]
  return new_child

# Select the better individuals to survive
def select_survivors(pob, limit_pob):
  pob_ordenada = sorted(pob, key=lambda x: x[0])
  new_pob = pob_ordenada[:limit_pob]
  return new_pob

# Execute the genetic algorithm
def ex_AG(file_path, start_time, time_limit):
  limit_pob = 100
  param_ruido = (-1,1)
  pob = initialization(file_path, param_ruido, 30)

  while((time.time()-start_time)<time_limit):
    [p1, p2] = select_parent(pob)
    child = crossover(p1,p2)

    prob = random.random()
    if prob < 0.1:
      num_cam = 5
      child = mutate(child, num_cam)
    new_child = educate(child, start_time, time_limit)
    pob.append(new_child)

    if(len(pob)>limit_pob):
      pob = select_survivors(pob, limit_pob)
  pob_ord = sorted(pob, key=lambda x: x[0])
  best_ind = pob_ord[0]

  return best_ind