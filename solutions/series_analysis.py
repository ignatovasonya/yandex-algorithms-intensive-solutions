import sys

def main():
    n = int(sys.stdin.readline())
    s = list(map(int, sys.stdin.readline().split()))
    a = list(map(int, sys.stdin.readline().split()))
    
    pairs = list(zip(s, a))
    pairs.sort()
    
    total_weight = sum(a)
    half = (total_weight + 1) // 2
    
    prefix_weight = 0
    e = 0
    for si, ai in pairs:
        prefix_weight += ai
        if prefix_weight >= half:
            e = si
            break
    
    total_cost = 0
    for si, ai in pairs:
        total_cost += abs(e - si) * ai
    
    print(e, total_cost)

if __name__ == "__main__":
    main()
