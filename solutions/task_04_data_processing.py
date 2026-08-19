text = input().strip()
n = int(input())
dictionary = [input().strip() for _ in range(n)]

# Сортируем слова по длине (оптимизация)
dictionary.sort(key=len, reverse=True)

dp = [False] * (len(text) + 1)
prev = [-1] * (len(text) + 1)
dp[0] = True  # пустая строка

for i in range(1, len(text) + 1):
    for word in dictionary:
        if len(word) <= i and text[i - len(word):i] == word:
            if dp[i - len(word)]:
                dp[i] = True
                prev[i] = i - len(word)
                break  # достаточно одного способа

# Восстанавливаем разбиение
result = []
pos = len(text)
while pos > 0:
    start = prev[pos]
    word = text[start:pos]
    result.append(word)
    pos = start

# Выводим слова в правильном порядке
print(' '.join(reversed(result)))
