import numpy as np
import random

def grasp(n,Q,R,Th,nodes,request,dist,k):
  #Initialize variables
  Th_dist = []
  route = []
  Q_route = []
  visited = {i for i in range(1,n+1)}
  M = 1e9
  
  # For the cars available, it will chose its near node and visit it 
  # until it reach the Th established
  for i in range(R):
    pos = int(nodes[0])
    Q_act = Q
    car_route =[0]
    accum = 0

    while(accum<Th):
      [dist_near, node_near] = check_distance(n, accum, dist, request, Q_act, pos, Th, k)
      if(dist_near == -1 and node_near == -1):
        break
      else:
        # If the node that I found is equal to my actual position means that 
        # I don´t have the capacity to sastifies any node so I have to return to the deposit
        if(node_near == pos):
          if(pos == 0):
            break
          #Update variables
          car_route.append(0)    # Add the deposit to that car route
          accum += dist[pos,0]   # Sum the distance traveled
          Q_act = Q             
          pos = 0                
        else: # Otherwise I can visited the nearest node
          Q_act = Q_act - request[node_near]   
          car_route.append(node_near)   # Add the nearest node to that car route
          visited.remove(node_near)     # Remove the node visited
          accum += dist_near            # Sum the distance traveled
          dist[:, node_near] = M       
          pos = node_near   
    Q_route.append(Q_act)        
    Th_dist.append(accum)     # Add the distance traveled by car i
    route.append(car_route)   # Add the route made by car i

  [Th_dist, route] = check_visited(visited, Th_dist, route, dist, request, Q_route, Q, M, Th, n, k)
  [Th_dist, route] = check_depo(R,route, Th_dist, dist)
  return Th_dist, route

def check_distance(n, accum, dist, request, Q_act, pos, Th, k):
  selected = []
  dist_near = dist[pos,pos]  # Set dist_near to a very large number 
  node_near = pos

  for i in range(1,n+1):    
    if(dist[pos,i]<dist_near and request[i]<=Q_act):
      selected.append((dist[pos,i],i))

  if not selected:
    dist_near = -1
    node_near = -1
  else:
    selected.sort(reverse=False)
    if(k<=len(selected)):
      k_nodes = selected[:k]
      random_node = random.choice(k_nodes)
      dist_near = random_node[0]
      node_near =  random_node[1]
    else:
      k_nodes = selected
      random_node = random.choice(k_nodes)
      dist_near = random_node[0]
      node_near =  random_node[1]
  # if node_near == pos:
  #   dist_near = -1
  #   node_near = -1

  return dist_near, node_near

# Function to verify that all the nodes have been visited
def check_visited(visited, Th_dist, route, dist, request, Q_route, Q, M, Th, n, k):
  while(len(visited)>0):
    min_time = min(Th_dist)
    min_car = Th_dist.index(min_time)  # Index of the car with minimum Th
    pos = route[min_car][-1]           # The node in which the car with minimum Th is        

    [dist_near, node_near] = check_distance(n, Th_dist[min_car], dist, request, Q_route[min_car], pos, Th, k)
    if((dist_near == -1 and node_near == -1) or (node_near == pos)):
      if(pos==0):
        break
      route[min_car].append(0)          # Add the deposit to the route of min_car
      Th_dist[min_car] += dist[pos,0]   # Sum the distance traveled
      Q_route[min_car] = Q
      pos = 0              
    else: # Otherwise I can visited the nearest node
      Q_route[min_car] = Q_route[min_car] - request[node_near]
      route[min_car].append(node_near)  # Add the nearest node to the route of min_car
      visited.remove(node_near)         # Remove the node visited        
      Th_dist[min_car] += dist_near     # Sum the distance traveled
      dist[:, node_near] = M    
      pos = node_near   
    
  return Th_dist, route

#Function to check if all the cars returned to the deposit
def check_depo(R,route,Th_dist,dist):
  for i in range(R):
    if(route[i][-1]!=0):
      Th_dist[i] += dist[route[i][-1],0]
      route[i].append(0)
  return Th_dist, route




