import re
from datetime import datetime

import pdfplumber

from core.models import Trade, Taxes, BrokerageNote
from utils.regex_patterns import DATE_REGEX, TAX_REGEX, IRRF_REGEX, LIQUIDO_REGEX


def parse_number(x):

    x = x.replace(".", "")
    x = x.replace(",", ".")

    return float(x)


class B3Parser:


    def parse(self, pdf_path):

        with pdfplumber.open(pdf_path) as pdf:

            page = pdf.pages[0]

            text = page.extract_text()

            trades = self.extract_trades(text)

            taxes = self.extract_taxes(text)

            date = self.extract_date(text)

            liquido = self.extract_liquido(text)

        return BrokerageNote(
            date=date,
            trades=trades,
            taxes=taxes,
            liquido_para=liquido
        )


    def parse_from_text(self, text):

        trades = self.extract_trades(text)

        taxes = self.extract_taxes(text)

        date = self.extract_date(text)

        return BrokerageNote(
            date=date,
            trades=trades,
            taxes=taxes
        )


    def extract_trades(self, text):

        trades = []

        for line in text.split("\n"):

            line = line.strip()

            if not line.startswith("BOVESPA"):
                continue

            tokens = line.split()

            if len(tokens) < 7:
                continue

            try:

                side = tokens[1]
                asset = tokens[3]

                numbers = []

                for t in tokens:

                    try:
                        numbers.append(parse_number(t))
                    except:
                        pass

                if len(numbers) < 2:
                    continue

                qty = numbers[0]
                price = numbers[1]

                trades.append(
                    Trade(asset, side, qty, price)
                )

            except:
                continue

        return trades


    def extract_taxes(self, text):
    
        taxes = Taxes()
    
        # taxas padrão
        for name, pattern in TAX_REGEX.items():
    
            m = re.search(pattern, text)
    
            if m:
    
                val = abs(parse_number(m.group(1)))
    
                setattr(taxes, name, val)
    
        # IRRF sobre operações
        irrf = self.extract_irrf(text)
    
        taxes.impostos = irrf
    
        taxes.total = (
            taxes.liquidacao
            + taxes.registro
            + taxes.emolumentos
            + taxes.operacional
            + taxes.impostos
        )
    
        return taxes

    
    def extract_date(self, text):
    
        # tentativa 1: regex simples
        m = re.search(r"\d{2}/\d{2}/\d{4}", text)
    
        if m:
            try:
                return datetime.strptime(m.group(0), "%d/%m/%Y")
            except:
                pass
    
        # tentativa 2: procurar após "Data Preg"
        lines = text.split("\n")
    
        for i, line in enumerate(lines):
    
            if "Data Preg" in line and i + 1 < len(lines):
    
                try:
                    return datetime.strptime(lines[i+1].strip(), "%d/%m/%Y")
                except:
                    pass
    
        return None

    def extract_irrf(self, text):
    
        m = re.search(IRRF_REGEX, text)
    
        if m:
            return abs(parse_number(m.group(1)))
    
        return 0
        
    
    def extract_liquido(self, text):
    
        for line in text.split("\n"):
    
            if "Líquido para" in line or "Liquido para" in line:
    
                parts = line.strip().split()
    
                # pegar último token da linha
                val = parts[-1]
    
                try:
                    return parse_number(val)
                except:
                    pass
    
        return None
