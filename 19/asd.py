import sympy

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
    
    def div_with_m(self, divisor, m):
        return CoolNum(self.a*sympy.mod_inverse(divisor, m)%m, self.b*sympy.mod_inverse(divisor, m)%m, self.c)
    
    def div_with_cn(self, other, m):
        conjug = other.conjugate()
        divisor = (conjug * other).get_num()[0]
        return (self * conjug).div_with_m(divisor, m)
    
    def get_num(self):
        return self.a, self.b, self.c
    

print((CoolNum(21, 1, 5).div_with_cn(CoolNum(21, -1, 5), 143)).get_num())