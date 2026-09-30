# Fichas das Expressões Regulares — ChecaCadastro

Notação formal (conforme guia do professor): `r|s` união · `rs` concatenação ·
`r*` fecho de Kleene · `r+` fecho positivo · `r?` opcionalidade `(r|ε)` ·
`(r)` agrupamento · `[abc]`/`[0-9]` classe/intervalo (abreviação de união) ·
`r{m}` m cópias · `r{m,n}` união de `r^m` até `r^n`.

`D = (0|1|2|...|9)`; `L = (a|...|z|A|...|Z)`.

Todas as ER são aplicadas com `re.fullmatch()`: a cadeia inteira precisa pertencer à linguagem, então não há âncoras `^`/`$` nos padrões. Usamos `[0-9]` em vez de `\d` porque, em Python 3, `\d` também casa dígitos Unicode (como `٣`), o que tornaria a linguagem maior que o alfabeto `{0,...,9}`. Não há retrorreferências, lookaround nem recursão.
Os AFNε foram construídos pela **construção de Thompson** (`tools/gerar_afne.py`), que gera os
arquivos `docs/diagramas/*.jff` e confere cada autômato contra a regex em milhares de cadeias.
Nos diagramas, uma classe de símbolos (`[0-9]`, `[14689]`...) aparece como dois estados ligados por
várias transições paralelas, uma por símbolo. No JFLAP, o movimento ε é a transição de rótulo vazio (λ).
Nas tabelas abaixo, `—{0-9}→` indica um conjunto de transições paralelas, uma por símbolo.

---

## ER-01 — CPF
| Campo | Conteúdo |
|---|---|
| **Identificação** | ER-01, `CPF`. Reconhece o número de CPF no formato `xxx.xxx.xxx-xx`. |
| **Alfabeto (Σ)** | `{0,...,9} ∪ {., -}` |
| **Linguagem L** | 9 dígitos em 3 blocos de 3 separados por `.`, seguidos de `-` e mais 2 dígitos (11 dígitos no total). |
| **ER formal** | `D D D . D D D . D D D - D D` |
| **Sintaxe implementada** | `[0-9]{3}\.[0-9]{3}\.[0-9]{3}-[0-9]{2}` |
| **Equivalência** | `[0-9]` = `D`, abreviação da união `0\|1\|...\|9` (usamos `[0-9]` e não `\d`, que em Python também casa dígitos Unicode); `{3}` e `{2}` = concatenação de 3 e 2 cópias de `D`; `\.` = literal `.` (escapado, pois `.` solto casaria qualquer símbolo); `-` = literal. |
| **AFNε** | Só concatenação: 14 átomos (11 de dígito, 2 de `.`, 1 de `-`), cada um com 2 estados, ligados por 13 movimentos ε. Não há ramificação de decisão; cada átomo de dígito tem 10 transições paralelas (0 a 9). Total: **28 estados**, 126 transições (113 com símbolo e 13 movimentos ε). Estado inicial `q0`, estado final `q27`. Diagrama: `docs/diagramas/er01_cpf.jff`. |
| **Testes** | Aceitas (6): `123.456.789-01`, `000.000.000-00`, `999.999.999-99`, `111.222.333-44`, `012.345.678-90`, `555.444.333-22`. Rejeitadas (6): `123456789-01`, `123.456.789.01`, `123.456.78-01`, `abc.def.ghi-jk`, ε (cadeia vazia), `123.456.789-012`. Caso-limite: `123.456.789-012`. |
| **Resultado e limite** | Não valida os dígitos verificadores do CPF (módulo 11), só o formato. Por isso `000.000.000-00` é aceito. |

**AFNε de CPF — detalhamento.** Estados `q0` a `q27`; inicial `q0`; finais `{q27}`.

