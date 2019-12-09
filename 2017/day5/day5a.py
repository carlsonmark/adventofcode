
jumps = [0,3,0,1,-3]

jumps = []
for line in open('input.txt').read().splitlines():
    jumps.append(int(line))

jumpCount = 0
curIdx = 0
while curIdx < len(jumps):
    jumpOffset = jumps[curIdx]
    nextIdx = curIdx + jumpOffset
    if jumpOffset >= 3:
        jumps[curIdx] -= 1
    else:
        jumps[curIdx] += 1
    jumpCount += 1
    curIdx = nextIdx

print jumpCount
