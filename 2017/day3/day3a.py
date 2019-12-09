import numpy as np

def spiral_cw(A):
    A = np.array(A)
    out = []
    while(A.size):
        out.append(A[0])        # take first row
        A = A[1:].T[::-1]       # cut off first row and rotate counterclockwise
    return np.concatenate(out)

def base_spiral(nrow, ncol):
    return spiral_cw(np.arange(nrow*ncol).reshape(nrow,ncol))[::-1]

def to_spiral(A):
    A = np.array(A)
    B = np.empty_like(A)
    B.flat[base_spiral(*A.shape)] = A.flat
    return B

def genPuzz(num):
    width = np.ceil(np.sqrt(num))
    if width % 2 == 0:
        width += 1
    a = np.arange(1, width * width + 1).reshape(width, width)
    return to_spiral(a)

generated = 289326

puzz = genPuzz(generated)

x, y = np.where(generated == puzz)

print 'found', generated, 'at', x,y

sx, sy = puzz.shape
dx = abs(x[0] - np.floor(sx/2))
dy = abs(y[0] - np.floor(sy/2))
print 'distance to center:', sx, sy, dx, dy
print 'walking distance:', dx + dy
