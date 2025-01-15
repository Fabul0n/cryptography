class User:
    def __init__(self, name):
        self.name = name
        self.message = None
        self.p = 115792089210356248762697446949407573530086143415290314195533631308867097853951
        self.a = -3
        self.b = int("5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b", 16)
        self.n = 115792089210356248762697446949407573529996955224135760342422259061068512044369
        self.q = self.n
        self.xG = int("6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296", 16)
        self.yG = int("4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5", 16)

asd = User("asd")
print(asd.yG ** 2 % asd.p, (asd.xG**3 + asd.a*asd.xG + asd.b) % asd.p)