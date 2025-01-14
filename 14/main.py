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

bit_length = 512
p, q = generate_prime(bit_length)
g = generate_primitive_root(p, q)

class User:
    def __init__(self, name):
        self.name = name
        self.private_key = random.randint(2, p - 2)
        self.public_key = pow(g, self.private_key, p)

    def get_public_key(self):
        return self.public_key

    def get_private_key(self):
        return self.private_key

    def get_secret(self, other_public_key):
        return pow(other_public_key, self.private_key, p)

    def __repr__(self):
        return self.name


def key_exchange(user1: User, user2: User):
    print(f"Публичный ключ пользователя {user1}: {user1.get_public_key()}")
    print(f"Публичный ключ пользователя {user2}: {user2.get_public_key()}")

    print(f"Секрет, который получился у пользователя {user1}: {user1.get_secret(user2.get_public_key())}")
    print(f"Секрет, который получился у пользователя {user2}: {user2.get_secret(user1.get_public_key())}")

def main():
    user_list = [User("Alice"), User("Bob")]
    while 1:
        os.system('cls||clear')
        match int(input((
            '\nДоступные пункты:\n'
            '1 - Вывести список доступных пользователей\n'
            '2 - Добавить нового пользователя\n'
            '3 - Произвести обмен ключами между пользователя\n'
            '4 - Выйти из программы\n'
            'Введите номер пункта: '
        ))):
            case 1:
                for i in range(len(user_list)):
                    print(i, user_list[i])
                input('Нажмите любую клавишу чтобы продолжить')
            case 2:
                user_list.append(User(input('Введите имя пользователя: ')))
            case 3:
                user1_id = int(input("Введите номер пользователя: "))
                user2_id = int(input("Введите номер пользователя: "))
                print("\nНачало обмена ключами")
                key_exchange(user_list[user1_id], user_list[user2_id])
                print("Конец обмена ключами\n")
                input('Нажмите любую клавишу чтобы продолжить')
            case 4:
                break


if __name__ == '__main__':
    main()