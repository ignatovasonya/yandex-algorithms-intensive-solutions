import sys
from collections import deque

def solve():
    n = int(sys.stdin.readline())
    parent = [0] * n
    for i in range(1, n):
        parent[i] = int(sys.stdin.readline())
    
    b = list(map(int, sys.stdin.readline().split()))
    
    children = [[] for _ in range(n)]
    for i in range(1, n):
        children[parent[i]].append(i)
    
    subtree_sum = [0] * n
    
    order = []
    stack = [0]
    while stack:
        u = stack.pop()
        order.append(u)
        for v in children[u]:
            stack.append(v)
    
    for u in reversed(order):
        subtree_sum[u] = b[u]
        for v in children[u]:
            subtree_sum[u] += subtree_sum[v]
    
    x = [0] * n
    x[0] = -b[0]  
    
    stack = [0]
    while stack:
        u = stack.pop()
        children_sum = 0
        for v in children[u]:
            children_sum += subtree_sum[v]
            stack.append(v)
        if u != 0:
            x[u] = -b[u] + children_sum
    
    ans = sum(abs(val) for val in x)
    print(ans)

if __name__ == "__main__":
    solve()
