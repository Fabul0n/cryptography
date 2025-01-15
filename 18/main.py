"""
Encryption/Decryption
"""

import random
import sympy
import os

def generate_prime(bit_length):
    return sympy.randprime(2**(bit_length-1), 2**bit_length)

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = extended_gcd(b % a, a)
        return g, y - (b // a) * x, x

bit_length = 1024

class User:
    def __init__(self, name):
        self.name = name
        self.message = None
        self.p = generate_prime(bit_length)
        while self.p % 4 != 3:
            self.p = generate_prime(bit_length)
        self.q = generate_prime(bit_length)
        while self.p == self.q or self.q % 4 != 3:
            self.q = generate_prime(bit_length)
        self.n = self.p * self.q

    def __repr__(self):
        return self.name + ' ' + str(self.message)
    
    def set_message(self, message):
        self.message = message

    def get_message(self):
        return self.message

    def get_n(self):
        return self.n
    
    def encrypt_message(self, recipient_n):
        return pow(self.message, 2, recipient_n)
    
    def decrypt_message(self, message):
        mp = pow(message, (self.p+1)//4, self.p)
        mq = pow(message, (self.q+1)//4, self.q)
        (g, yp, yq) = extended_gcd(self.p, self.q)
        r1 = (yp*self.p*mq + yq*self.q*mp) % self.n
        r2 = self.n - r1
        r3 = (yp*self.p*mq - yq*self.q*mp) % self.n
        r4 = self.n - r3
        return r1, r2, r3, r4
    

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
                print(f"Полученное сообщение: {user2.decrypt_message(user1.encrypt_message(user2.get_n()))}")
                input('Нажмите любую клавишу чтобы продолжить')
            case 4:
                break


if __name__ == '__main__':
    main()