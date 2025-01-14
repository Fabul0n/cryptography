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
        self.other_p = None
        self.cB = None
        self.dB = None
        self.p = generate_prime(bit_length)
        while 1:
            cA = random.randint(2, self.p-2)
            if extended_gcd(cA, self.p-1)[0] == 1:
                self.cA = cA
                self.dA = sympy.mod_inverse(cA, self.p-1)
                break

    def __repr__(self):
        return self.name + ' ' + str(self.message)
    
    def get_other_p(self, p):
        self.other_p = p
        while 1:
            cB = random.randint(2, self.other_p-2)
            if extended_gcd(cB, self.other_p-1)[0] == 1:
                self.cB = cB
                self.dB = sympy.mod_inverse(cB, self.other_p-1)
                break

    def send_p(self):
        return self.p

    def set_message(self, message):
        self.message = message
    
    def send_x1(self):
        return pow(self.message, self.cA, self.p)
    
    def get_x1_send_x2(self, x1):
        return pow(x1, self.cB, self.other_p)
    
    def get_x2_send_x3(self, x2):
        return pow(x2, self.dA, self.p)
    
    def get_x3_return_message(self, x3):
        return pow(x3, self.dB, self.other_p)
    

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
                user2.get_other_p(user1.send_p())
                x1 = user1.send_x1()
                x2 = user2.get_x1_send_x2(x1)
                x3 = user1.get_x2_send_x3(x2)
                x4 = user2.get_x3_return_message(x3)
                print(f"Полученное сообщение: {x4}")
                input('Нажмите любую клавишу чтобы продолжить')
            case 4:
                break


if __name__ == '__main__':
    main()