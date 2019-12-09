
def isAnagram(a, b):
    if len(a) != len(b):
        return False
    for c in a:
        if c in b:
            b = b.replace(c, '', 1)
        else:
            break
    return len(b) == 0
        
def isValid(line):
    valid = True
    l = line.strip().split()
    for i in range(len(l)):
        a = l[i]
        for j in range(len(l)):
            if i == j:
                continue
            b = l[j]
            if isAnagram(a, b):
                valid = False
                break
        if not valid:
            break
    return valid

f = open("input.txt")
s = 0
for l in f.readlines():
    if isValid(l):
        s += 1
print s
