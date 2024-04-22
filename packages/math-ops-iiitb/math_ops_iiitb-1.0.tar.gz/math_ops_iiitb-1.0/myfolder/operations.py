def add(a: float, b: float) -> float:
    """
    Addition: Returns the sum of two numbers.

    Parameters:
        a (float): The first number.
        b (float): The second number.

    Returns:
        float: The sum of a and b.

    Raises:
        TypeError: If either a or b is not of type int or float.
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Inputs must be of type int or float")
    return a + b

def subtract(a: float, b: float) -> float:
    """
    Subtraction: Returns the difference of two numbers.

    Parameters:
        a (float): The first number.
        b (float): The second number.

    Returns:
        float: The difference between a and b.

    Raises:
        TypeError: If either a or b is not of type int or float.
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Inputs must be of type int or float")
    return a - b

def multiply(a: float, b: float) -> float:
    """
    Multiplication: Returns the product of two numbers.

    Parameters:
        a (float): The first number.
        b (float): The second number.

    Returns:
        float: The product of a and b.

    Raises:
        TypeError: If either a or b is not of type int or float.
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Inputs must be of type int or float")
    return a * b

def divide(a: float, b: float) -> float:
    """
    Division: Returns the result of dividing the first number by the second.

    Parameters:
        a (float): The numerator.
        b (float): The denominator.

    Returns:
        float: The result of a divided by b.

    Raises:
        TypeError: If either a or b is not of type int or float.
        ZeroDivisionError: If the second number (denominator) is zero.
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Inputs must be of type int or float")
    if b == 0:
        raise ZeroDivisionError("Division by zero is undefined")
    return a / b

def modulo(a: float, b: float) -> float:
    """
    Modulo: Returns the remainder of dividing the first number by the second.

    Parameters:
        a (float): The dividend.
        b (float): The divisor.

    Returns:
        float: The remainder of a divided by b.

    Raises:
        TypeError: If either a or b is not of type int or float.
        ZeroDivisionError: If the second number (divisor) is zero.
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Inputs must be of type int or float")
    if b == 0:
        raise ZeroDivisionError("Modulo by zero is undefined")
    return a % b