Transições com símbolo (agrupadas):
```
q0 —{0-9}→ q1
q2 —{0-9}→ q3
q4 —{0-9}→ q5
q6 —{.}→ q7
q8 —{0-9}→ q9
q10 —{0-9}→ q11
q12 —{0-9}→ q13
q14 —{.}→ q15
q16 —{0-9}→ q17
q18 —{0-9}→ q19
q20 —{0-9}→ q21
q22 —{-}→ q23
q24 —{0-9}→ q25
q26 —{0-9}→ q27
```

Movimentos ε (vazios):

```
q1 —ε→ q2
q3 —ε→ q4
q5 —ε→ q6
q7 —ε→ q8
q9 —ε→ q10
q11 —ε→ q12
q13 —ε→ q14
q15 —ε→ q16
q17 —ε→ q18
q19 —ε→ q20
q21 —ε→ q22
q23 —ε→ q24
q25 —ε→ q26
```

---

## ER-02 — E-mail
| Campo | Conteúdo |
|---|---|
| **Identificação** | ER-02, `EMAIL`. Reconhece endereços de e-mail simplificados, com domínio simples ou multinível (`.com.br`). |
| **Alfabeto (Σ)** | `{a-z, A-Z, 0-9} ∪ {., _, -, @}` |
| **Linguagem L** | `usuário@domínio(.subdomínio)*.tld`, com usuário de 1 ou mais símbolos de `[L D . _ -]`, blocos de domínio de 1 ou mais símbolos de `[L D -]` e tld de 2 a 4 letras. |
| **ER formal** | `(L\|D\|.\|_\|-)+ @ (L\|D\|-)+ ( . (L\|D\|-)+ )* . L L (L)? (L)?` |
| **Sintaxe implementada** | `[a-zA-Z0-9._-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*\.[a-zA-Z]{2,4}` |
| **Equivalência** | `[a-zA-Z0-9._-]` = união de `L`, `D` e dos literais `.`, `_`, `-` (o `-` no fim da classe é literal); `+` = fecho positivo `rr*`; `(?:\.[a-zA-Z0-9-]+)*` = fecho de Kleene do grupo (sem captura) "ponto + bloco" (zero ou mais subdomínios); `{2,4}` = união de `LL`, `LLL` e `LLLL`, isto é, `L L L? L?`; `\.` = literal `.`. |
| **AFNε** | Construção de Thompson: bloco 1 (fecho positivo) antes do `@`; átomo `@`; bloco 2 (fecho positivo) do primeiro domínio; bloco 3, fecho de Kleene do grupo "`.` + bloco", que tem ε de pulo (zero repetições) e ε de retorno (mais repetições); átomo `.` final e tld com 2 letras obrigatórias e 2 opcionais (ε de pulo). As transições dos blocos 1, 2 e 3 são paralelas por símbolo; por isso são 430 no total. Total: **32 estados**, 430 transições (402 com símbolo e 28 movimentos ε). Estado inicial `q0`, estado final `q31`. Diagrama: `docs/diagramas/er02_email.jff`. |
| **Testes** | Aceitas (6): `maria@gmail.com`, `joao.souza@empresa.com.br`, `a@b.co`, `user_name-1@sub-domain.io`, `teste@teste.org`, `x@y.info`. Rejeitadas (6): `maria@@gmail.com`, `@gmail.com`, `maria@gmail`, `maria.gmail.com`, ε (cadeia vazia), `maria@gmail.c`. Caso-limite: `maria@gmail.c`. |
| **Resultado e limite** | Não verifica se o domínio existe. Também aceita `a..b@x.com` (pontos seguidos no usuário) e blocos de domínio que terminam em hífen (`a@b-.com`): é uma versão simplificada, não o padrão RFC 5322. |

**AFNε de EMAIL — detalhamento.** Estados `q0` a `q31`; inicial `q0`; finais `{q31}`.

Transições com símbolo (agrupadas):
```
q1 —{-.,0-9,A-Z,_,a-z}→ q2
q4 —{@}→ q5
q7 —{-,0-9,A-Z,a-z}→ q8
q11 —{.}→ q12
q14 —{-,0-9,A-Z,a-z}→ q15
q18 —{.}→ q19
q20 —{A-Z,a-z}→ q21
q22 —{A-Z,a-z}→ q23
q25 —{A-Z,a-z}→ q26
q29 —{A-Z,a-z}→ q30
```

