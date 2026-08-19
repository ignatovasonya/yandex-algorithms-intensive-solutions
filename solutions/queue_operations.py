

    

import sys

def main():
    n, m, x = map(int, sys.stdin.readline().split())
    
    intervals = []
    
    for _ in range(n):
        a, b, v = map(int, sys.stdin.readline().split())
        
        if a < b:
            start_t = (x - b) / v
            end_t = (x - a) / v
        else:
            start_t = (b - x) / v
            end_t = (a - x) / v
        
        if start_t > end_t:
            start_t, end_t = end_t, start_t
        
        if end_t >= 0:
            start_t = max(0.0, start_t)
            intervals.append((start_t, end_t))
    
    intervals.sort()
    merged = []
    
    for start, end in intervals:
        if not merged or start > merged[-1][1]:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)
    
    times = list(map(int, sys.stdin.readline().split()))
    results = []
    
    for t in times:
        low, high = 0, len(merged) - 1
        idx = -1
        
        while low <= high:
            mid = (low + high) // 2
            if merged[mid][0] <= t:
                idx = mid
                low = mid + 1
            else:
                high = mid - 1
        
        if idx >= 0 and t <= merged[idx][1]:
            results.append(f"{merged[idx][1]:.9f}")
        else:
            results.append(f"{t:.9f}")
    
    print("\n".join(results))

if __name__ == "__main__":
    main()
