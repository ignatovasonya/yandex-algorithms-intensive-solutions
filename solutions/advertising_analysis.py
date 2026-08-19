def can_fit(k, N, W, H, words):
    total_height = 0
    current_width = 0
    current_height = 0
    
    for i in range(N):
        w = k * words[i][0]
        h = k * words[i][1]
        
        if w > W + 1e-12 or h > H + 1e-12:
            return False
            
        if current_height == 0:
            current_height = h
            current_width = w
        elif abs(h - current_height) <= 1e-12:
            if current_width + w <= W + 1e-12:
                current_width += w
            else:
                total_height += current_height
                if total_height > H + 1e-12:
                    return False
                current_height = h
                current_width = w
        else:
            total_height += current_height
            if total_height > H + 1e-12:
                return False
            current_height = h
            current_width = w
            
        if total_height + current_height > H + 1e-12:
            return False
            
    total_height += current_height
    return total_height <= H + 1e-12

N, W, H = map(int, input().split())
words = []
for _ in range(N):
    a, b = map(int, input().split())
    words.append((a, b))

left, right = 0.0, 1e10
for _ in range(100):
    mid = (left + right) / 2
    if can_fit(mid, N, W, H, words):
        left = mid
    else:
        right = mid

print(f"{left:.15f}")