Movimentos ε (vazios):

```
q0 —ε→ q1
q2 —ε→ {q3, q1}
q3 —ε→ q4
q5 —ε→ q6
q6 —ε→ q7
q8 —ε→ {q9, q7}
q9 —ε→ q10
q10 —ε→ {q11, q17}
q12 —ε→ q13
q13 —ε→ q14
q15 —ε→ {q16, q14}
q16 —ε→ {q17, q11}
q17 —ε→ q18
q19 —ε→ q20
q21 —ε→ q22
q23 —ε→ q24
q24 —ε→ {q25, q27}
q26 —ε→ q27
q27 —ε→ q28
q28 —ε→ {q29, q31}
q30 —ε→ q31
```

---

## ER-03 — Telefone
| Campo | Conteúdo |
|---|---|
| **Identificação** | ER-03, `TELEFONE`. Reconhece telefone fixo (8 dígitos) ou celular (9 dígitos) com DDD real. |
| **Alfabeto (Σ)** | `{0,...,9} ∪ {(, ), espaço, -}` |
| **Linguagem L** | `(` + um dos 67 DDDs reais do Brasil + `)` + espaço + 4 ou 5 dígitos + `-` + 4 dígitos. |
| **ER formal** | `( AREA ) espaço ( D D D D \| D D D D D ) - D D D D`, com `AREA = A B \| 2(1\|2\|4\|7\|8) \| 3(1\|2\|3\|4\|5\|7\|8) \| 5(1\|3\|4\|5) \| 7(1\|3\|4\|5\|7\|9)`, `A = (1\|4\|6\|8\|9)` e `B = (1\|2\|...\|9)` |
| **Sintaxe implementada** | `\((?:[14689][1-9]\|2[12478]\|3[1234578]\|5[1345]\|7[134579])\) [0-9]{4,5}-[0-9]{4}` |
| **Equivalência** | `\(` e `\)` = literais escapados; `(?:...)` = agrupamento sem captura; `\|` = união entre os 5 grupos de dezena; `[14689][1-9]` = concatenação de duas uniões (dezenas 1, 4, 6, 8, 9 com unidade de 1 a 9, o que dá 45 DDDs); `2[12478]`, `3[1234578]`, `5[1345]`, `7[134579]` = 5 + 7 + 4 + 6 DDDs, total de 67; `[0-9]{4,5}` = `D D D D (D)?`, isto é, união de 4 e 5 cópias de `D`. |
| **AFNε** | Depois do átomo `(` há um ramo de união com 5 alternativas (uma por grupo de dezena), cada uma concatenando dois átomos de classe, que reconvergem por ε no estado que antecede `)`. Depois de `)` e do espaço vêm 4 átomos de dígito obrigatórios, um átomo de dígito opcional (ε de pulo, que dá os 8 ou 9 dígitos), o `-` e 4 átomos de dígito. Total: **50 estados**, 165 transições (134 com símbolo e 31 movimentos ε). Estado inicial `q0`, estado final `q49`. Diagrama: `docs/diagramas/er03_telefone.jff`. |
| **Testes** | Aceitas (6): `(91) 98765-4321`, `(11) 3241-5678`, `(21) 99999-0000`, `(47) 4002-8922`, `(85) 91234-5678`, `(99) 3234-5678`. Rejeitadas (11): `91 98765-4321`, `(91)98765-4321`, `(91) 987654321`, `(9) 98765-4321`, ε (cadeia vazia), `(20) 98765-4321`, `(36) 98765-4321`, `(10) 91234-5678`, `(00) 91234-5678`, `(91) 98765-4321X`, `(91) 123-4321`. Caso-limite: `(91) 123-4321`. |
| **Resultado e limite** | Confere o DDD contra os 67 códigos reais, mas não valida o número em si (por exemplo, se o celular começa com 9). Também não vale para telefones sem DDD, com +55 ou sem parênteses. |

