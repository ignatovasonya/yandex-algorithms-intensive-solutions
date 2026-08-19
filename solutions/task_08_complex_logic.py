def build_primes(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
    return is_prime

n = int(input())

if n == 0:
    print(2)
    exit()

is_prime = build_primes(n)
win = [False] * (n + 1)

for i in range(1, n + 1):
    for take in (1, 2, 3):
        rest = i - take
        if rest >= 0 and not is_prime[rest]:
            if not win[rest]:
                win[i] = True
                break

print(1 if win[n] else 2)
