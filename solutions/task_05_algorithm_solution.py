n, k = map(int, input().split())
a = [0] + list(map(int, input().split()))  

cost = [0] * (n + 1)
for i in range(1, n - k + 2):
    total = 0
    min_val = float('inf')
    for j in range(i, i + k):
        total += a[j]
        min_val = min(min_val, a[j])
    cost[i] = total * min_val

dp = [0] * (n + 1)
prev = [0] * (n + 1)  

for i in range(1, n + 1):
    dp[i] = dp[i - 1]
    prev[i] = 0
    if i >= k:
        if dp[i - k] + cost[i - k + 1] > dp[i]:
            dp[i] = dp[i - k] + cost[i - k + 1]
            prev[i] = 1

towers = []
i = n
while i > 0:
    if prev[i] == 1:
        towers.append(i - k + 1)
        i -= k
    else:
        i -= 1

towers.reverse()

print(len(towers))
print(' '.join(map(str, towers)))
