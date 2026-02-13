import re

# -------- SCANNER --------
TOKEN_TYPES = [
    ('SUJEITO', r'eu'),
    ('VERBO_AUX', r'quero|preciso'),
    ('OBJETO', r'agua|comida'),
    ('VERBO_INF', r'sair|comer'),
    ('CONFIRMACAO', r'sim'),
    ('NEGACAO', r'nao'),
    ('SKIP', r'[ \t\n]+'),
    ('MISMATCH', r'.'),
]

token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_TYPES)

def lexical_analyzer(text):
    tokens = []
    text = text.lower()

    for match in re.finditer(token_regex, text):
        token_type = match.lastgroup
        token_value = match.group(token_type)

        if token_type == 'SKIP':
            continue
        if token_type == 'MISMATCH':
            raise RuntimeError(f"Erro léxico: símbolo inválido '{token_value}'")

        tokens.append((token_type, token_value))
    return tokens


# -------- PARSER --------
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current = tokens[0] if tokens else None

    def advance(self):
        self.pos += 1
        self.current = self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self, expected):
        if self.current and self.current[0] == expected:
            self.advance()
        else:
            raise SyntaxError(f"Esperado {expected}, encontrado {self.current}")

    def parse(self):
        if not self.current:
            raise SyntaxError("Frase vazia")

        if self.current[0] in ['CONFIRMACAO', 'NEGACAO']:
            self.consume(self.current[0])
        elif self.current[0] == 'SUJEITO':
            self.consume('SUJEITO')
            self.consume('VERBO_AUX')
            if self.current and self.current[0] in ['OBJETO', 'VERBO_INF']:
                self.consume(self.current[0])
            else:
                raise SyntaxError("Esperado objeto ou verbo")
        else:
            raise SyntaxError("Estrutura inválida")

        if self.current:
            raise SyntaxError("Tokens extras encontrados")

        return "Frase válida"


# -------- TESTES --------
def testar(frase):
    try:
        tokens = lexical_analyzer(frase)
        parser = Parser(tokens)
        print(frase, "->", parser.parse())
    except Exception as e:
        print(frase, "-> Erro:", e)


testar("eu quero agua")
testar("eu preciso sair")
testar("sim")
testar("nao")
testar("eu agua quero")