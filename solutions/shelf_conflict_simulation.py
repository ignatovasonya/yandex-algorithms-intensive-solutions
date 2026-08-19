import math

a, b, S = map(int, input().split())

D = (a - b) ** 2 + 4 * S
sqrt_D = int(math.isqrt(D))

if sqrt_D * sqrt_D != D:
    print(-1)
else:
    L1 = (a + b + sqrt_D) // 2
    L2 = (a + b - sqrt_D) // 2
    
    if (a + b + sqrt_D) % 2 == 0 and L1 > max(a, b):
        print(L1)
    elif (a + b - sqrt_D) % 2 == 0 and L2 > max(a, b):
        print(L2)
    else:
        print(-1)
