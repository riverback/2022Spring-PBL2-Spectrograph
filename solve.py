import sympy
from sympy import solve, acos, Symbol

x = Symbol('x')
result = solve(acos(0.4654469)-x)
print(result)
print(float(sympy.pi))