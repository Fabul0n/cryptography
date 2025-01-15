import os
from fastecdsa.curve import Curve
from fastecdsa.point import Point
import random
import sympy

p=115792089210356248762697446949407573530086143415290314195533631308867097853951
a=-3
b=int("5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b", 16)
q=115792089210356248762697446949407573529996955224135760342422259061068512044369
gx=int("6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296", 16)
gy=int("4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5", 16)

curve = Curve(
    name="Some curve",
    p=115792089210356248762697446949407573530086143415290314195533631308867097853951,
    a=-3,
    b=int("5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b", 16),
    q=115792089210356248762697446949407573529996955224135760342422259061068512044369,
    gx=int("6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296", 16),
    gy=int("4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5", 16)
)

G = Point(int("6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296", 16), int("4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5", 16), curve)

class User:
    def __init__(self, name):
        self.name = name
        self.message = None
        self.curve = curve
        self.c = random.randint(1, p-1)
        self.D = self.c * G



    def get_D(self):
        return self.D

    def __repr__(self):
        return self.name + ' ' + str(self.message)
    
    def set_message(self, message):
        self.message = message

    def get_message(self):
        return self.message

    def encrypt_message(self, recipient_D):
        k = random.randint(1, q-1)
        R = k * G
        P = k * recipient_D
        e = self.message * P.x % p
        return R, e

    
    def decrypt_message(self, R, e):
        Q = self.c * R
        m = e * sympy.mod_inverse(Q.x, p) % p
        return m
        

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
                (R, e) = user1.encrypt_message(user2.get_D())
                print(f"Полученное сообщение: {user2.decrypt_message(R, e)}")
                input('Нажмите любую клавишу чтобы продолжить')
            case 4:
                break


if __name__ == '__main__':
    main()
