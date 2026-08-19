import sys

def main():
    n = int(sys.stdin.readline().strip())
    a = list(map(int, sys.stdin.readline().strip().split()))
    
    a = [0] + a
    
    prefix = [0] * (n + 2)
    for i in range(1, n + 1):
        prefix[i] = prefix[i - 1] + a[i]
    
    suffix = [0] * (n + 2)
    for i in range(n, 0, -1):
        suffix[i] = suffix[i + 1] + a[i]
    
    left = 1
    right = n
    min_diff = float('inf')
    best_l = 1
    best_r = n
    
    while left < right:
        sumV = prefix[left]
        sumM = suffix[right]
        diff = abs(sumV - sumM)
        
        if diff < min_diff:
            min_diff = diff
            best_l = left
            best_r = right
        
        if sumV < sumM:
            left += 1
        elif sumV > sumM:
            right -= 1
        else:
            break
    
    if left + 1 < right:
        sumV = prefix[left + 1]
        sumM = suffix[right]
        diff = abs(sumV - sumM)
        if diff < min_diff:
            min_diff = diff
            best_l = left + 1
            best_r = right
    
    print(min_diff, best_l, best_r)

if __name__ == "__main__":
    main()
