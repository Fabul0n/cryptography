import sympy
import random
import os
import math
import numpy as np


def generate_prime(bit_length):
    return sympy.randprime(2**(bit_length-1), 2**bit_length)

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = extended_gcd(b % a, a)
        return g, y - (b // a) * x, x

bit_length = 1024

def matrix_mult_mod(a, b, mod):
    return [
        [(a[0][0] * b[0][0] + a[0][1] * b[1][0]) % mod,
         (a[0][0] * b[0][1] + a[0][1] * b[1][1]) % mod],
        [(a[1][0] * b[0][0] + a[1][1] * b[1][0]) % mod,
         (a[1][0] * b[0][1] + a[1][1] * b[1][1]) % mod],
    ]

def matrix_pow_mod(mat, power, mod):
    result = [[1, 0], [0, 1]]
    while power > 0:
        if power % 2 == 1:
            result = matrix_mult_mod(result, mat, mod)
        mat = matrix_mult_mod(mat, mat, mod)
        power = power // 2
    return result

def lucas_u(n, P, Q, mod):
    if n == 0:
        return 0
    elif n == 1:
        return 1 % mod
    else:
        mat = [[0, 1], [-Q, P]]
        mat_n = matrix_pow_mod(mat, n - 1, mod)
        return (mat_n[1][0] * 0 + mat_n[1][1] * 1) % mod

def lucas_v(n, P, Q, mod):
    if n == 0:
        return 2 % mod
    elif n == 1:
        return P % mod
    else:
        mat = [[0, 1], [-Q, P]]
        mat_n = matrix_pow_mod(mat, n - 1, mod)
        return (mat_n[1][0] * 2 + mat_n[1][1] * P) % mod

class CoolNum:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def conjugate(self):
        return CoolNum(self.a, -self.b, self.c)
    
    def __mul__(self, other):
        return CoolNum(self.a * other.a + self.b * other.b * self.c, self.a * other.b + self.b * other.a, self.c)
    
    def add_a(self, a):
        return CoolNum(self.a + a, self.b, self.c)

    def add_b(self, b):
        return CoolNum(self.a, self.b + b, self.c)
    
    def get_num(self):
        return self.a, self.b, self.c

class User:
    def __init__(self, name):
        self.name = name
        self.message = None
        self.p = generate_prime(bit_length)
        self.q = generate_prime(bit_length)
        self.n = self.p * self.q
        f = 0
        for c in range(1, self.n):
            delta_p = sympy.legendre_symbol(c, self.p)
            delta_q = sympy.legendre_symbol(c, self.q)
            if delta_p % 4 == (-self.p) % 4:
                if delta_q % 4 == (-self.q) % 4:
                    for s in range(1, self.n):
                        if sympy.jacobi_symbol(s**2 - c, self.n) == -1 and math.gcd(s, self.n) == 1:
                            m = (self.p - delta_p)*(self.q - delta_q)//4
                            for d in range(2, self.n):
                                if math.gcd(d, m) == 1:
                                    e = (m+1)//2*sympy.mod_inverse(d, m)
                                    self.c = c
                                    self.s = s
                                    self.m = m
                                    self.d = d
                                    self.e = e
                                    f = 1
                                if f:
                                    break
                        if f: break
            if f:
                break
        if not f:
            raise Exception("e was not found")

                            

    def __repr__(self):
        return self.name + ' ' + str(self.message)
    
    def set_message(self, message):
        self.message = message

    def get_message(self):
        return self.message

    def get_n(self):
        return self.n
    
    def get_e(self):
        return self.e
    
    def get_c(self):
        return self.c
    
    def get_s(self):
        return self.s
    
    def encrypt_message(self, recipient_n, recipient_e, recipient_c, recipients_s):
        w = self.message
        if sympy.jacobi_symbol(w**2 - recipient_c, recipient_n) == 1:
            b1 = 0
            gamma = CoolNum(w, 1, recipient_c)
        else:
            b1 = 1
            gamma = CoolNum(w, 1, recipient_c)*CoolNum(recipients_s, 1, recipient_c)
        
        (gamma_a, gamma_b, smth) = (gamma*gamma).get_num()
        (denomin, smth, smth2) = (gamma * gamma.conjugate()).get_num()
        denomin_inv = sympy.mod_inverse(denomin, recipient_n)
        gamma_a = (gamma_a * denomin_inv) % recipient_n
        gamma_b = (gamma_b * denomin_inv) % recipient_n
        alpha = CoolNum(gamma_a, gamma_b, recipient_c)
        b2 = gamma_a % 2
        E = ((lucas_v(recipient_e, 2*gamma_a, 1, recipient_n) * sympy.mod_inverse(2, recipient_n) % recipient_n) * sympy.mod_inverse((gamma_b*lucas_u(recipient_e, 2*gamma_a, 1, recipient_n)) % recipient_n, recipient_n)) % recipient_n
        return (E, b1, b2)

    
    def decrypt_message(self, message, b1, b2):
        cooln = CoolNum(message, 1, self.c)
        (denomin, smth, smth2) = (cooln * cooln.conjugate()).get_num()
        (cooln_a, cooln_b, smth) = (cooln * cooln).get_num()
        denomin_inv = sympy.mod_inverse(denomin, self.n)
        cooln_a = (cooln_a * denomin_inv) % self.n
        cooln_b = (cooln_b * denomin_inv) % self.n
        alpha_2ed_a = ((lucas_v(self.d, 2*cooln_a, 1, self.n) * sympy.mod_inverse(2, self.n)) % self.n)
        alpha_2ed_b = ((cooln_b * lucas_u(self.d, 2*cooln_a, 1, self.n)) % self.n)
        if b2 == 1 and alpha_2ed_a % 2 == 0:
            alpha_2ed_a = (-alpha_2ed_a) % self.n
            alpha_2ed_b = (-alpha_2ed_b) % self.n
        elif b2 == 0 and alpha_2ed_a % 2 == 1:
            alpha_2ed_a = (-alpha_2ed_a) % self.n
            alpha_2ed_b = (-alpha_2ed_b) % self.n
        
        if b1 != 0:
            tmpcn = CoolNum(self.s, -1, self.c)
            (denomin, smth, smth2) = (tmpcn * tmpcn.conjugate()).get_num()
            denomin_inv = sympy.mod_inverse(denomin, self.n)
            (tmpcn_a, tmpcn_b, smth) = (tmpcn * tmpcn).get_num()
            tmpcn_a = (tmpcn_a * denomin_inv) % self.n
            tmpcn_b = (tmpcn_b * denomin_inv) % self.n
            alpha_shtrih = CoolNum(alpha_2ed_a, alpha_2ed_b, self.c)*CoolNum(tmpcn_a, tmpcn_b, self.c)
        else:
            alpha_shtrih = CoolNum(alpha_2ed_a, alpha_2ed_b, self.c)
        
        (alpha_shtrih_a, alpha_shtrih_b, smth) = alpha_shtrih.get_num()
        (denomin, smth, smth2) = (CoolNum(alpha_shtrih_a-1, alpha_shtrih_b, self.c) * CoolNum(alpha_shtrih_a-1, alpha_shtrih_b, self.c).conjugate()).get_num()
        denomin_inv = sympy.mod_inverse(denomin, self.n)
        (smth, res, smth2) = (CoolNum(alpha_shtrih_a+1, alpha_shtrih_b, self.c) * CoolNum(alpha_shtrih_a-1, alpha_shtrih_b, self.c).conjugate()).get_num()
        res *= denomin_inv
        res *= self.c
        return res % self.n
        

def main():
    user_list = [User("Alice"), User("Bob")]
    user_list[0].set_message(1234567899)
    user_list[1].set_message(9987654321)
    while 1:
        os.system('cls||clear')
        match int(input((
            '\nДоступные пункты:\n'
            '1 - Вывести список доступных пользователей\n'
            '2 - Добавить нового пользователя\n'
            '3 - Произвести общение между пользователями\n'
            '4 - Выйти из программы\n'
            'Введите номер пункта: '
        ))):
            case 1:
                for i in range(len(user_list)):
                    print(i, user_list[i])
                input('Нажмите любую клавишу чтобы продолжить')
            case 2:
                user_list.append(User(input('Введите имя пользователя: ')))
                user_list[-1].set_message(int(input('Введите сообщение, которое будет отправлять пользователь (число): ')))
            case 3:
                user1_id = int(input("Введите номер пользователя - отправителя: "))
                user2_id = int(input("Введите номер пользователя - получателя: "))
                user1 = user_list[user1_id]
                user2 = user_list[user2_id]
                (encrypted_mes, b1, b2) = user1.encrypt_message(user2.get_n(), user2.get_e(), user2.get_c(), user2.get_s())
                print(f"Полученное сообщение: {user2.decrypt_message(encrypted_mes, b1, b2)}")
                input('Нажмите любую клавишу чтобы продолжить')
            case 4:
                break


if __name__ == '__main__':
    main()