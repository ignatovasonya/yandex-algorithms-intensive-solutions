import sys
import bisect

def main():
    input = sys.stdin.read().split()
    idx = 0
    
    n = int(input[idx]); idx += 1
    powers = []
    rates = []
    
    for _ in range(n):
        b = int(input[idx]); idx += 1
        t = int(input[idx]); idx += 1
        powers.append(b)
        rates.append(t)
    
    m = int(input[idx]); idx += 1
    queries = []
    for _ in range(m):
        q = int(input[idx]); idx += 1
        queries.append(q)
    
    MOD = 1000000001
    results = []
    
    for q in queries:
        pos = bisect.bisect_left(powers, q) - 1
        if pos < 0:
            pos = 0
        tax = q * rates[pos]
        results.append(str(tax % MOD))
    
    print("\n".join(results))

if __name__ == "__main__":
    main()
