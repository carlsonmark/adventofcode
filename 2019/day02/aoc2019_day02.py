from collections import namedtuple
import copy

def toList(s):
    return [int(x) for x in s.split(',')]

ExpectedResult = namedtuple('ExpectedResult', 'intput output')

inputAList = toList( "1,12,02,3,1,1,2,3,1,3,4,3,1,5,0,3,2,1,10,19,2,9,19,23,2,23,10,27,1,6,27,31,1,31,6,35,2,35,10,39,1,39,5,43,2,6,43,47,2,47,10,51,1,51,6,55,1,55,6,59,1,9,59,63,1,63,9,67,1,67,6,71,2,71,13,75,1,75,5,79,1,79,9,83,2,6,83,87,1,87,5,91,2,6,91,95,1,95,9,99,2,6,99,103,1,5,103,107,1,6,107,111,1,111,10,115,2,115,13,119,1,119,6,123,1,123,2,127,1,127,5,0,99,2,14,0,0")
testAList = [
    ExpectedResult(toList("1,0,0,0,99"), 2),
    ExpectedResult(toList("2,3,0,3,99"), 2),
    ExpectedResult(toList("2,4,4,5,99,0"), 2),
    ExpectedResult(toList("1,1,1,4,99,5,6,0,99"), 30)
    ]

def add(val1, val2):
  return val1 + val2

def mul(val1, val2):
  return val1 * val2

ops = {
  1 : add,
  2 : mul
}

def executeA(l, pc):
  #print(f'executing: {pc}')
  opcode = l[pc]
  if opcode == 99:
    return False
  loc1, loc2, locOut = l[pc+1:pc+4]
  op = ops[opcode]
  val1 = l[loc1]
  val2 = l[loc2]
  l[locOut] = op(val1, val2)
  return True

def functionA(inp: list):
  l = copy.copy(inp)
  pc = 0
  cont = True
  while cont:
    cont = executeA(l, pc)
    pc += 4
  return l[0]

for inp, outp in testAList:
  ret = functionA(inp)
  assert ret == outp, '{} != {} for input={}'.format(ret, outp, inp)

print('result A:', functionA(inputAList))

def functionB():
  for noun in range(256):
    for verb in range(100):
      l = copy.copy(inputAList)
      l[1] = noun
      l[2] = verb
      try:
        if functionA(l) == 19690720:
          print(f'{noun}, {verb} = 19690720')
          return
      except:
        pass
  print('not found!')
  return
functionB()
