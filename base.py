

# Константы
g = 9.81
p = 1029.3
b = 1.5
n = 0.4
# Ввод
H = 20
Vt = 0.00135
t = 20


Np = p*g*Vt*t
print(Np)
Ndv =  round((Np/1000),2)/n
print(Ndv)
Nust = b *Ndv
print(round(Nust,1))