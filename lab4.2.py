def infix_to_rpn(expression: str) -> list:
    precedence = {
        '+': 1, '-': 1,
        '*': 2, '/': 2,
        '^': 3,
        'unary+': 4, 'unary-': 4,
        'sin': 5, 'cos': 5
    }
    postfix_ops = {'!', '++', '--'}

    output = []
    stack = []
    tokens = tokenize(expression)
    
    i = 0
    while i < len(tokens):
        token = tokens[i]
        
        if is_number(token) or (is_identifier(token) and token not in ('sin', 'cos')):
            output.append(token)
            
            while i + 1 < len(tokens) and tokens[i + 1] in postfix_ops:
                output.append(tokens[i + 1])
                i += 1
                
        elif token in ('sin', 'cos'):
            stack.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            
            if not stack:
                raise ValueError("Несбалансированные скобки")
            
            stack.pop()
            
            if stack and stack[-1] in ('sin', 'cos'):
                output.append(stack.pop())
            
            while i + 1 < len(tokens) and tokens[i + 1] in postfix_ops:
                output.append(tokens[i + 1])
                i += 1
        elif token in '+-':
            if (i == 0 or tokens[i-1] == '(' or 
                tokens[i-1] in '+-*/^'):
                unary_op = 'unary+' if token == '+' else 'unary-'
                stack.append(unary_op)
            else:
                while (stack and stack[-1] != '(' and
                       stack[-1] in precedence and
                       precedence[stack[-1]] >= precedence[token]):
                    output.append(stack.pop())
                stack.append(token)
        elif token in '*/^':
            while (stack and stack[-1] != '(' and
                   stack[-1] in precedence and
                   precedence[stack[-1]] >= precedence[token]):
                output.append(stack.pop())
            stack.append(token)
        elif token in postfix_ops:
            raise ValueError(f"Постфиксный оператор '{token}' без операнда")
        else:
            raise ValueError(f"Неизвестный токен: {token}")
        
        i += 1

    while stack:
        op = stack.pop()
        if op == '(':
            raise ValueError("Несбалансированные скобки")
        output.append(op)

    return output

def tokenize(expr: str) -> list:
    tokens = []
    i = 0
    keywords = ['sin', 'cos']
    
    while i < len(expr):
        if expr[i].isspace():
            i += 1
            continue
            
        matched = False
        for kw in sorted(keywords, key=len, reverse=True):
            if expr[i:].startswith(kw):
                if (i + len(kw) >= len(expr) or 
                    not expr[i + len(kw)].isalnum()):
                    tokens.append(kw)
                    i += len(kw)
                    matched = True
                    break
        if matched:
            continue
            
        if expr[i:i+2] == '++':
            tokens.append('++')
            i += 2
            continue
        if expr[i:i+2] == '--':
            tokens.append('--')
            i += 2
            continue
        if expr[i] == '!':
            tokens.append('!')
            i += 1
            continue
            
        if expr[i].isdigit() or expr[i] == '.':
            j = i
            dot_count = 0
            while j < len(expr) and (expr[j].isdigit() or expr[j] == '.'):
                if expr[j] == '.':
                    dot_count += 1
                    if dot_count > 1:
                        raise ValueError(f"Некорректное число: несколько точек")
                j += 1
            tokens.append(expr[i:j])
            i = j
            
        elif expr[i].isalpha():
            j = i
            while j < len(expr) and expr[j].isalnum():
                j += 1
            tokens.append(expr[i:j])
            i = j
            
        elif expr[i] in '+-*/^()':
            tokens.append(expr[i])
            i += 1
        else:
            raise ValueError(f"Недопустимый символ: {expr[i]}")
    
    return tokens

def is_number(token: str) -> bool:
    try:
        float(token)
        return True
    except ValueError:
        return False

def is_identifier(token: str) -> bool:
    return token.isalpha() or (token[0].isalpha() and token.isalnum())

