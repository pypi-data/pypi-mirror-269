def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "Cannot divide by zero"
    else:
        return a / b

def modulo(a, b: int):
    if b == 0:
        return "Cannot divide with zero"
    else:
        return a % b

__all__ = ['add', 'subtract', 'multiply', 'divide', 'modulo']