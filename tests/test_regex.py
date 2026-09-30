"""Testes das 5 ER: >= 6 cadeias aceitas e >= 6 rejeitadas por expressão, com caso-limite
(LIMITE) e verificação exaustiva das faixas de DDD, dia e mês. Todas usam fullmatch()."""
import os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from padroes import valida

CASOS = {
    "CPF": (
        ["123.456.789-01", "000.000.000-00", "999.999.999-99", "111.222.333-44",
         "012.345.678-90", "555.444.333-22"],
        ["123456789-01", "123.456.789.01", "123.456.78-01", "abc.def.ghi-jk",
         "", "123.456.789-012"],
    ),
    "EMAIL": (
        ["maria@gmail.com", "joao.souza@empresa.com.br", "a@b.co",
         "user_name-1@sub-domain.io", "teste@teste.org", "x@y.info"],
        ["maria@@gmail.com", "@gmail.com", "maria@gmail", "maria.gmail.com",
         "", "maria@gmail.c"],
    ),
    "TELEFONE": (
        ["(91) 98765-4321", "(11) 3241-5678", "(21) 99999-0000",
         "(47) 4002-8922", "(85) 91234-5678", "(99) 3234-5678"],
        ["91 98765-4321", "(91)98765-4321", "(91) 987654321", "(9) 98765-4321",
         "", "(20) 98765-4321", "(36) 98765-4321", "(10) 91234-5678",
         "(00) 91234-5678", "(91) 98765-4321X", "(91) 123-4321"],
    ),
    "CEP": (
        ["66000-000", "01310-100", "20040-020", "70040-010", "80010-000", "90010-150"],
        ["66000000", "66000-0000", "6600-000", "abcde-123", "", "66000-00"],
    ),
    "DATA": (
        ["15/03/1990", "01/12/1985", "20/07/2000", "29/02/2024", "31/12/1999", "05/05/1988"],
        ["15-03-1990", "1/3/1990", "15/031990", "15//1990", "", "32/01/2000",
         "15/13/2000", "00/01/2000", "15/00/2000", "15/03/1990 ", "15/03/19900"],
    ),
}

# caso-limite de cada ER (obrigatório no enunciado): precisa estar entre as rejeitadas
LIMITE = {
    "CPF": "123.456.789-012",     # 1 dígito a mais no final
    "EMAIL": "maria@gmail.c",     # tld com 1 letra, abaixo do mínimo 2
    "TELEFONE": "(91) 123-4321",  # 3 dígitos antes do hífen, abaixo do mínimo 4
    "CEP": "66000-00",            # falta 1 dígito
    "DATA": "15/03/19900",        # 1 dígito a mais no ano
}

DDDS = {11,12,13,14,15,16,17,18,19,21,22,24,27,28,31,32,33,34,35,37,38,
        41,42,43,44,45,46,47,48,49,51,53,54,55,61,62,63,64,65,66,67,68,69,
        71,73,74,75,77,79,81,82,83,84,85,86,87,88,89,91,92,93,94,95,96,97,98,99}


class TestRegex(unittest.TestCase):
    def test_todas(self):
        for nome, (aceitas, rejeitadas) in CASOS.items():
            self.assertGreaterEqual(len(aceitas), 6)
            self.assertGreaterEqual(len(rejeitadas), 6)
            self.assertIn(LIMITE[nome], rejeitadas)
            for s in aceitas:
                with self.subTest(nome=nome, cadeia=s, esperado="aceita"):
                    self.assertTrue(valida(nome, s))
            for s in rejeitadas:
                with self.subTest(nome=nome, cadeia=s, esperado="rejeitada"):
                    self.assertFalse(valida(nome, s))

    def test_ddd_exaustivo(self):
        self.assertEqual(len(DDDS), 67)
        for n in range(100):
            with self.subTest(ddd=n):
                self.assertEqual(valida("TELEFONE", f"({n:02d}) 91234-5678"), n in DDDS)

    def test_dia_mes_exaustivo(self):
        for n in range(100):
            with self.subTest(dia=n):
                self.assertEqual(valida("DATA", f"{n:02d}/01/2000"), 1 <= n <= 31)
            with self.subTest(mes=n):
                self.assertEqual(valida("DATA", f"15/{n:02d}/2000"), 1 <= n <= 12)

    def test_apenas_digitos_ascii(self):
        """[0-9] (e não \\d): dígitos Unicode ficam fora da linguagem."""
        for nome, cadeia in [("CEP", "٦٦٠٠٠-٠٠٠"), ("CEP", "６６０００-０００"),
                             ("CPF", "١٢٣.٤٥٦.٧٨٩-٠١"), ("DATA", "１５/０３/１９９０"),
                             ("TELEFONE", "(９１) 98765-4321")]:
            with self.subTest(nome=nome, cadeia=cadeia):
                self.assertFalse(valida(nome, cadeia))


if __name__ == "__main__":
    unittest.main(verbosity=2)