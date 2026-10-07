# Python Swirl

**Aprenda estatística praticando em Python.**

**Lançamento público · 7 de outubro de 2026:** a versão 0.1 está disponível para estudar, adaptar e contribuir. Leia o [anúncio do projeto](docs/LANCAMENTO.md).

Curso interativo gratuito para iniciantes. Você faz uma previsão, calcula em Python, interpreta o resultado e aplica a ideia a outros dados. A compreensão estatística orienta cada atividade.

**Idealização e direção pedagógica: [Sidiney Rodrigues, pedagogo](https://github.com/sidineyr).**

## Escolha como começar

- [Experimente os três temas no navegador](https://sidineyr.github.io/python-swirl-statistics/): prévias conceituais com tentativa, feedback e exploração. Cálculos em JavaScript; não executam Python.
- [Baixe e faça o curso com Python no computador](https://sidineyr.github.io/python-swirl-statistics/instalacao.html): requisitos e passos para Windows e Linux.

## Comece em poucos passos

Instale Python 3.10 ou superior, [baixe o ZIP atual](https://github.com/sidineyr/python-swirl-statistics/archive/refs/heads/main.zip) ou clone o repositório e abra o terminal na pasta do README. Não é necessário instalar bibliotecas para estudar.

Windows:

```powershell
py -3 -m python_swirl
```

Linux:

```sh
python3 -m python_swirl
```

Escolha a lição **1**. Exemplo do que você vai investigar:

```python
>>> mean([10, 12, 14, 16, 88])
28
>>> median([10, 12, 14, 16, 88])
14
```

O tempo de 88 minutos eleva a média. Qual medida comunica melhor um tempo típico? O curso pede que você explique, além de calcular. Os sinais `>>>` ilustram a interação; não os copie ao digitar.

## Lições disponíveis

| Lição | Você aprende a |
| --- | --- |
| O que uma média esconde? | Comparar média e mediana e investigar um valor extremo |
| Duas turmas, a mesma média. São iguais? | Interpretar amplitude, desvio padrão e gráfico de pontos |
| Uma amostra conta toda a história? | Simular amostras e distinguir variabilidade de viés |

Dados simulados, linguagem em português e respostas abertas com critérios de autoavaliação. Código e progresso ficam no computador, sem conta ou API paga.

## Ajuda e retomada

- `:dica`: apoio progressivo, chegando a uma solução comentada.
- `:explorar`: experimentar Python em contexto separado, sem avançar ou alterar a resposta.
- `:repetir`: reler a etapa.
- `:bloco`: escrever várias linhas; encerrar com `.` em uma linha própria.
- `:sair`: pausar; escolha a mesma lição na próxima execução para retomar.
- `:restaurar`: recuperar os dados originais sem apagar respostas.
- `:revisar` e `:editar`: ler e revisar suas reflexões, mantendo o histórico.
- `:reiniciar`: refazer a lição após confirmação explícita, removendo o progresso dela.

Respostas abertas não recebem nota automática. Para exportar suas respostas, use `python -m python_swirl --exportar minhas-respostas.json`. Os gráficos são SVGs locais com descrição textual; o curso informa onde abri-los.

## Documentação e contribuição

- [Instalação](docs/INSTALACAO.md) e [guia completo de uso](docs/USO.md).
- [Currículo, pesquisa e arquitetura](docs/PROJETO.md).
- [Criar lições](docs/AUTORIA.md) e [contribuir](CONTRIBUTING.md).
- [Avaliação pedagógica](docs/AVALIACAO.md), [validação técnica](docs/VALIDACAO.md) e [histórico](CHANGELOG.md).
- [Créditos](CREDITS.md), [licenças](LICENSE.md) e [preparação para AdSense](docs/ADSENSE.md).

## Estado e limites

A versão 0.1 contém as três lições acima. Tabelas, inferência, regressão e o projeto final estão planejados. Não há certificado, tutor com IA ou publicação no PyPI. Vinte testes técnicos passaram localmente em Linux/Python 3.12.14, incluindo regressões da auditoria e execução real da CLI. O piloto com estudantes, leitores de tela e dispositivos móveis reais ainda precisa ser realizado. A matriz técnica da revisão 2 com Python 3.10 e 3.12 passou em Linux e Windows no [run 37689651692](https://github.com/sidineyr/python-swirl-statistics/actions/runs/37689651692); cada atualização executa novamente esses jobs no [GitHub Actions](https://github.com/sidineyr/python-swirl-statistics/actions); consulte os jobs para o alcance da validação. Isso não substitui a avaliação com estudantes.

O código do estudante executa localmente, sem isolamento, e é reexecutado na retomada. Use código e lições de confiança. Consulte [o guia de uso](docs/USO.md) para detalhes; este executor não deve ser exposto como serviço web.

## Créditos e compromisso social

Inspirado no [swirl do R](https://swirlstats.com/) e em seu [repositório original](https://github.com/swirldev/swirl). Projeto independente, sem vínculo oficial. A primeira versão foi elaborada com assistência de ChatGPT/Codex, sob orientação do idealizador. Veja [os créditos](CREDITS.md).

O Python Swirl é um projeto educacional gratuito. Caso o projeto gere lucro, o idealizador declara que esse lucro será destinado ao **[Hospital Pequeno Príncipe](https://pequenoprincipe.org.br/)**. Esse compromisso não representa comprovação de doações realizadas, parceria ou endosso do hospital. Para apoio direto, consulte [os canais oficiais da instituição](https://pequenoprincipe.org.br/doadores/apoie-o-pequeno-principe/).

Código original: [MIT](LICENSE). Conteúdo educacional e dados simulados originais: [CC BY 4.0](LICENSE.md). Dados pessoais e respostas dos estudantes não estão abrangidos por essa licença.

## Apresentação web e indexação

A [apresentação pública](https://sidineyr.github.io/python-swirl-statistics/) está publicada no GitHub Pages, incluindo três prévias conceituais guiadas, instalação, metadados e [sitemap](https://sidineyr.github.io/python-swirl-statistics/sitemap.xml). A publicação foi verificada em 7 de outubro de 2026. O sitemap foi enviado ao Google e a indexação da página inicial e da lição foi solicitada; a presença no índice ainda não foi confirmada. O Bing permanece pendente por bloqueio na autenticação. Consulte [o procedimento de indexação](docs/INDEXACAO.md) e [o prompt completo](docs/PROMPT-INDEXACAO.md). O workflow Pages publica alterações em `site/` na branch main e também pode ser executado manualmente.

A revisão 2 preserva respostas antigas e retoma a lição 3 nas etapas novas de apoio quando necessário. Consulte [as correções da auditoria e seus limites](docs/CORRECOES-AUDITORIA.md).
