import re


BROKER_PATTERNS = {

    "rico": [
        r"RICO\s+INVESTIMENTOS",
        r"RICO\s+CORRETORA"
    ],

    "clear": [
        r"CLEAR\s+CORRETORA"
    ],

    "modal": [
        r"MODAL\s+DTVM",
        r"MODALMAIS"
    ],

    "nuinvest": [
        r"EASYNVEST",
        r"NUINVEST",
        r"NU INVEST",
        r"NUBANK",
        r"NU\s+INVEST"
    ],

    "xp": [
        r"XP\s+INVESTIMENTOS"
    ]

}


def detect_broker(text):

    text_upper = text.upper()

    for broker, patterns in BROKER_PATTERNS.items():

        for p in patterns:

            if re.search(p, text_upper):

                return broker

    return "unknown"
