import numpy as np

def matrix_mult_mod(a, b, mod):
    """Умножение двух матриц 2x2 с взятием результата по модулю."""
    return [
        [(a[0][0] * b[0][0] + a[0][1] * b[1][0]) % mod,
         (a[0][0] * b[0][1] + a[0][1] * b[1][1]) % mod],
        [(a[1][0] * b[0][0] + a[1][1] * b[1][0]) % mod,
         (a[1][0] * b[0][1] + a[1][1] * b[1][1]) % mod],
    ]

def matrix_pow_mod(mat, power, mod):
    """Быстрое возведение матрицы в степень с взятием результата по модулю."""
    result = [[1, 0], [0, 1]]  # Единичная матрица
    while power > 0:
        if power % 2 == 1:
            result = matrix_mult_mod(result, mat, mod)
        mat = matrix_mult_mod(mat, mat, mod)
        power = power // 2
    return result

def lucas_u(n, P, Q, mod):
    """Вычисление U_n(P, Q) mod m с использованием матриц."""
    if n == 0:
        return 0
    elif n == 1:
        return 1 % mod
    else:
        mat = [[0, 1], [-Q, P]]
        mat_n = matrix_pow_mod(mat, n - 1, mod)
        # U_n = mat_n[1][0] * U_0 + mat_n[1][1] * U_1
        return (mat_n[1][0] * 0 + mat_n[1][1] * 1) % mod

def lucas_v(n, P, Q, mod):
    """Вычисление V_n(P, Q) mod m с использованием матриц."""
    if n == 0:
        return 2 % mod
    elif n == 1:
        return P % mod
    else:
        mat = [[0, 1], [-Q, P]]
        mat_n = matrix_pow_mod(mat, n - 1, mod)
        # V_n = mat_n[1][0] * V_0 + mat_n[1][1] * V_1
        return (mat_n[1][0] * 2 + mat_n[1][1] * P) % mod
    
print(lucas_u(2533419940566027519473381088361022224, 1, 2, 100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000))