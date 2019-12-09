import numpy as np
from pprint import pprint
import sys

np.set_printoptions(threshold=np.inf)

generated = 289326

# Generate an empty matrix of the desired size
# Actually, for this puzzle, it is far too large
width = int(np.ceil(np.sqrt(generated)))
if width % 2 == 0:
    width += 1
width = 11
a = np.zeros((width,width), dtype='int')

x = int(np.floor(width/2))
y = x

print width, x, y

UP, LEFT, DOWN, RIGHT = ((0, -1), (-1, 0), (0, +1), (+1, 0) )
directions = (UP, LEFT, DOWN, RIGHT)
currentDirection = RIGHT
def nextDirection(current):
    curIdx = directions.index(current)
    nextIdx = curIdx + 1
    if nextIdx == len(directions):
        nextIdx = 0
    return directions[nextIdx]

curValue = 1
a[x][y] = curValue

while True:
    # move
    dx,dy = currentDirection
    x += dx
    y += dy
    slice_ = a[x-1:x+2,y-1:y+2]
    curValue = np.sum(slice_)
    a[x][y] = curValue
    print x, y, curValue
    print slice_
    # change direction?
    nextDir = nextDirection(currentDirection)
    nextDx, nextDy = nextDir
    if a[x + nextDx][y + nextDy] == 0:
        currentDirection = nextDir
    if curValue > generated:
        break

#pprint(a)
np.set_printoptions(precision=0)
print(a)
#np.savetxt(sys.stdout, a)
pprint(curValue)
