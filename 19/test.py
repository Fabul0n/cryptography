import sympy

def lucas_u(n, P, Q):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        U_prev_prev, U_prev = 0, 1
        for _ in range(2, n + 1):
            U_current = P * U_prev - Q * U_prev_prev
            U_prev_prev, U_prev = U_prev, U_current
        return U_prev

def lucas_v(n, P, Q):
    if n == 0:
        return 2
    elif n == 1:
        return P
    else:
        V_prev_prev, V_prev = 2, P
        for _ in range(2, n + 1):
            V_current = P * V_prev - Q * V_prev_prev
            V_prev_prev, V_prev = V_prev, V_current
        return V_prev
    
a = 95
b = 126
n = 143
print((lucas_v(16, 2*a,1)*sympy.mod_inverse(2, n)) % n)
print((lucas_u(16, 2*a,1)*b) % n)
