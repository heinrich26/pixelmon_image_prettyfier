import sys
import math

def pixelate(Ax, Ay, Bx, By):
	global resolution
	# 45 degr
	if max(Ax, Bx) - min(Ax, Bx) and max(Ay, By) - min(Ay, By):
		print("45 degr case")
		y = {}
		m = (Ax - Bx) / (Ay - By)
		for x in range(math.floor(min(Ax, Bx) * resolution), math.ceil(max(Ax, Bx) * resolution) + 1):
			y[x] = int(m * (x - math.floor(Ax * resolution)) + math.floor(Ay * resolution))
		print(y)
	elif Ay == By:
		print("horrizontal case")
		y = {x:math.floor(Ay * resolution) for x in range(math.floor(min(Ax, Bx) * resolution), math.ceil(max(Ax, Bx) * resolution) + 1)}



		print(y)
	elif  Ax == Bx:
		print("vertical case")


resolution = int(input("Enter a image res: "))
Ax, Ay = 0.2, 0.9
Bx, By = 1, 0.1
Cx, Cy = 0.75, 0.75

# while not 0 <= Ax <= 1:
# 	try:
# 		Ax = float(input("Enter Point Ax: "))
# 	except:
# 		pass
# while not 0 <= Ay <= 1:
# 	try:
# 		Ay = float(input("Enter Point Ay: "))
# 	except:
# 		pass
# while not 0 <= Bx <= 1:
# 	try:
# 		Bx = float(input("Enter Point Bx: "))
# 	except:
# 		pass
# while not 0 <= By <= 1:
# 	try:
# 		By = float(input("Enter Point By: "))
# 	except:
# 		pass
# while not 0 <= Cx <= 1:
# 	try:
# 		Cx = float(input("Enter Point Cx: "))
# 	except:
# 		pass
# while not 0 <= Cy <= 1:
# 	try:
# 		Cy = float(input("Enter Point Cy: "))
# 	except:
# 		pass

Ay = 1.0 - Ay
By = 1.0 - By
Cy = 1.0 - Cy

pixelate(Ax, Ay, Bx, By)
pixelate(Ax, Ay, Cx, Cy)
pixelate(Cx, Cy, Bx, By)

