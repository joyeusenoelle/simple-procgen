import random as r
import sys
from PIL import Image

def createDungeon(x=None, y=None, seed=None):
	""" Initializes an x by y grid.
		x is width, y is height
		seed is the chance that a given cell will be "live" and should be an integer between 1-99.
		If True is equivalent to "walkable", then lower seeds make more walls.
	"""
	x = 10 if x == None else int(x)
	y = 10 if y == None else int(y)
	seed = 45 if seed == None else int(seed)
	new_map = []
	for j in range(y):
		new_row = []
		for i in range(x):
			new_row.append(False if r.randint(1,99) > seed else True)
		new_map.append(new_row)
	return new_map

def refineDungeon(d_map, d_lmt=None, a_lmt=None):
	""" Refines the grid.
	"""
	d_lmt = 3 if d_lmt == None else int(d_lmt)
	a_lmt = 4 if a_lmt == None else int(a_lmt)
	new_map = []
	for j in range(len(d_map)):
		new_line = []
		for i in range(len(d_map[j])):
			x, y = i, j
			n_count = countAliveNeighbors(d_map, x, y)
			if d_map[y][x]:
				if n_count <= d_lmt:
					new_line.append(False)
				else:
					new_line.append(True)
			else:
				if n_count >= a_lmt:
					new_line.append(True)
				else:
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
				count += 1
			elif d_map[n_y][n_x]:
				count += 1
	return count

def printDungeon(d_map, wall=None, path=None):
	wall = "II" if wall == None else wall
	path = "  " if path == None else path
	for line in d_map:
		print("".join([wall if x == True else path for x in line]))
	print()

def main(x=None, y=None, seed=None, d_lmt=None, a_lmt=None, reps=None, out=None):
	# Initialize
	x = 20 if x == None else int(x)
	y = 20 if y == None else int(y)
	seed = 45 if seed == None else int(seed)
	d_lmt = 4 if d_lmt == None else int(d_lmt)
	a_lmt = 4 if a_lmt == None else int(a_lmt)
	reps = 2 if reps == None else int(reps)
	out = False if out == None else bool(out)
	my_map = createDungeon(x,y,seed)
	if not out:
		printDungeon(my_map)
	for _ in range(reps):
		my_map = refineDungeon(my_map, d_lmt, d_lmt)
		if not out:
			printDungeon(my_map)
	if out:
		img = Image.new("RGB",(x,y),(0,0,0))
		lst = []
		for line in my_map:
			for val in line:
				lst.append((0,0,0) if val else (255,255,255))
		img.putdata(lst)
		hexes = ["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"]
		filename = []
		for _ in range(16):
			filename.append(r.choice(hexes))
		img.save('maps/{}.png'.format("".join(filename)))
		print("Saved maps/{}.png".format("".join(filename)))

def parseArgs(args):
	flags = {
		"--height" : 20,
		"--width"  : 20,
		"--seed"   : 45,
		"--death"  : 4,
		"--birth"  : 4,
		"--reps"   : 2,
		"--out"    : False
	}
	for flag, default in flags.items():
		if flag in args:
			if flag == "--out":
				flags["--out"] = True
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
		 flags["--out"])