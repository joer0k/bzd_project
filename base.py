CONSTS = {"g": 9.81, "p": 1029.3, "b": 1.5, "n": 0.4}
# Константы
# g = 9.81
# p = 1029.3
# b = 1.5
# n = 0.4
# Ввод
H = 20
Vt = 0.00135
t = 20


def useful_power(Vt, temperature):
    return round(CONSTS["p"] * CONSTS["g"] * temperature * Vt / 1000, 2)


def nominal_power(u_p):
    return u_p / CONSTS["n"]


def installed_capacity(nom_power):
    return round(CONSTS["b"] * nom_power), round(CONSTS["b"] * nom_power, 2)

up = useful_power(Vt, t)
print(up)

np = nominal_power(up)
print(np)

ic = installed_capacity(np)
print(ic)
