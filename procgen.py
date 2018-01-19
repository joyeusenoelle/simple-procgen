import random as r
import sys, os
from PIL import Image

def createDungeon(x=None, y=None, seed=None):
	""" Initializes an x by y grid.
		x is width, y is height
		seed is the chance that a given cell will be "live" and should be an integer between 1-99.
		If True is equivalent to "wall", then higher seeds make more walls.
	"""
	x = 10 if x == None else int(x)
	y = 10 if y == None else int(y)
	seed = 45 if seed == None else int(seed)
	new_map = []
	for j in range(y):
		new_row = []
		for i in range(x):
			new_row.append(True if r.randint(1,99) <= seed else False)
		new_map.append(new_row)
	return new_map

def refineDungeon(d_map, d_lmt=None, a_lmt=None):
	""" Refines the grid.
	"""
	d_lmt = 4 if d_lmt == None else int(d_lmt)
	a_lmt = 4 if a_lmt == None else int(a_lmt)
	new_map = []
	for j in range(len(d_map)):
		new_line = []
		for i in range(len(d_map[j])):
			x, y = i, j
			n_count = countAliveNeighbors(d_map, x, y)
			if d_map[y][x]:
				# It's a wall.
				if n_count < d_lmt:
					# It has too few wall neighbors, so kill it.
					new_line.append(False)
				else:
					# It has enough wall neighbors, so keep it.
					new_line.append(True)
			else:
				# It's a path.
				if n_count > a_lmt:
					# It has too many wall neighbors, so it becomes a wall.
					new_line.append(True)
				else:
					# It's not too crowded, so it stays a path.
					new_line.append(False)
		new_map.append(new_line)
	return new_map

def countAliveNeighbors(d_map, x, y):
	count = 0
	for j in range(-1,2):
		for i in range(-1,2):
			n_x, n_y = x+i, y+j
			if i == 0 and j == 0:
				continue
			if n_x < 0 or n_x >= len(d_map[j]) or n_y == 0 or n_y >= len(d_map):
				# The target cell is at the edge of the map and this neighbor is off the edge.
				# So we make this neighbor count as a wall.
				count += 1
				#pass
			elif d_map[n_y][n_x]:
				# This neighbor is on the map and is a wall.
				count += 1
	return count

def printDungeon(d_map, wall=None, path=None):
	wall = "II" if wall == None else wall
	path = "  " if path == None else path
	for line in d_map:
		print("".join([wall if x else path for x in line]))
	print()

def createImage(d_map, color=None, chunky=None, fn=None):
	color = False if color == None else bool(color)
	chunky = False if chunky == None else bool(chunky)
	fn = filename() if fn == None else fn
	x, y = len(d_map[0]), len(d_map)
	if chunky:
		true_x, true_y = x*2, y*2
	else:
		true_x, true_y = x, y
	img = Image.new("RGB",(true_x,true_y),(0,0,0))
	lst = []
	# Walls are black by default
	c_wall = [r.randint(0,255), r.randint(0,255), r.randint(0,255)] if color else [0,0,0]
	# Paths are white by default
	c_space = [255-x for x in c_wall]
	if chunky:
		for line in  d_map:
			for _ in range(2):
				for val in line:
					for _ in range(2):
						lst.append(tuple(c_wall) if val else tuple(c_space))
	else:
		for line in  d_map:
			for val in line:
				lst.append(tuple(c_wall) if val else tuple(c_space))
	img.putdata(lst)
	if not os.path.exists("maps"):
		os.makedirs("maps")
	img.save('maps/{}.png'.format(fn))
	print("Saved maps/{}.png".format(fn))

def filename():
	hexes = ["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"]
	fn = []
	for _ in range(16):
		fn.append(r.choice(hexes))
	return "".join(fn)


def main(x=None, y=None, seed=None, d_lmt=None, a_lmt=None, reps=None, out=None, color=None, chunky=None):
	# Initialize
	x = 20 if x == None else int(x)
	y = 20 if y == None else int(y)
	seed = 45 if seed == None else int(seed)
	d_lmt = 4 if d_lmt == None else int(d_lmt)
	a_lmt = 4 if a_lmt == None else int(a_lmt)
	reps = 2 if reps == None else int(reps)
	out = False if out == None else bool(out)
	color = False if color == None else bool(color)
	chunky = False if chunky == None else bool(chunky)
	my_map = createDungeon(x,y,seed)
	fn = filename()
	for _ in range(reps):
		my_map = refineDungeon(my_map, d_lmt, a_lmt)
	if out:
		createImage(my_map, color, chunky)
	else:
		printDungeon(my_map)

def parseArgs(args):
	flags = {
		"--height" : 20,
		"--width"  : 20,
		"--seed"   : 45,
		"--death"  : 4,
		"--birth"  : 4,
		"--reps"   : 2,
		"--out"    : False,
		"--color"  : False,
		"--chunky" : False,
	}
	for flag, default in flags.items():
		if flag in args:
			if flag == "--out":
				flags["--out"] = True
			elif flag == "--color":
				flags["--color"] = True
			elif flag == "--chunky":
				flags["--chunky"] = True
			else:
				flags[flag] = args[args.index(flag) + 1]
	return flags

if __name__ == "__main__":
	flags = parseArgs(sys.argv)

	main(flags["--width"], 
		 flags["--height"], 
		 flags["--seed"], 
		 flags["--death"], 
		 flags["--birth"], 
		 flags["--reps"],
		 flags["--out"],
		 flags["--color"],
		 flags["--chunky"])