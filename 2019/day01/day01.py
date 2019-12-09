from collections import namedtuple
import unittest
ExampleItem = namedtuple('ExampleItem', field_names='inp outp')
examplesA = [
  ExampleItem(12, 2),
  ExampleItem(14, 2),
  ExampleItem(1969, 654),
  ExampleItem(100756, 33583)
]
examplesB = [
  ExampleItem(14, 2),
  ExampleItem(1969, 966),
  ExampleItem(100756, 50346),
]

def calcFuel(mass):
  return math.floor(mass/3) - 2

def calcFuelRecursive(mass):
  fuelForMass = calcFuel(mass)
  totalFuel = fuelForMass
  print(f'{totalFuel}')
  while fuelForMass > 0:
    fuelForMass = calcFuel(fuelForMass)
    if fuelForMass > 0:
      totalFuel += fuelForMass
    print(f'{totalFuel}, {fuelForMass}')
  return totalFuel


testFunctionA = calcFuel
testFunctionB = calcFuelRecursive


def aocFunctionA(inpList):
  s = 0
  for inp in inpList:
    s += calcFuel(inp)
  return s

def aocFunctionB(inpList):
  s = 0
  for inp in inpList:
    s += calcFuelRecursive(inp)
  return s


class test_AOC(unittest.TestCase):
  def test_AOCa(self):
    for ex in examplesA:
      result = testFunctionA(ex.inp)
      self.assertEqual(result, ex.outp, msg=f'for {ex}')
    return
  def test_AOCb(self):
    for ex in examplesB:
      result = testFunctionB(ex.inp)
      self.assertEqual(result, ex.outp, msg=f'for {ex}')
    return
    

import math


aocInput = [int(x) for x in """145866
101641
71590
95922
140188
72376
55476
85697
98456
93928
106896
115715
124364
72957
108532
85330
147386
54323
145384
104665
117539
51151
94139
124784
106624
127034
121847
87388
85778
146850
62744
125351
62382
92694
92848
73291
85971
69358
148674
115957
127865
63695
82372
98268
115743
139867
124701
95280
58252
140192
148478
133129
129392
62828
117987
117070
134493
123419
148890
53183
143135
99892
133565
103335
126562
56527
148819
134626
62805
145167
117147
75263
89470
64792
145233
67654
67642
103778
90355
80176
128655
96818
78409
53704
74910
57051
108317
84280
95293
126315
63765
84776
91836
57134
122127
95625
136598
59997
104865
86457
""".splitlines()]


if __name__ == '__main__':
  print('AOC value A:', aocFunctionA(aocInput))
  print('AOC value B:', aocFunctionB(aocInput))
  unittest.main()
