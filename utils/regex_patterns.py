DATE_REGEX = r"Data\s*Preg[aã]o\s*(\d{2}/\d{2}/\d{4})"

IRRF_REGEX = r"I\.?R\.?R\.?F\.?[^\d]*?([\d.,]+)"

LIQUIDO_REGEX = r"L[ií]quido\s+para.*?(-?[\d.,]+)"

TAX_REGEX = {

"liquidacao": r"Taxa\s+de\s+Liquida[cç][aã]o\s+(-?[\d.,]+)",
"registro": r"Taxa\s+de\s+Registro\s+(-?[\d.,]+)",
"emolumentos": r"Emolumentos\s+(-?[\d.,]+)",
"operacional": r"(?:Corretagem|Taxa\s+Operacional)\s+(-?[\d.,]+)",
"impostos": r"ISS[^\d]*(-?[\d.,]+)"

}
