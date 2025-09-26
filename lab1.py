def exp_taylor(x, n_terms=20):
 
    SCALE = 10**6
    
    if x < 0:
        result = exp_taylor(-x, n_terms)
        return (SCALE * SCALE) // result  # 1/exp(x)
    
    result = SCALE  
    term = SCALE    
    

    for i in range(1, n_terms):
       
        term = (term * x) // (i * SCALE)
        result += term
        
        if term == 0:
            break
    
    return result

def exp_float_to_fixed(x, scale=10**6):
    return int(x * scale)

def fixed_to_float(value, scale=10**6):

    return value / scale


if __name__ == "__main__":

    SCALE = 10**6
    
    test_values = [0, 1, 2, -1]
    
    for x_float in test_values:
        x_fixed = exp_float_to_fixed(x_float, SCALE)
        
        # Вычисляем экспоненту
        result_fixed = exp_taylor(x_fixed)
        result_float = fixed_to_float(result_fixed, SCALE)
        
        # Сравниваем с математической библиотекой
        import math
        expected = math.exp(x_float)
        


    
    x_fixed = exp_float_to_fixed(1, SCALE)
    
    for n_terms in [20]:
        result_fixed = exp_taylor(x_fixed, n_terms)
        result_float = fixed_to_float(result_fixed, SCALE)
        expected = math.exp(1)
        
        print(f"Членов ряда: {n_terms:2d} -> {result_float:.8f} "
              f"(погрешность: {abs(result_float - expected):.8f})")