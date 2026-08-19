n, p = map(int, input().split())
c = list(map(int, input().split()))

arr = []
for i in range(n):
    arr.append((c[i], i + 1))

arr.sort()

best_i = 1
best_j = 2
best_diff = float('inf')

for j in range(n):
    target = p * arr[j][0]
    
    left, right = 0, n - 1
    pos = n - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid][0] >= target:
            pos = mid
            right = mid - 1
        else:
            left = mid + 1
    
    for k in range(max(0, pos - 2), min(n, pos + 3)):
        if k == j:
            continue
            
        ratio = arr[k][0] / arr[j][0]
        diff = abs(ratio - p)
        
        if diff < best_diff - 1e-12:
            best_diff = diff
            best_i = arr[k][1]
            best_j = arr[j][1]

print(best_i, best_j)
