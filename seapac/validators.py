import re


def validate(cpf: str) -> bool:

    # Retorno:
    # - Falso, quando o CPF não possuir o formato 999.999.999-99;
    # - Falso, quando o CPF não possuir 11 caracteres numéricos;
    # - Falso, quando os dígitos verificadores forem inválidos;

    if not re.match(r"\d{3}\.\d{3}\.\d{3}-\d{2}", cpf):
        return False

    numbers = [int(digit) for digit in cpf if digit.isdigit()]

    if len(numbers) != 11 or len(set(numbers)) == 1:
        return False

    sum_of_products = sum(a * b for a, b in zip(numbers[0:9], range(10, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10

    if numbers[9] != expected_digit:
        return False

    sum_of_products = sum(a * b for a, b in zip(numbers[0:10], range(11, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10

    if numbers[10] != expected_digit:
        return False

    return True
