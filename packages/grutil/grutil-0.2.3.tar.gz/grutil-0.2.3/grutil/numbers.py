def float2gr(val: float, decimals=2) -> str:
    """1234567.89 => 1.234.567,89"""
    txtfloat = f"{val:,.{decimals}f}"
    return txtfloat.replace(",", "X").replace(".", ",").replace("X", ".")


def float2gr_(val: float, decimals=2) -> str:
    """If val == 0, return empty string"""
    if val == 0:
        return ""
    return float2gr(val, decimals)


def gr2float(strval: str) -> float:
    """Greek decimal string to python decimal number

        1.234.567,89 => 1234567.89

    :param strval: Greek decimal string
    :param decimals: Number of decimal digits
    :return: Python decimal number
    """
    return float(strval.replace(".", "").replace(",", "."))
