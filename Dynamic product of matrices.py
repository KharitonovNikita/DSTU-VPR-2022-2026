import numpy as np

def counting(p):
    n = len(p)
    m = [[0 for x in range(n)] for x in range(n)]
    s = [[0 for x in range(n)] for x in range(n)]

    for i in range(1, n):
        m[i][i] = 0 #По диагонали нули

    for L in range(2, n):
        for i in range(1, n - L + 1):
            j = i + L - 1
            m[i][j] = float('inf')

            for k in range(i, j):
                q = m[i][k] + m[k+1][j] + p[i-1]*p[k]*p[j]
                if q < m[i][j]:
                    m[i][j] = q
                    s[i][j] = k  # Оптимальный индекс разделения

    return m, s

def optimal_placement(s, i, j):
    if i == j:
        print("A" + str(i), end="")
    else:
        print("(", end="")
        optimal_placement(s, i, s[i][j])
        optimal_placement(s, s[i][j] + 1, j)
        print(")", end="")

def input_matrices():
    matrices = []
    num_matrices = int(input("Введите количество матриц: "))
    for i in range(num_matrices):
        rows = int(input(f"Введите количество строк в матрице {i + 1}: "))
        cols = int(input(f"Введите количество столбцов в матрице {i + 1}: "))
        if i > 0:
            prev_rows, prev_cols = matrices[-1]
            if prev_cols != rows:
                print("Ошибка: количество столбцов предыдущей матрицы не соответствует количеству строк текущей матрицы. Умножение невозможно.")
                return None
        matrices.append((rows, cols))
    return matrices

def generate_random_matrix(rows, cols):
    return np.random.randint(1, 10, size=(rows, cols))

def print_table(matrix):
    for row in matrix:
        print('\t'.join(map(str, row)))

def multiply_matrices(matrices, s, i, j, multiplication_count=0):
    if i == j:
        return matrices[i - 1], multiplication_count
    else:
        k = s[i][j]
        matrix_a, count_a = multiply_matrices(matrices, s, i, k, multiplication_count)
        matrix_b, count_b = multiply_matrices(matrices, s, k + 1, j, multiplication_count)
        multiplication_count = count_a + count_b + matrix_a.shape[0] * matrix_a.shape[1] * matrix_b.shape[1]
        product = np.dot(matrix_a, matrix_b)
        print()
        print(f"Промежуточный результат умножения от {i}-{k} на {k + 1}-{j}:")
        print_table(product)
        return product, multiplication_count

matrices = input_matrices()
if matrices is None:
    exit()

p = [mat[0] for mat in matrices] + [mat[-1] for mat in matrices[-1:]]  # Преобразуем размеры в массив размеров
print()
print("p =", p)

required_multiplications = 1
for size in p:
    required_multiplications *= size
print("Количество необходимых перемножений матриц:", required_multiplications)

m, s = counting(p)
print("\nТаблица стоимости перемножения матриц:")
print_table(m)

optimal_cost = m[1][len(p) - 1]
print("\nОптимальная стоимость перемножения матриц:", optimal_cost)

print("\nОптимальная расстановка скобок:")
optimal_placement(s, 1, len(p) - 1)

random_matrices = [generate_random_matrix(rows, cols) for rows, cols in matrices]
print("\nСгенерированные матрицы:")
for i, matrix in enumerate(random_matrices, start=1):
    print()
    print(f"Матрица {i}:")
    print_table(matrix)

result_matrix, total_multiplications = multiply_matrices(random_matrices, s, 1, len(p) - 1)
print("\nОптимальная стоимость перемножения матриц:", total_multiplications)
print("\nРезультат умножения с учетом оптимальной расстановки скобок:")
print_table(result_matrix)