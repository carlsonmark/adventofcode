data = """b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10
"""
data = open('input.txt').read()

pythonLines = []
allVars = set()

for line in data.splitlines():
    varName, op, value, if_, varCheck, checkType, checkValue = line.split()
    pythonOp = '+='
    if op == 'dec':
        pythonOp = '-='
    # if varCheck checkType checkValue: varName op value
    pythonLine = 'if {} {} {}: {} {} {}'.format(varCheck, checkType, checkValue, varName, pythonOp, value)
    pythonLines.append(pythonLine)
    allVars.add(varName)
    
print pythonLines
print allVars

variables = {}
for varName in allVars:
    variables[varName] = 0

toExec = '\n'.join(pythonLines)
    
exec(toExec, {}, variables)

largest = 0
for varName in allVars:
    largest = max(variables[varName], largest)
    print varName,'=',variables[varName]
    

print 'largest:', largest
