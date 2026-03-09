DATE_REGEX = r"Data\s*Preg[aã]o\s*(\d{2}/\d{2}/\d{4})"

IRRF_REGEX = r"I\.R\.R\.F.*?([\d,]+)$"

TAX_REGEX = {

"liquidacao": r"Taxa de Liquidação\s+(-?[\d.,]+)",
"registro": r"Taxa de Registro\s+(-?[\d.,]+)",
"emolumentos": r"Emolumentos\s+(-?[\d.,]+)",
"operacional": r"Corretagem\s+(-?[\d.,]+)",
"impostos": r"ISS.*?\s(-?[\d.,]+)"

}
