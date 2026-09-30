"""Geração do relatório final."""


def gerar_relatorio(registros, erros, vazias, total):
    L = ["=" * 56, "CHECACADASTRO - RELATÓRIO DE CADASTROS", "=" * 56,
         f"Linhas lidas: {total}",
         f"  válidas:   {len(registros)}",
         f"  inválidas: {len(erros)}",
         f"  vazias:    {vazias}", ""]

    if registros:
        L.append("Cadastros válidos:")
        for r in registros:
            L.append(f"  linha {r['numero']}: {r['nome']} ({r['email']})")
    else:
        L.append("Nenhum cadastro válido encontrado.")

    if erros:
        L += ["", "Cadastros inválidos:"]
        for numero, motivo in erros:
            L.append(f"  linha {numero}: {motivo}")

    return "\n".join(L)