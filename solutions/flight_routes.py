import heapq
import sys

def time_to_minutes(s):
    h, m = map(int, s.split(':'))
    return h * 60 + m

def main():
    # Читаем построчно
    N = int(sys.stdin.readline().strip())
    trips_ab = []
    for _ in range(N):
        line = sys.stdin.readline().strip()
        dep, arr = line.split('-')
        trips_ab.append((time_to_minutes(dep), time_to_minutes(arr)))
    
    M = int(sys.stdin.readline().strip())
    trips_ba = []
    for _ in range(M):
        line = sys.stdin.readline().strip()
        dep, arr = line.split('-')
        trips_ba.append((time_to_minutes(dep), time_to_minutes(arr)))
    
    trips_ab.sort()
    trips_ba.sort()
    
    ready_a = []  # min-heap of times when buses become available at A
    ready_b = []  # min-heap of times when buses become available at B
    buses = 0
    
    i, j = 0, 0
    while i < N or j < M:
        if j == M or (i < N and trips_ab[i][0] <= trips_ba[j][0]):
            # A->B trip
            dep, arr = trips_ab[i]
            i += 1
            
            # Find available bus at A (arrived before departure)
            if ready_a and ready_a[0] <= dep:
                heapq.heappop(ready_a)
            else:
                buses += 1
                
            heapq.heappush(ready_b, arr)
        else:
            # B->A trip  
            dep, arr = trips_ba[j]
            j += 1
            
            if ready_b and ready_b[0] <= dep:
                heapq.heappop(ready_b)
            else:
                buses += 1
                
            heapq.heappush(ready_a, arr)
    
    print(buses)

if __name__ == "__main__":
    main()
