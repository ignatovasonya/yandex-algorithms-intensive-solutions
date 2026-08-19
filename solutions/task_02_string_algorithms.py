s = input().strip()
n = len(s)

INF = 10**9
dp = [[INF, INF] for _ in range(n + 1)]
dp[0][0] = 0

for i in range(1, n + 1):
    river = s[i-1]
    
    if river == 'B':
        dp[i][0] = min(dp[i-1][1] + 1)
        dp[i][1] = min(dp[i-1][0] + 1)
    elif river == 'L':
        dp[i][0] = min(dp[i-1][0], dp[i-1][1] + 1)
    else:  # R
        dp[i][1] = min(dp[i-1][1], dp[i-1][0] + 1)

# В конце можем быть на любом берегу, но хотим на правом
result = min(dp[n][0] + 1, dp[n][1])
print(result)
