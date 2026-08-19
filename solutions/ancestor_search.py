import sys
sys.setrecursionlimit(200000)

n = int(input())
parent_list = list(map(int, input().split()))
m = int(input())

children = [[] for _ in range(n + 1)]
root = -1
for i in range(1, n + 1):
    parent = parent_list[i - 1]
    if parent == 0:
        root = i
    else:
        children[parent].append(i)

tin = [0] * (n + 1)
tout = [0] * (n + 1)
timer = 0

def dfs(u):
    global timer
    timer += 1
    tin[u] = timer
    for v in children[u]:
        dfs(v)
    timer += 1
    tout[u] = timer

dfs(root)

for _ in range(m):
    a, b = map(int, input().split())
    if tin[a] <= tin[b] and tout[a] >= tout[b]:
        print(1)
    else:
        print(0)
