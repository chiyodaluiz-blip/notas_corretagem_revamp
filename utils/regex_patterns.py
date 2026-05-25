DATE_REGEX = r"Data\s*Preg[aã]o\s*(\d{2}/\d{2}/\d{4})"

IRRF_REGEX = r"I\.R\.R\.F.*?-?R\$\s*([\d.,]+)"

LIQUIDO_REGEX = r"L[ií]quido\s+para.*?(-?[\d.,]+)"

TAX_REGEX = {
    "liquidacao": r"Taxa de Liquidação/CCP\s+-?R\$\s*([\d.,]+)",

    "registro": r"Taxa de Registro\s+-?R\$\s*([\d.,]+)",

    "emolumentos": r"Emolumentos\s+-?R\$\s*([\d.,]+)",

    "operacional": r"Corretagem\s+-?R\$\s*([\d.,]+)",

    "impostos": r"ISS.*?-?R\$\s*([\d.,]+)"
}
