from collections import deque

n = int(input())

graph = [[] for _ in range(n + 1)]
for _ in range(n - 1):
    u, v = map(int, input().split())
    graph[u].append(v)
    graph[v].append(u)

leaves = [i for i in range(1, n + 1) if len(graph[i]) == 1]

for i in range(1, n + 1):
    leaf_count = 0
    for neighbor in graph[i]:
        if len(graph[neighbor]) == 1:
            leaf_count += 1
    if leaf_count >= 2:
        print(2)
        exit()

if len(leaves) < 2:
    print(0)
else:
    dist = [-1] * (n + 1)
    source = [-1] * (n + 1)
    q = deque()
    
    for leaf in leaves:
        dist[leaf] = 0
        source[leaf] = leaf
        q.append(leaf)
    
    min_dist = n + 1
    while q:
        u = q.popleft()
        for v in graph[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                source[v] = source[u]
                q.append(v)
            elif source[v] != source[u]:
                min_dist = min(min_dist, dist[u] + dist[v] + 1)
    
    print(min_dist)
