
example = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"

def calc_hash(step: str) -> int:
    h = 0
    for c in step:
        h += ord(c)
        h *= 17
        h &= 0xff
    return h

def solve(s: str):
    steps = s.replace('\n','').split(',')
    hashes = []
    for step in steps:
        h = calc_hash(step)
        print(f'{h} for {step}')
        hashes.append(h)
    print(sum(hashes))

if __name__ == '__main__':
    # solve(example)
    solve(open('input.txt').read())

# too low: 509879, accidentally had the newline from the file in there
