import re
from datetime import datetime

from utils.pdf_text import extract_text
from utils.trade_parser import parse_trade_line
from utils.regex_patterns import DATE_REGEX, TAX_REGEX

from core.models import Trade, Taxes, BrokerageNote


class B3Parser:


    def parse(self, pdf_path):

        text = extract_text(pdf_path)

        return self.parse_from_text(text)


    def parse_from_text(self, text):

        trades = []

        for line in text.split("\n"):

            parsed = parse_trade_line(line)

            if parsed:

                trades.append(
                    Trade(
                        parsed["asset"],
                        parsed["side"],
                        parsed["qty"],
                        parsed["price"]
                    )
                )

        # data da nota
        date_match = re.search(DATE_REGEX, text)

        date = None

        if date_match:
            date = datetime.strptime(date_match.group(1), "%d/%m/%Y")

        # taxas
        taxes = Taxes()

        for name,pattern in TAX_REGEX.items():

            m = re.search(pattern, text)

            if m:

                val = float(m.group(1).replace(",", "."))

                setattr(taxes,name,val)

        taxes.total = (
            taxes.liquidacao
            + taxes.registro
            + taxes.emolumentos
            + taxes.operacional
            + taxes.impostos
        )

        return BrokerageNote(
            date=date,
            trades=trades,
            taxes=taxes
        )