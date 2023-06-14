import numpy as np
import random
import copy 

def func_obj(sol, distance):
  obj = 0
  for i in range(len(sol)-1):
    obj += distance[int(sol[i])][int(sol[i+1])]
  return obj

def fun_obj2(route, distance):
  Th_dist = []
  for i in range(len(route)):
    dist = 0
    for j in range(len(route[i])-1):
      dist += distance[route[i][j]][route[i][j+1]]
  Th_dist.append(dist)
  return Th_dist

def func_obj_two(ruta1, ruta2, distance):
  obj1 = 0
  obj2 = 0
  for i in range(len(ruta1)-1):
    obj1 += distance[ruta1[i]][ruta1[i+1]]
  for i in range(len(ruta2)-1):
    obj2 += distance[ruta2[i]][ruta2[i+1]]
  return obj1, obj2

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

def two_opt(sol, obj, distance):
  best_dist_opt = obj
  solution_opt = sol.copy()

  if(len(sol)<=3):
    return solution_opt, best_dist_opt

  for i in range(1,len(sol)-1):
    for j in range(i+1,len(sol)-1):
      temp_sol = sol.copy()
      temp_sol[i:j+1] = np.flip(sol[i:j+1])
      
      curr_dist_opt = func_obj(temp_sol, distance)

      if(curr_dist_opt<best_dist_opt):
        best_dist_opt = curr_dist_opt
        solution_opt = temp_sol
        
  return solution_opt, best_dist_opt

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