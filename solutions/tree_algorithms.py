import sys
import heapq

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    a = list(map(int, data[1:1+n]))
    b = list(map(int, data[1+n:1+2*n]))
    
    total_a = 0
    total_b = 0
    for i in range(n):
        total_a += a[i]
        total_b += b[i]
    
    if total_a > total_b:
        print(-1)
        return
    
    # Проверка k=0
    zero_ok = True
    for i in range(n):
        if a[i] > b[i]:
            zero_ok = False
            break
    if zero_ok:
        print(0)
        return
    
    left, right = 1, n - 1
    answer = n - 1
    
    # Предварительно создадим все события для экономии памяти
    all_events = []
    for i in range(n):
        if a[i] > 0:
            all_events.append((i, a[i]))
    
    while left <= right:
        mid = (left + right) // 2
        
        # Вместо создания нового списка events для каждого mid, используем исходный all_events
        # и вычисляем границы на лету
        heap = []
        event_ptr = 0
        possible = True
        
        for day in range(n):
            # Добавляем события, чья левая граница <= текущему дню
            while event_ptr < len(all_events):
                i, cnt = all_events[event_ptr]
                left_bound = max(0, i - mid)
                if left_bound <= day:
                    right_bound = min(n - 1, i + mid)
                    heapq.heappush(heap, (right_bound, cnt))
                    event_ptr += 1
                else:
                    break
            
            # Обрабатываем текущий день
            capacity = b[day]
            while capacity > 0 and heap:
                r, cnt = heapq.heappop(heap)
                if r < day:
                    possible = False
                    break
                
                take = min(capacity, cnt)
                capacity -= take
                cnt -= take
                
                if cnt > 0:
                    heapq.heappush(heap, (r, cnt))
            
            if not possible:
                break
        
        # Проверяем оставшиеся события
        while heap and possible:
            r, cnt = heapq.heappop(heap)
            if r < n - 1:
                possible = False
        
        if possible:
            answer = mid
            right = mid - 1
        else:
            left = mid + 1
    
    print(answer)

if __name__ == "__main__":
    main()
