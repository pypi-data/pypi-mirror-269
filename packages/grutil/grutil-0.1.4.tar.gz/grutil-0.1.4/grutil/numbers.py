def float2grnum(val: float, decimals=2) -> str:
    """1234567.89 => 1.234.567,89"""
    txtfloat = f"{val:,.{decimals}f}"
    return txtfloat.replace(",", "X").replace(".", ",").replace("X", ".")


def float2grnum_or_space(val: float, decimals=2) -> str:
    if val == 0:
        return ""
    return float2grnum(val, decimals)


def grnum2float(strval) -> float:
    """Greek decimal string to python decimal number

    :param strval: Greek decimal string
    :param decimals: Number of decimal digits
    :return: Python decimal number
    """
    return float(strval.replace(".", "").replace(",", "."))
