import random, sys, os
from PIL import Image

class CellMap:
	initial = []
	genmap = []

	def __init__(self, height=None, width=None, seed=None, death=None, 
				 birth=None, reps=0, out=None, color=None, chunky=None, 
				 treasure=None):
		self.height = height if height != None else 0
		self.width = width if width != None else 0
		self.seed = seed if seed != None else 0
		self.death = death if death != None else 0
		self.birth = birth if birth != None else 0
		self.reps = reps if reps != None else 0
		self.out = out if out != None else False
		self.color = color if color != None else False
		self.chunky = chunky if chunky != None else False
		self.treasure = treasure if treasure != None else False
		self.id = filename()

	@property
	def height(self):
		return self.__height

	@height.setter
	def height(self, height):
		self.__height = int(height) if int(height) > 0 else 0

	@property
	def width(self):
		return self.__width

	@width.setter
	def width(self, width):
		self.__width = int(width) if int(width) > 0 else 0

	@property
	def seed(self):
		return self.__seed

	@ seed.setter
	def  seed(self, seed):
		self.__seed = int(seed) if int(seed) > 0 else 0

	@property
	def death(self):
		return self.__death

	@death.setter
	def death(self, death):
		self.__death = int(death) if int(death) > 0 else 0

	@property
	def birth(self):
		return self.__birth

	@birth.setter
	def birth(self, birth):
		self.__birth = int(birth) if int(birth) > 0 else 0

	@property
	def reps(self):
		return self.__reps

	@reps.setter
	def reps(self, reps):
		self.__reps = int(reps) if int(reps) > 0 else 0

	@property
	def out(self):
		return self.__out

	@out.setter
	def out(self, out):
		self.__out = bool(out)

	@property
	def color(self):
		return self.__color

	@color.setter
	def color(self, color):
		self.__color = bool(color)

	@property
	def chunky(self):
		return self.__chunky

	@chunky.setter
	def chunky(self, chunky):
		self.__chunky = bool(chunky)

	@property
	def treasure(self):
		return self.__treasure

	@treasure.setter
	def treasure(self, treasure):
		self.__treasure = bool(treasure)

	def generateFullMap(self):
		""" Puts everything together.
		"""
		self.createMap()
		for _ in range(self.reps):
			self.smoothMap()
		if self.out:
			self.createImage()
		else:
			self.printScreen()	

	def createMap(self):
		""" Initializes an x by y grid.
			x is width, y is height
			seed is the chance that a given cell will be "live" and should be an integer between 1-99.
			If True is equivalent to "wall", then higher seeds make more walls.
		"""
		if self.__height == 0 or self.__width == 0 or self.__seed == 0:
			print("Height, width, and seed must be set before creating a map.")
			print("Current values: height: {}, width: {}, seed: {}".format(self.height, self.width, self.seed))
			return
		y = self.height
		x = self.width
		seed = self.seed
		new_map = []
		for j in range(y):
			new_row = []
			for i in range(x):
				new_row.append(True if random.randint(1,99) <= seed else False)
			new_map.append(new_row)
		self.initial = new_map
		self.genmap = self.initial

	def smoothMap(self):
		""" Refines the grid.
		"""
		if self.death == 0 or self.birth == 0:
			print("The 'death' limit is currently {} and the 'birth' limit is {}.".format(self.death,self.birth))
			print("Smoothing with the 'death' or 'birth' limit set to 0 is not recommended.")
			print("Do you want to proceed? (y/N) ", end="")
			cont = input().strip()
			if cont.lower() != "y":
				print("Aborting.")
				return
		d_lmt = self.death
		a_lmt = self.birth
		new_map = []
		for j in range(len(self.genmap)):
			new_line = []
			for i in range(len(self.genmap[j])):
				x, y = i, j
				n_count = self.countWalls(x, y)
				if self.genmap[y][x]:
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
		self.genmap = new_map

	def countWalls(self, x, y):
		count = 0
		for j in range(-1,2):
			for i in range(-1,2):
				n_x, n_y = x+i, y+j
				if i == 0 and j == 0:
					continue
				if n_x < 0 or n_x >= len(self.genmap[j]) or n_y == 0 or n_y >= len(self.genmap):
					# The target cell is at the edge of the map and this neighbor is off the edge.
					# So we make this neighbor count as a wall.
					count += 1
					#pass
				elif self.genmap[n_y][n_x]:
					# This neighbor is on the map and is a wall.
					count += 1
		return count

	def printScreen(self):
		wall = "II"
		path = "  "
		for line in self.genmap:
			print("".join([wall if x else path for x in line]))
		print()

	def createImage(self):
		x, y = len(self.genmap[0]), len(self.genmap)
		if self.chunky:
			true_x, true_y = x*2, y*2
		else:
			true_x, true_y = x, y
		img = Image.new("RGB",(true_x,true_y),(0,0,0))
		lst = []
		# Walls are black by default
		c_wall = [random.randint(0,255), random.randint(0,255), random.randint(0,255)] if self.color else [0,0,0]
		# Paths are white by default
		c_space = [255-x for x in c_wall]
		if self.chunky:
			for line in self.genmap:
				for _ in range(2):
					for val in line:
						for _ in range(2):
							lst.append(tuple(c_wall) if val else tuple(c_space))
		else:
			for line in self.genmap:
				for val in line:
					lst.append(tuple(c_wall) if val else tuple(c_space))
		img.putdata(lst)
		if not os.path.exists("maps"):
			os.makedirs("maps")
		fn = self.id
		i = 0
		while os.path.exists("maps/{}.png".format(fn)):
			i += 1
			fn = self.id + "-" + str(i)
		img.save('maps/{}.png'.format(fn))
		print("Saved maps/{}.png".format(fn))


def filename():
	hexes = ["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"]
	fn = []
	for _ in range(16):
		fn.append(random.choice(hexes))
	return "".join(fn)

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
		"--treas"  : False,
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

def main(args):
	flags = parseArgs(args)
	my_map = CellMap(flags["--height"],flags["--width"],flags["--seed"],flags["--death"],
					 flags["--birth"],flags["--reps"],flags["--out"],flags["--color"],
					 flags["--chunky"],flags["--treas"],)
	my_map.generateFullMap()

if __name__ == "__main__":
	main(sys.argv)