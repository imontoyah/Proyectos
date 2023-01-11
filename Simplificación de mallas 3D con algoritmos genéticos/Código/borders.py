#Clase punto con coordenadas x y y
class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y

#Encuentra el punto más a la izquierda
def Left_index(points):
	minn = 0
	for i in range(1,len(points)):
		if points[i].x < points[minn].x:
			minn = i
		elif points[i].x == points[minn].x:
			if points[i].y > points[minn].y:
				minn = i
	return minn

#Encuentra la orientación de 3 puntos dados (horario, antihorario, colineales)
def orientation(p, q, r):
	val = (q.y - p.y) * (r.x - q.x) - \
		(q.x - p.x) * (r.y - q.y)

	if val == 0:
		return 0
	elif val > 0:
		return 1
	else:
		return 2

#Encuentra la envolvente convexa de un conjunto de puntos
def convexHull(points, n):
	if n < 3:
		return

	l = Left_index(points)

	hull = []
	
	p = l
	q = 0

	while(True):
		hull.append(p)

		q = (p + 1) % n

		for i in range(n):
			if(orientation(points[p],
						points[i], points[q]) == 2):
				q = i

		p = q

		if(p == l):
			break

	return hull

# Código tomado de:
# Convex Hull | Set 1 (Jarvis’s Algorithm or Wrapping), GeeksForGeeks, 2022 [En línea]. Disponible en:
# https://www.geeksforgeeks.org/convex-hull-set-1-jarviss-algorithm-or-wrapping/ 