**AFNε de TELEFONE — detalhamento.** Estados `q0` a `q49`; inicial `q0`; finais `{q49}`.

Transições com símbolo (agrupadas):
```
q0 —{(}→ q1
q4 —{1,4,6,89}→ q5
q6 —{1-9}→ q7
q8 —{2}→ q9
q10 —{12,4,78}→ q11
q12 —{3}→ q13
q14 —{1-5,78}→ q15
q16 —{5}→ q17
q18 —{1,3-5}→ q19
q20 —{7}→ q21
q22 —{1,3-5,7,9}→ q23
q24 —{)}→ q25
q26 —{ }→ q27
q28 —{0-9}→ q29
q30 —{0-9}→ q31
q32 —{0-9}→ q33
q34 —{0-9}→ q35
q37 —{0-9}→ q38
q40 —{-}→ q41
q42 —{0-9}→ q43
q44 —{0-9}→ q45
q46 —{0-9}→ q47
q48 —{0-9}→ q49
```

Movimentos ε (vazios):

```
q1 —ε→ q2
q2 —ε→ {q4, q8, q12, q16, q20}
q3 —ε→ q24
q5 —ε→ q6
q7 —ε→ q3
q9 —ε→ q10
q11 —ε→ q3
q13 —ε→ q14
q15 —ε→ q3
q17 —ε→ q18
q19 —ε→ q3
q21 —ε→ q22
q23 —ε→ q3
q25 —ε→ q26
q27 —ε→ q28
q29 —ε→ q30
q31 —ε→ q32
q33 —ε→ q34
q35 —ε→ q36
q36 —ε→ {q37, q39}
q38 —ε→ q39
q39 —ε→ q40
q41 —ε→ q42
q43 —ε→ q44
q45 —ε→ q46
q47 —ε→ q48
```

---

## ER-04 — CEP
| Campo | Conteúdo |
|---|---|
| **Identificação** | ER-04, `CEP`. Reconhece CEP no formato `xxxxx-xxx`. |
| **Alfabeto (Σ)** | `{0,...,9} ∪ {-}` |
| **Linguagem L** | 5 dígitos, `-`, 3 dígitos. |
| **ER formal** | `D D D D D - D D D` |
| **Sintaxe implementada** | `[0-9]{5}-[0-9]{3}` |
| **Equivalência** | `[0-9]{5}` e `[0-9]{3}` = concatenação de 5 e 3 cópias de `D`; `-` = literal. |
| **AFNε** | Só concatenação: 9 átomos (8 de dígito e 1 de `-`), cada um com 2 estados, ligados por 8 movimentos ε. Sem ramificação de decisão. Total: **18 estados**, 89 transições (81 com símbolo e 8 movimentos ε). Estado inicial `q0`, estado final `q17`. Diagrama: `docs/diagramas/er04_cep.jff`. |
| **Testes** | Aceitas (6): `66000-000`, `01310-100`, `20040-020`, `70040-010`, `80010-000`, `90010-150`. Rejeitadas (6): `66000000`, `66000-0000`, `6600-000`, `abcde-123`, ε (cadeia vazia), `66000-00`. Caso-limite: `66000-00`. |
| **Resultado e limite** | Não valida se o CEP corresponde a um endereço real. |

**AFNε de CEP — detalhamento.** Estados `q0` a `q17`; inicial `q0`; finais `{q17}`.

Transições com símbolo (agrupadas):
```
q0 —{0-9}→ q1
q2 —{0-9}→ q3
q4 —{0-9}→ q5
q6 —{0-9}→ q7
q8 —{0-9}→ q9
q10 —{-}→ q11
q12 —{0-9}→ q13
q14 —{0-9}→ q15
q16 —{0-9}→ q17
```

Movimentos ε (vazios):

```
q1 —ε→ q2
q3 —ε→ q4
q5 —ε→ q6
q7 —ε→ q8
q9 —ε→ q10
q11 —ε→ q12
q13 —ε→ q14
q15 —ε→ q16
```

