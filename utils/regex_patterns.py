DATE_REGEX = r"(\d{2}/\d{2}/\d{4})"

TAX_REGEX = {

"liquidacao": r"Taxa de liquidação\s+([\d,]+)",
"registro": r"Taxa de registro\s+([\d,]+)",
"emolumentos": r"Emolumentos\s+([\d,]+)",
"operacional": r"Corretagem\s+([\d,]+)",
"impostos": r"ISS\s+([\d,]+)"

}