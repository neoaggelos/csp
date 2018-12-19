import kenken_problems


s = kenken_problems.nine

N = s['N']

print ('problem = {')
print(f"'size' : {s['N']},")
print("'vars': [")
for s in s['sextes']:
    parts = s.split('|')
    func = parts[0]
    res = parts[1]
    vars = parts[2:]

    l = []
    for v in vars:
        x, y = int(v.split(',')[0]), int(v.split(',')[1])

        l.append(str(x * N + y))

    print('{')
    print("'cells': '", '_'.join(l), "',", sep='')
    print("'action':", end =' ')
    if func == '+':
        print("'sum',")
    elif func == '-':
        print("'sub',")
    elif func == '*':
        print("'mul',")
    elif func == '/':
        print("'div',")
    
    print("'result':", res)
    print('},')
    
print(']')