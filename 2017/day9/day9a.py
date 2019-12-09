data = '{{<a!>},{<a!>},{<a!>},{<ab>}}'
data = '{{{},{},{{}}}}'
data = '{{<!>},{<!>},{<!>},{<a>}}'
data = open('input.txt').read()

from anytree import Node, RenderTree, LevelOrderIter

topNode = None
nodeStack = []
currentGarbage = ''
allGarbage = ''

def processChar(c, skippedPrevious, collectingGarbage):
    global nodeStack, topNode, currentGarbage, allGarbage
    shouldSkipNext = False
    if c == '>':
        print 'done garbage collecting', currentGarbage
        collectingGarbage = False
    elif c == '!':
        shouldSkipNext = True
    elif collectingGarbage:
        print 'adding to garbage:', c
        currentGarbage += c
        allGarbage += c
    elif c == '<':
        collectingGarbage = True
        currentGarbage = ''
    elif c == '{':
        # Create a new node
        newNode = Node('', data='')
        if topNode == None:
            topNode = newNode
            nodeStack.append(newNode)
        else:
            # Add node as a child of the deepest node in the stack
            newNode.parent = nodeStack[-1]
            nodeStack.append(newNode)
    elif c == '}':
        print 'finished node:', nodeStack[-1]
        nodeStack.pop()
    else:
        nodeStack[-1].data += c
    return shouldSkipNext, collectingGarbage
    
skipNext = False
skippedPrevious = False
collectingGarbage = False
count = 0
for c in data[:-1]:
    count += 1
    if skipNext:
        print count, 'skipping', c
        skippedPrevious = True
        skipNext = False
        continue
    else:
        print count, 'of',len(data), 'did not skip', c
    skipNext, collectingGarbage = processChar(c, skippedPrevious, collectingGarbage)
    skippedPrevious = False

print(RenderTree(topNode))

score = 0
depth = 0
def recursiveScore(n, depth):
    childScore = 0
    for child in n.children:
        childScore += recursiveScore(child, depth + 1)
    return depth + childScore

print recursiveScore(topNode, 1)
print len(allGarbage)
