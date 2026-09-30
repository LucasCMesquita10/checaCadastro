"""Validação de uma linha de cadastro (CSV separado por ';')."""
from padroes import valida

CAMPOS = ["nome", "cpf", "email", "telefone", "cep", "data_nascimento"]
CAMPOS_REGEX = {"cpf": "CPF", "email": "EMAIL", "telefone": "TELEFONE",
                "cep": "CEP", "data_nascimento": "DATA"}
LINHA_VAZIA = "linha vazia"


def validar_linha(linha, numero):
    """Retorna (registro, None) se válida, ou (None, motivo) se não for."""
    linha = linha.rstrip("\r\n")
    if not linha.strip():
        return None, LINHA_VAZIA

    partes = linha.split(";")
    if len(partes) != len(CAMPOS):
        return None, f"esperados {len(CAMPOS)} campos, encontrados {len(partes)}"

    registro = dict(zip(CAMPOS, (p.strip() for p in partes)))

    if not registro["nome"]:
        return None, "campo 'nome' vazio"

    for campo, nome_regex in CAMPOS_REGEX.items():
        valor = registro[campo]
        if not valor:
            return None, f"campo '{campo}' vazio"
        if not valida(nome_regex, valor):
            return None, f"campo '{campo}' inválido: {valor!r}"

    registro["numero"] = numero
    return registro, None