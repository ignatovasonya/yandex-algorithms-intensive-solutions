n = int(input())

def steps(n):
    if n == 0:
        return 1
    if n == 1:
        return 1
    if n == 2:
        return 2
    
    a, b, c = 1, 1, 2
    
    for i in range(3, n + 1):
        next_val = a + b + c
        a, b, c = b, c, next_val
    
    return c

print(steps(n))

