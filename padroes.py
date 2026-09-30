r"""As 5 Expressões Regulares do ChecaCadastro.

Todas aplicadas com fullmatch(): a cadeia INTEIRA precisa pertencer à
linguagem, para que expressão formal, código, testes e AFNε representem
exatamente a mesma linguagem.

Usamos [0-9] em vez de \d: em Python 3, \d também casa dígitos Unicode (ex.: '٣'),
o que faria a linguagem maior que o alfabeto {0,...,9} documentado.
"""
import re

PADROES = {
    # 1. CPF no formato xxx.xxx.xxx-xx (não valida dígitos verificadores)
    "CPF": re.compile(r"[0-9]{3}\.[0-9]{3}\.[0-9]{3}-[0-9]{2}"),
    # 2. E-mail simplificado: usuario@dominio(.subdominio)*.tld (tld de 2 a 4 letras)
    "EMAIL": re.compile(r"[a-zA-Z0-9._-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*\.[a-zA-Z]{2,4}"),
    # 3. Telefone brasileiro: DDD válido (67 códigos reais), 8 ou 9 dígitos, hífen, 4 dígitos
    "TELEFONE": re.compile(r"\((?:[14689][1-9]|2[12478]|3[1234578]|5[1345]|7[134579])\) [0-9]{4,5}-[0-9]{4}"),
    # 4. CEP no formato xxxxx-xxx
    "CEP": re.compile(r"[0-9]{5}-[0-9]{3}"),
    # 5. Data no formato dd/mm/aaaa, com dia 01-31 e mês 01-12 válidos (não cruza dia com mês/ano)
    "DATA": re.compile(r"(?:0[1-9]|[12][0-9]|3[01])/(?:0[1-9]|1[0-2])/[0-9]{4}"),
}


def valida(nome, texto):
    """True se a cadeia inteira pertence à linguagem da expressão `nome`."""
    return PADROES[nome].fullmatch(texto) is not None