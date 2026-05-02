def validate_cpf(cpf):
    """
    Validate CPF format and checksum using Brazilian algorithm.
    """
    if not cpf or not isinstance(cpf, str):
        return False

    # Remove non-numeric characters
    cpf = ''.join(filter(str.isdigit, cpf))

    # Must have exactly 11 digits
    if len(cpf) != 11:
        return False

    # Check if all digits are the same (invalid CPF)
    if cpf == cpf[0] * 11:
        return False

    # Calculate first verification digit
    sum1 = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digit1 = (sum1 * 10) % 11
    if digit1 == 10:
        digit1 = 0

    # Calculate second verification digit
    sum2 = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digit2 = (sum2 * 10) % 11
    if digit2 == 10:
        digit2 = 0

    # Check if calculated digits match the provided ones
    return int(cpf[9]) == digit1 and int(cpf[10]) == digit2
