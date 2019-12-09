
start = [0, 2, 7, 0]
#start = [int(i) for i in '2	8	8	5	4	2	3	1	5	5	1	2	15	13	5	14'.split()]

numBanks = len(start)

history = []

curBanks = list(start)

count = 0

foundCounter = 0
while foundCounter < 3:
    maxVal = max(curBanks)
    maxIdx = curBanks.index(maxVal)
    history.append(list(curBanks))
    curIdx = maxIdx
    curBanks[curIdx] = 0
    while maxVal > 0:
        maxVal -= 1
        curIdx += 1
        if curIdx >= numBanks:
            curIdx = 0
        curBanks[curIdx] += 1
    if len(history) > 2:
        foundCounter = history.count(history[1])
    print curBanks, foundCounter#, history

firstRepeatIdx = history[2:].index(history[1])
secondRepeatRelIdx = history[2+firstRepeatIdx+1:].index(history[1]) + 1
    
print firstRepeatIdx, secondRepeatRelIdx