def validate_expression(tokens):
    if not tokens:
        raise ValueError("Пустое выражение")
    
    balance = 0
    for token in tokens:
        if token == '(':
            balance += 1
        elif token == ')':
            balance -= 1
            if balance < 0:
                raise ValueError("Несбалансированные скобки")
    if balance != 0:
        raise ValueError("Несбалансированные скобки")

    i = 0
    while i < len(tokens):
        token = tokens[i]
        
        if token in ('++', '--'):
            if i == 0:
                raise ValueError(f"Оператор '{token}' не может быть в начале выражения")
            
            prev_token = tokens[i - 1]
            if is_number(prev_token):
                raise ValueError(f"Оператор '{token}' не может применяться к числовому литералу '{prev_token}'")
        
        if token in '+-' and i > 0 and tokens[i-1] in ('++', '--'):
            if i == 0 or tokens[i-1] == '(' or tokens[i-1] in '+-*/^' or tokens[i-1] in ('sin', 'cos', '!', '++', '--'):
                raise ValueError(f"Унарный оператор '{token}' не может стоять сразу после постфиксного оператора '{tokens[i-1]}'")
        
        if token in '+-' and i > 0:
            if (tokens[i-1] == '(' or tokens[i-1] in '+-*/^' or 
                tokens[i-1] in ('sin', 'cos', '!', '++', '--')):
                if i > 1 and tokens[i-1] in '+-' and (
                    tokens[i-2] == '(' or tokens[i-2] in '+-*/^' or 
                    tokens[i-2] in ('sin', 'cos', '!', '++', '--')):
                    raise ValueError(f"Несколько унарных операторов подряд: '{tokens[i-1]}{token}'")
        
        if token == '(':
            if i > 0:
                prev_token = tokens[i-1]
                if (is_number(prev_token) or is_identifier(prev_token) or prev_token == ')'):
                    if prev_token not in ('sin', 'cos'):
                        raise ValueError(f"Перед '(' должен быть оператор, но найден '{prev_token}'")
        
        if token == ')':
            if i + 1 < len(tokens):
                next_token = tokens[i + 1]
                if (is_number(next_token) or is_identifier(next_token) or 
                    next_token == '(' or next_token in ('sin', 'cos')):
                    raise ValueError(f"После ')' должен быть оператор, но найден '{next_token}'")
        
        if (is_number(token) or is_identifier(token)) and token not in ('sin', 'cos'):
            if i + 1 < len(tokens):
                next_token = tokens[i + 1]
                if is_number(next_token) or is_identifier(next_token):
                    raise ValueError(f"После '{token}' должен быть оператор, но найден '{next_token}'")
                elif next_token in ('sin', 'cos'):
                    raise ValueError(f"После '{token}' должен быть оператор, но найден '{next_token}'")
        
        if token in ('sin', 'cos'):
            if i + 1 >= len(tokens):
                raise ValueError(f"Оператор '{token}' должен иметь операнд")
            next_token = tokens[i + 1]
            if not (is_identifier(next_token) or is_number(next_token) or next_token == '('):
                raise ValueError(f"После '{token}' должен быть операнд или '(', но найден '{next_token}'")
            
            if is_identifier(next_token) or is_number(next_token):
                i += 1
                while i + 1 < len(tokens) and tokens[i + 1] in ('!', '++', '--'):
                    i += 1
            elif next_token == '(':
                j = i + 2
                bracket_balance = 1
                while j < len(tokens):
                    if tokens[j] == '(':
                        bracket_balance += 1
                    elif tokens[j] == ')':
                        bracket_balance -= 1
                        if bracket_balance == 0:
                            break
                    j += 1
                
                if j >= len(tokens) or tokens[j] != ')':
                    raise ValueError(f"Не закрыта скобка после '{token}'")
                
                if j == i + 2:
                    raise ValueError(f"Функция '{token}' должна иметь аргумент")
                i = j
        
        if token in ('!', '++', '--'):
            if i == 0:
                raise ValueError(f"Оператор '{token}' не может быть в начале выражения")
            
            prev_token = tokens[i - 1]
            if not (is_number(prev_token) or is_identifier(prev_token) or prev_token == ')' or prev_token in ('!', '++', '--')):
                raise ValueError(f"Оператор '{token}' должен стоять после операнда, но перед ним '{prev_token}'")
            
            if token in ('++', '--') and is_number(prev_token):
                raise ValueError(f"Оператор '{token}' не может применяться к числовому литералу")
            
            if i + 1 < len(tokens):
                next_token = tokens[i + 1]
                if (is_number(next_token) or is_identifier(next_token) or 
                    next_token in ('sin', 'cos') or next_token == '('):
                    if next_token not in ('!', '++', '--'):
                        raise ValueError(f"После оператора '{token}' должен быть бинарный оператор, но найден '{next_token}'")
        
        if token in '+-*/^':
            if token in '+-' and (i == 0 or tokens[i-1] in '+-*/^(' or tokens[i-1] in ('sin', 'cos', '!', '++', '--')):
                pass
            else:
                if i == 0:
                    raise ValueError(f"Оператор '{token}' должен иметь левый операнд")
                
                prev_token = tokens[i - 1]
                if (prev_token in '+-*/^(' or 
                    (prev_token in ('sin', 'cos') and prev_token not in ('!', '++', '--'))):
                    raise ValueError(f"Перед оператором '{token}' должен быть операнд, но найден '{prev_token}'")
                
                if i + 1 >= len(tokens):
                    raise ValueError(f"После оператора '{token}' должен быть правый операнд")
                
                next_token = tokens[i + 1]
                if next_token in '*/^)':
                    raise ValueError(f"После оператора '{token}' должен быть операнд, но найден '{next_token}'")
                elif next_token == '-':
                    if not (tokens[i-1] in '+-*/^(' or tokens[i-1] in ('sin', 'cos', '!', '++', '--')):
                        raise ValueError(f"После оператора '{token}' должен быть операнд, но найден '{next_token}'")
        
        i += 1

def infix_to_rpn_with_validation(expression: str) -> list:
    tokens = tokenize(expression)
    
    for i, token in enumerate(tokens):
        if token in ('++', '--') and i > 0:
            prev_token = tokens[i-1]
            if is_number(prev_token):
                raise ValueError(f"Оператор '{token}' не может применяться к числовому литералу '{prev_token}'")
    
    validate_expression(tokens)
    return infix_to_rpn(expression)

def testlt(test):
    try:
        result = infix_to_rpn_with_validation(test)
        print(f"{test} : {result}")
    except ValueError as e:
        print(f"{test} : ОШИБКА: {e}")

print("=== Основные тесты ===")
test1 = '3 + 4 * 2 / ( 1 - 5 ) ^ 2 ^ 3'
test2 = '-5 + 3'
test3 = 'sin(-x) + cos(y)'
test4 = 'a++'
test5 = '(n)!'
test6 = 'x + !(4) * y'
test7 = 'sin(cos(z))'
test8 = '!(!(k))'
test9 = '--b'
test10 = '++x + --y'

testlt(test1)
testlt(test2)
testlt(test3)
testlt(test4)
testlt(test5)
testlt(test6)
testlt(test7)
testlt(test8)
testlt(test9)


print("\n")
testlt('(3 ++ 4) * 2')
testlt('sin(3.14+++/1) + cos(0)')
testlt('5+! + 3++')
testlt('sin(x)')
testlt('sin x')
testlt('sin x ++')
testlt('sin x!')
testlt('n!')