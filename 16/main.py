import random
import sympy
import os

def generate_prime(bit_length):
    while True:
        q = sympy.randprime(2**(bit_length-1), 2**bit_length)
        p = 2 * q + 1
        if sympy.isprime(p):
            return p, q

def generate_primitive_root(p, q):
    while True:
        g = random.randint(2, p - 2)
        if pow(g, q, p) != 1:
            return g

bit_length = 256
p, q = generate_prime(bit_length)
g = generate_primitive_root(p, q)

class User:
    def __init__(self, name):
        self.name = name
        self.message = None
        self.private_key = random.randint(2, p - 2)
        self.public_key = pow(g, self.private_key, p)

    def get_public_key(self):
        return self.public_key

    def set_message(self, message):
        self.message = message

    def get_message(self):
        return self.message

    def send_message(self, recipient_d):
        k = random.randint(2, p-2)
        r = pow(g, k, p)
        e = self.message * pow(recipient_d, k, p) % p
        return r, e
    
    def decrypt_message(self, r, e):
        return e * pow(r, p-1-self.private_key, p) % p

    def __repr__(self):
        return self.name + ' ' + str(self.message)
    

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
                encrypted_r, encrypted_e = user1.send_message(user2.get_public_key())
                decrypted_message = user2.decrypt_message(encrypted_r, encrypted_e)
                print(f"Полученное сообщение: {decrypted_message}")
                input('Нажмите любую клавишу чтобы продолжить')
            case 4:
                break


if __name__ == '__main__':
    main()