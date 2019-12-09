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
    pythonLine = 'if {} {} {}:\n'.format(varCheck, checkType, checkValue)
    pythonLine += '  {} {} {}\n'.format(varName, pythonOp, value)
    pythonLine += '  largest = max(largest, {})'.format(varName)
    pythonLines.append(pythonLine)
    allVars.add(varName)
    
print pythonLines
print allVars

variables = {}
for varName in allVars:
    variables[varName] = 0

largest = 0
variables['largest'] = largest

toExec = '\n'.join(pythonLines)
    
exec(toExec, {}, variables)

for varName in allVars:
    largest = max(variables[varName], largest)
    print varName,'=',variables[varName]
    

print 'largest:', variables['largest']
