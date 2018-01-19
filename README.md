# Simple procedural generation of "dungeon maps"

Basic proof of concept for a "cellular automata" model. No real refinement at this point.

Initial work based on [this tutorial](https://gamedevelopment.tutsplus.com/tutorials/generate-random-cave-levels-using-cellular-automata--gamedev-9664).

It takes the following flags:

* --width *x*: the width of the map. *x* must be a positive integer. See below.
* --height *x*: the height of the map. *x* must be a positive integer. See below. 
* --seed *x*: the chance a given cell will be generated as "wall". *x* must be an integer from 1-99.
* --death *x*: if a wall cell has fewer than this many wall cells surrounding it, it becomes empty. *x* must be an integer from 1-8.
* --birth *x*: if an empty cell has more than this many wall cells surrounding it, it becomes a wall. *x* must be an integer from 1-8.
* --reps *x*: the number of smoothing passes to take on the map. *x* must be a positive integer. Large values can significantly extend runtime.
* --out: save the result to an image in the maps/ directory instead of printing it to the screen.

### A note on width and height

If you use --out, width and height are in pixels.

If you don't, height is lines of text, and width is measured in **chunks of two characters**; "--width 40" will produce a map 80 characters wide. This is because each "wall" cell is represented by a double **I** character and each "empty" cell is represented by a double space; in the font the developer uses, this makes it so that if a map's width and height are the same, the map is roughly square.
