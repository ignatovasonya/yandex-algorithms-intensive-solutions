import sys
from collections import defaultdict

def main():
    input = sys.stdin.read().split()
    idx = 0
    n = int(input[idx]); idx += 1
    d = int(input[idx]); idx += 1
    
    points = []
    point_set = set()
    
    for _ in range(n):
        x = int(input[idx]); idx += 1
        y = int(input[idx]); idx += 1
        points.append((x, y))
        point_set.add((x, y))
    
    result = 0
    used_pairs = set()
    
    max_dx = int(d**0.5) + 1
    for dx in range(-max_dx, max_dx + 1):
        remaining = d - dx * dx
        if remaining < 0:
            continue
            
        dy = int(remaining**0.5)
        if dy * dy != remaining:
            continue
        
        for x, y in points:
            for x2, y2 in [(x + dx, y + dy), (x + dx, y - dy)]:
                if (x2, y2) in point_set and (x, y) != (x2, y2):
                    pair = tuple(sorted([(x, y), (x2, y2)]))
                    if pair not in used_pairs:
                        used_pairs.add(pair)
                        result += 1
    
    print(result)

if __name__ == "__main__":
    main()
