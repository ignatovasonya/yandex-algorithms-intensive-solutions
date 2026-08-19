def levenshtein(word1, word2):
    word1 = word1.lower()
    word2 = word2.lower()
    n, m = len(word1), len(word2)
    if n > m:
        word1, word2 = word2, word1
        n, m = m, n
    current_row = range(n + 1)
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            if word1[j - 1] != word2[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n]

if __name__ == '__main__':
    result = levenshtein(input("Слово 1"), input("Слово 2"))
    print(result)
