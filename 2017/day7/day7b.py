from anytree import Node, RenderTree, LevelOrderIter
from scipy import stats

data = '''pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)
'''

data = open('input.txt').read()

nodeDict = {}

for line in data.splitlines():
    l = line.split()
    nodeName = l[0]
    nodeWeight = int(l[1][1:-1])
    childNames = []
    if len(l) > 2:
        childNames = l[3:]
        for i in range(len(childNames)):
            childNames[i] = childNames[i].replace(',','')
    nodeDict[nodeName] = [Node(nodeName, weight=nodeWeight), childNames]

# Assign parents
for nodeName, nodeDictEntry in nodeDict.iteritems():
    node, childNames = nodeDictEntry
    for childName in childNames:
        nodeDict[childName][0].parent = node

# Find the node with no parent
topNode = None
for nodeName, nodeDictEntry in nodeDict.iteritems():
    node, childNames = nodeDictEntry
    if node.parent == None:
        topNode = node
        break

# Calculate total weights
def recursiveWeight(node):
    totalWeight = node.weight
    if node.children:
        childWeights = []
        for child in node.children:
            childWeight = recursiveWeight(child)
            childWeights.append(childWeight)
            totalWeight += childWeight
        mode = stats.mode(childWeights).mode[0]
        for child in node.children:
            if child.totalWeight != mode:
                diff = child.totalWeight - mode
                print child, 'was unbalanced, it should have been', diff, 'lighter:', child.weight - diff
    node.totalWeight = totalWeight
    return totalWeight
        
recursiveWeight(topNode)


#print(RenderTree(topNode))

#print topNode
