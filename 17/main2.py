"""
RSA with digital signature
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

bit_length = 128

class User:
    def __init__(self, name):
        self.name = name
        self.message = None
        self.P = generate_prime(bit_length)
        self.Q = generate_prime(bit_length)
        self.N = self.P * self.Q
        self.phi = (self.P-1)*(self.Q-1)
        while 1:
            c = random.randint(2, self.phi-1)
            if extended_gcd(c, self.phi)[0] == 1:
                self.c = c
                self.d = sympy.mod_inverse(c, self.phi)
                break

    def __repr__(self):
        return self.name + ' ' + str(self.message)
    
    def get_N(self):
        return self.N
    
    def get_d(self):
        return self.d
    
    def set_message(self, message):
        self.message = message

    def get_message(self, message):
        return self.message
    
    def send_message(self, recipient_d, recipient_N):
        return pow(pow(self.message, self.c, self.N), recipient_d, recipient_N)
    
    def decrypt_message(self, encrypted_message, sender_d, sender_N):
        return pow(pow(encrypted_message, self.c, self.N), sender_d, sender_N)
    

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
                print(f"Полученное сообщение: {user2.decrypt_message(user1.send_message(user2.get_d(), user2.get_N()), user1.get_d(), user1.get_N())}")
                input('Нажмите любую клавишу чтобы продолжить')
            case 4:
                break


if __name__ == '__main__':
    main()