""" A tool for randomly generating maps.
	It starts by populating a grid with randomized True/False values and
	then uses a "cellular automata"-based smoothing algorithm to build a
	map. 

	Maps are rectangles, but can be of any size. Naturally, larger maps
	take longer to generate. 

	By default, the mapper will print to the screen as a grid of "I"s (walls) 
	and spaces (paths). You can tell the mapper to print to an image instead.
	If you do, the following apply:

	You can tell the mapper to make a map "chunky", which keeps the T/F 
	grid the same size but uses four pixels instead of one for each point 
	on the grid, doubling the size of the final generated image.

	Maps are two-color: black and white by default, but it will use random 
	contrasting colors if told to.

	You can tell the mapper to insert treasure, which appears as a third
	color on the map.
"""

__author__ = "Noëlle Anthony"
__version__ = "1.0.0"

import random
import sys
import os

from PIL import Image

class CellMap:
	initial = []
	genmap = []
	treasurelist = []

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
		""" Puts everything together. Runs the smoothing routine a number
			of times equal to self.reps, generates treasure (if self.treasure
			is set), and creates and saves an image of the map if self.out is
			set or prints the map to stdout if it isn't.
		"""
		self.createMap()
		for _ in range(self.reps):
			self.smoothMap()
		if self.treasure:
			self.generateTreasure()
		if self.out:
			self.createImage()
		else:
			self.printScreen()	

	def resetMap(self):
		""" Resets the map to its initial state, allowing the user to experiment
			with death/birth limits and number of repetitions on a single map.
		"""
		self.genmap = list(self.initial)

	def createMap(self):
		""" Initializes an x by y grid.
			x is width, y is height
			seed is the chance that a given cell will be "live" and should be
			an integer between 1-99.
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
		self.genmap = new_map

	def smoothMap(self):
		""" Refines the grid using cellular-automaton rules.
			If a wall doesn't have enough wall neighbors, it "dies" and
			becomes a path. If a path has too many wall neighbors, it turns
			into a wall. This is controlled by the values in self.death and
			self.birth, respectively.
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
		""" Counts the number of wall neighbors a cell has and returns that count.
		"""
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
				elif self.genmap[n_y][n_x] and self.genmap[n_y][n_x] not in ("Gold","Diam"):
					# This neighbor is on the map and is a wall.
					count += 1
		return count

	def generateTreasure(self):
		""" If a path cell has 5 wall neighbors, put a treasure there.
			If a path cell has at least 6 wall neighbors, put a rare treasure.
		"""
		for j in range(len(self.genmap)):
			for i in range(len(self.genmap[j])):
				if not self.genmap[j][i]:
					self.genmap[j][i] = "Gold" if self.countWalls(i,j) == 5 else self.genmap[j][i]
					self.genmap[j][i] = "Diam" if self.countWalls(i,j) >= 6 else self.genmap[j][i]
		
	def printScreen(self):
		""" Prints the map to standard out, using "II" for a wall 
			and "  " for a path.

			The "color", "chunky", and "treasure" options don't affect
			this mode.
		"""
		wall = "II"
		path = "  "
		gold = "GG"
		diam = "DD"
		for line in self.genmap:
			print("".join([path if not x 
								else (gold if x == "Gold" 
										   else (diam if x == "Diam" 
										   			  else wall)) for x in line]))
		print()

	def createImage(self):
		""" Creates and saves an image of the map.

			If self.color is True, the map uses randomized complementary 
			colors; otherwise, it uses black for walls, white for paths, and 
			light grey for treasures.

			If self.chunky is True, the map uses 4 pixels for each cell 
			instead of one. This results in an image that's twice as large, 
			and is useful for enlarging smaller maps without the added runtime
			of actually generating a larger map.

			If an image with the current map's name already exists, the script
			will add digits after the filename but before the extension, to 
			avoid a collision. While the possibility of a name collision is 
			low, this allows you to make several copies of a given map (for
			example, with different settings) without fear of overwriting 
			your previous maps.
		"""
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
		c_gold = [(x+64)%255 for x in c_space]
		c_diam = [(x+64)%255 for x in c_gold]
		if self.chunky:
			for line in self.genmap:
				for _ in range(2):
					for val in line:
						for _ in range(2):
							if not val:
								lst.append(tuple(c_space))
							elif val == "Gold":
								lst.append(tuple(c_gold))
							elif val == "Diam":
								lst.append(tuple(c_diam))
							else:
								lst.append(tuple(c_wall))
		else:
			for line in self.genmap:
				for val in line:
					if not val:
						lst.append(tuple(c_space))
					elif val == "Gold":
						lst.append(tuple(c_gold))
					elif val == "Diam":
						lst.append(tuple(c_diam))
					else:
						lst.append(tuple(c_wall))
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

	def printArray(self):
		""" This prints the map as a list of lists of True/False values, 
			possibly useful for importing into other scripts or for uses
			other than generating maps.
		"""
		print("[",end="\n")
		for line in self.genmap:
			print("\t{},".format(line))
		print("]")


def filename():
	""" Creates a 16-character hexadecimal ID.
		Since the number of results is so large (16^16), the chance of
		a collision is very small.
	"""
	hexes = ["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"]
	fn = []
	for _ in range(16):
		fn.append(random.choice(hexes))
	return "".join(fn)

def parseArgs(args):
	""" Parses the command-line arguments sent to the script.
		Discards anything that isn't a recognized as a valid flag.
	"""
	flags = {
		"--height"  : 20,
		"--width"   : 20,
		"--seed"    : 45,
		"--death"   : 4,
		"--birth"   : 4,
		"--reps"    : 2,
		"--out"     : False,
		"--color"   : False,
		"--chunky"  : False,
		"--treasure": False,
	}
	for flag, default in flags.items():
		if flag in args:
			if flag == "--out":
				flags["--out"] = True
			elif flag == "--color":
				flags["--color"] = True
			elif flag == "--chunky":
				flags["--chunky"] = True
			elif flag == "--treasure":
				flags["--treasure"] = True
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