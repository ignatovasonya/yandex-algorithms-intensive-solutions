import sys

def main():
    input = sys.stdin.read().split()
    idx = 0
    n = int(input[idx]); idx += 1
    m = int(input[idx]); idx += 1
    k = int(input[idx]); idx += 1
    
    a = [0] + list(map(int, input[idx:idx + n])); idx += n
    
    diff = [0] * (n + 2)
    
    # Обрабатываем маршруты
    for _ in range(m):
        l = int(input[idx]); idx += 1
        r = int(input[idx]); idx += 1
        diff[l] += 1
        diff[r + 1] -= 1
    
    # Считаем freq
    freq = [0] * (n + 1)
    current = 0
    for i in range(1, n + 1):
        current += diff[i]
        freq[i] = current
    
    # Суммарный дискомфорт до ремонта
    total_discomfort = 0
    for i in range(1, n + 1):
        total_discomfort += a[i] * freq[i]
    
    # Сортируем участки по убыванию важности (freq)
    segments = []
    for i in range(1, n + 1):
        segments.append((freq[i], a[i]))
    
    segments.sort(reverse=True)
    
    # Жадно ремонтируем
    remaining = k
    for f, bumps in segments:
        if remaining <= 0:
            break
        repair = min(bumps, remaining)
        total_discomfort -= repair * f
        remaining -= repair
    
    print(total_discomfort)

if __name__ == "__main__":
    main()