---

## ER-05 — Data de nascimento
| Campo | Conteúdo |
|---|---|
| **Identificação** | ER-05, `DATA`. Reconhece data no formato `dd/mm/aaaa` com dia entre 01 e 31 e mês entre 01 e 12. |
| **Alfabeto (Σ)** | `{0,...,9} ∪ {/}` |
| **Linguagem L** | Dia (01 a 31) + `/` + mês (01 a 12) + `/` + 4 dígitos de ano. |
| **ER formal** | `DIA / MES / D D D D`, com `DIA = 0(1\|2\|...\|9) \| (1\|2) D \| 3(0\|1)` e `MES = 0(1\|2\|...\|9) \| 1(0\|1\|2)` |
| **Sintaxe implementada** | `(?:0[1-9]\|[12][0-9]\|3[01])/(?:0[1-9]\|1[0-2])/[0-9]{4}` |
| **Equivalência** | `(?:...\|...\|...)` = agrupamento com união; `0[1-9]` = `0` seguido de união de 1 a 9 (01 a 09); `[12][0-9]` = 10 a 29; `3[01]` = 30 e 31; `1[0-2]` = 10, 11 e 12; `[0-9]{4}` = 4 cópias de `D`; `/` = literal. |
| **AFNε** | Dois ramos de união: o do dia com 3 alternativas e o do mês com 2, cada alternativa concatenando dois átomos de classe, com reconvergência por ε. Entre eles, átomos `/`; no fim, 4 átomos de dígito para o ano. Total: **36 estados**, 103 transições (81 com símbolo e 22 movimentos ε). Estado inicial `q0`, estado final `q35`. Diagrama: `docs/diagramas/er05_data.jff`. |
| **Testes** | Aceitas (6): `15/03/1990`, `01/12/1985`, `20/07/2000`, `29/02/2024`, `31/12/1999`, `05/05/1988`. Rejeitadas (11): `15-03-1990`, `1/3/1990`, `15/031990`, `15//1990`, ε (cadeia vazia), `32/01/2000`, `15/13/2000`, `00/01/2000`, `15/00/2000`, `15/03/1990 ` (com espaço no final), `15/03/19900`. Caso-limite: `15/03/19900`. |
| **Resultado e limite** | Valida faixas (dia 01-31, mês 01-12), mas não cruza dia com mês (`31/04/2000` e `30/02/2000` são aceitas), não trata ano bissexto (`29/02/2023` é aceita) e aceita ano `0000`. Decisão consciente para manter a linguagem regular e o autômato de tamanho razoável; vale citar na apresentação. |

**AFNε de DATA — detalhamento.** Estados `q0` a `q35`; inicial `q0`; finais `{q35}`.

Transições com símbolo (agrupadas):
```
q2 —{0}→ q3
q4 —{1-9}→ q5
q6 —{12}→ q7
q8 —{0-9}→ q9
q10 —{3}→ q11
q12 —{01}→ q13
q14 —{/}→ q15
q18 —{0}→ q19
q20 —{1-9}→ q21
q22 —{1}→ q23
q24 —{0-2}→ q25
q26 —{/}→ q27
q28 —{0-9}→ q29
q30 —{0-9}→ q31
q32 —{0-9}→ q33
q34 —{0-9}→ q35
```

Movimentos ε (vazios):

```
q0 —ε→ {q2, q6, q10}
q1 —ε→ q14
q3 —ε→ q4
q5 —ε→ q1
q7 —ε→ q8
q9 —ε→ q1
q11 —ε→ q12
q13 —ε→ q1
q15 —ε→ q16
q16 —ε→ {q18, q22}
q17 —ε→ q26
q19 —ε→ q20
q21 —ε→ q17
q23 —ε→ q24
q25 —ε→ q17
q27 —ε→ q28
q29 —ε→ q30
q31 —ε→ q32
q33 —ε→ q34
```

---