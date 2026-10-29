# Publicação no GitHub: etapas e commits verdadeiros

Crie um repositório **novo**, público, na sua conta: `eng-dados-junior-olist`.
Não marque README/gitignore na criação porque já estão no projeto.

É essencial **não usar somente um commit para a entrega inteira**. Construa e confira cada etapa. O notebook no Colab permite executar e observar as saídas antes de publicar.

## Ordem recomendada para publicar

1. **Estrutura/spec:** `.gitignore`, `README.md`, `specs/transformacao.md`, `requirements.txt`, `pyproject.toml`. Commit: `docs: define pergunta, escopo, grao e regras`.
2. **Ingestão:** `pipeline/__init__.py`, `pipeline/config.py`, `pipeline/ingestao.py`. Commit: `feat: carrega quatro tabelas no schema raw preservando varchar`.
3. **Transformação:** `pipeline/transformacao.py`. Commit: `feat: cria refined com chaves unicas e tipos validados`.
4. **Indicadores:** `pipeline/marts.py` e os **cinco** arquivos em `sql/marts/`. Commit: `feat: implementa cinco indicadores SQL com CTE e janela`.
5. **Qualidade/testes:** `pipeline/qualidade.py`, `pipeline/executar.py`, `tests/`, `.github/workflows/testes.yml`, `reports/resultado_execucao.md`, `GUIA_GITHUB.md`. Commit: `test: adiciona validacoes, coverage e relatorio de execucao`.

Se publicar via interface web, selecione os arquivos **da etapa** e depois clique `Commit changes`. Navegadores podem ocultar pastas com ponto (`.github`); verifique se a workflow aparece em `.github/workflows/testes.yml` no site.

**Não publique:** dados brutos baixados, arquivo `.duckdb`, `.env` e credenciais.

## Última conferência antes da entrega
- Abra `Actions` e confira que os testes passaram (verdes).
- Abra `reports/resultado_execucao.md` e confira resultados reais gerados no Colab.
- Abra os cinco `.sql`, verifique que as perguntas e o grão são seus.
- Só então copie `https://github.com/SEU_USUARIO/eng-dados-junior-olist` para o formulário.
