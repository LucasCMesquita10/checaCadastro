# ChecaCadastro — Validador de Formulário de Cadastro

Projeto da disciplina Linguagens Formais e Autômatos.

Lê um arquivo CSV com cadastros (nome, CPF, e-mail, telefone, CEP, data de
nascimento), valida cada campo com uma Expressão Regular e gera um relatório
com os cadastros válidos e o motivo de cada cadastro inválido.

## Instalação e execução
Requer Python 3.8+ (sem dependências externas).

    python main.py                    # valida data/exemplo.csv
    python main.py caminho/dados.csv  # valida outro arquivo
    python main.py --interativo       # digita um cadastro por vez ("sair" encerra)

## Testes
    python -m unittest tests.test_regex -v

## Regenerar os diagramas dos AFNε
    python tools/gerar_afne.py

Gera `docs/diagramas/*.jff` (construção de Thompson) a partir das regex de `padroes.py`
e confere cada autômato contra `re.fullmatch` em milhares de cadeias.

## Estrutura
- `padroes.py` — as 5 Expressões Regulares (fonte única da verdade)
- `validador.py` — validação e extração de campos de uma linha do CSV
- `relatorio.py` — geração do relatório
- `main.py` — entrada/saída e tratamento de erros
- `data/exemplo.csv` — dados de exemplo (válidos, inválidos, linha vazia e malformada)
- `tests/test_regex.py` — 6+ cadeias aceitas e 6+ rejeitadas por expressão (com caso-limite),
  mais verificação exaustiva das faixas de DDD, dia e mês
- `tools/gerar_afne.py` — gera e verifica os AFNε
- `docs/expressoes-regulares.md` — ficha completa de cada ER (alfabeto, linguagem, ER formal,
  AFNε com estados, transições e movimentos ε, testes)
- `docs/diagramas/*.jff` — os 5 AFNε para abrir no JFLAP

## Expressões Regulares (todas usadas com `fullmatch`)
| # | Campo | Padrão no código |
|---|------|------------------|
| 1 | CPF | `[0-9]{3}\.[0-9]{3}\.[0-9]{3}-[0-9]{2}` |
| 2 | E-mail | `[a-zA-Z0-9._-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*\.[a-zA-Z]{2,4}` |
| 3 | Telefone | `\((?:[14689][1-9]\|2[12478]\|3[1234578]\|5[1345]\|7[134579])\) [0-9]{4,5}-[0-9]{4}` |
| 4 | CEP | `[0-9]{5}-[0-9]{3}` |
| 5 | Data de nascimento | `(?:0[1-9]\|[12][0-9]\|3[01])/(?:0[1-9]\|1[0-2])/[0-9]{4}` |

Usamos `[0-9]` em vez de `\d` porque, em Python 3, `\d` também casa dígitos Unicode
(como `٣`), o que ampliaria a linguagem além do alfabeto {0,...,9}.

O telefone aceita apenas os 67 DDDs reais do Brasil; a data aceita dia de 01 a 31 e mês de 01 a 12.

## Tratamento de entradas
- Linha vazia, número de campos diferente de 6 e campo vazio são rejeitados com mensagem clara.
- Espaços no início e no fim de cada campo são removidos antes da validação
  (`" 01310-100 "` é lido como `01310-100`). A ER em si não aceita espaços.
- O campo `nome` só precisa não estar vazio (não há ER para ele); as 5 ER cobrem os demais campos.
- Como `;` é o separador, nenhum campo pode conter `;`.

## Limitações
- CPF: não valida os dígitos verificadores (algoritmo módulo 11), só o formato.
- E-mail: versão simplificada; aceita `a..b@x.com` e blocos de domínio terminados em hífen,
  e não verifica se o domínio existe.
- Telefone: valida o DDD contra os 67 códigos reais, mas não valida o número em si.
- CEP: não valida se o CEP corresponde a um endereço real.
- Data: valida as faixas de dia (01–31) e mês (01–12), mas não cruza dia com mês
  (`31/04/2000` passaria), não trata ano bissexto (`29/02/2023` passaria) e aceita ano `0000`.

## Uso de Inteligência Artificial
A equipe utilizou a ferramenta Claude (Anthropic) como apoio em: revisão das regex de
telefone (DDDs reais) e data (faixas de dia e mês); criação do script `tools/gerar_afne.py`,
que gera os AFNε por construção de Thompson e os verifica contra as regex; geração dos
diagramas `.jff`; reescrita de `docs/expressoes-regulares.md`; ampliação de `tests/test_regex.py`
e deste README.
Todos os integrantes compreendem, explicam e conseguem modificar o conteúdo produzido.

## Contribuições dos integrantes
| Integrante | Contribuição |
|------------|--------------|
| [Benjamin Yuji Suzuki] | [Construção dos modelos no JFLAP, mapeando as expressões regulares para os diagramas de Autômatos Finitos Não Determinísticos (AFNε)] |
| [Felipe de Freitas da Silva] | [Elaboração da apresentação de slides, estruturando a explicação das expressões regulares e a narrativa do projeto] |
| [Jorge Lobato Gonçalves] | [Auxílio na elaboração dos casos de teste e revisão da documentação para garantir a consistência geral das validações] |
| [Lucas Coelho Mesquita] | [Criação e configuração do repositório principal, estruturação da base do código e domínio das regras de negócio do projeto] |
