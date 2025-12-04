import decimal
import math

def my_sin(x):
   
    angle = decimal.Decimal(x)
    decimal.getcontext().prec = 30

    term = angle
    result = term
    angle2 = angle * angle
    n = 1
    prev=result

    test=math.sin(x)
    while n <= 60:
        term = -term * angle2 / (decimal.Decimal(2 * n) * decimal.Decimal(2 * n + 1))
        prev =result
        result += term
        if float(result)==float(prev):
            break;        
        n += 1
    print(x,n,"iterations")
    return float(result)

N = 199
test_points = [2 * math.pi * i / N  for i in range(N)]

mismatches = 0
for x in test_points:
    a = my_sin(x)
    b = math.sin(x)
    if a != b:
        mismatches += 1
        print(f" my_sin = {a} | diff = {abs(a - b)}")
print(f"Несовпадений: {mismatches}")