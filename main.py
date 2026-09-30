"""ChecaCadastro - validador de formulário de cadastro.

Uso:
  python main.py [arquivo.csv]     valida um arquivo (padrão: data/exemplo.csv)
  python main.py --interativo      testa um cadastro por vez, campo a campo
"""
import sys
from validador import validar_linha, LINHA_VAZIA, CAMPOS
from relatorio import gerar_relatorio


def processar_arquivo(caminho):
    try:
        with open(caminho, encoding="utf-8-sig") as f:
            linhas = f.readlines()
    except FileNotFoundError:
        print(f"Erro: arquivo '{caminho}' não encontrado.")
        return 1
    except UnicodeDecodeError:
        print(f"Erro: '{caminho}' não está em UTF-8. "
              "Salve o CSV com a codificação UTF-8 e tente novamente.")
        return 1
    except OSError as e:
        print(f"Erro ao ler '{caminho}': {e}")
        return 1
    if not linhas:
        print(f"Erro: o arquivo '{caminho}' está vazio.")
        return 1

    registros, erros, vazias = [], [], 0
    for numero, linha in enumerate(linhas, start=1):
        registro, erro = validar_linha(linha, numero)
        if registro:
            registros.append(registro)
        elif erro == LINHA_VAZIA:
            vazias += 1
        else:
            erros.append((numero, erro))
    print(gerar_relatorio(registros, erros, vazias, len(linhas)))
    return 0


def modo_interativo():
    print(f"Digite os campos separados por ';' na ordem: {', '.join(CAMPOS)}")
    print("('sair' para encerrar)")
    numero = 0
    while True:
        try:
            linha = input("cadastro> ")
        except EOFError:
            break
        if linha.strip().lower() == "sair":
            break
        numero += 1
        registro, erro = validar_linha(linha, numero)
        print("  VÁLIDO" if registro else f"  INVÁLIDO: {erro}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--interativo":
        modo_interativo()
    else:
        sys.exit(processar_arquivo(sys.argv[1] if len(sys.argv) > 1 else "data/exemplo.csv"))