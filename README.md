# Python Swirl

**Aprenda Python e estatística com conceitos, vídeos e desafios.**

Curso gratuito para iniciantes, idealizado e dirigido pedagogicamente pelo **[professor Sidiney Rodrigues](https://github.com/sidineyr)**. A reconstrução de 8/10/2026 oferece dez módulos, do primeiro cálculo à entrega de uma análise de dados.

## Comece pelo curso on-line

**[Abrir o curso](https://sidineyr.github.io/python-swirl-statistics/)** · [Como estudar](https://sidineyr.github.io/python-swirl-statistics/como-estudar.html)

Cada aula segue problema → conceitos → vídeo → prática guiada → questões → desafio → síntese. Você executa Python real em um notebook, confere resultados e interpreta os dados com uma rubrica. Vídeos são complementares; explicações textuais permitem estudar sem assisti-los.

O site não executa Python. Use os notebooks pelo Colab (com conta Google) ou baixe e execute em Jupyter local (sem cadastro). Dez notebooks iniciais e dez soluções acompanham o curso; o CSV sintético já está incorporado para evitar dependência de download em execução.

## Percurso e entregas

| Módulo | Você aprende a |
| --- | --- |
| 1. Execute seu primeiro cálculo | Executar uma célula Python; Distinguir código, saída e comentário; Interpretar uma divisão no contexto |
| 2. Organize valores, tipos e listas | Criar nomes e listas; Distinguir texto e número; Calcular uma média com sum e len |
| 3. Leia uma tabela com pandas | Criar um DataFrame e ler CSV; Inspecionar linhas e colunas; Filtrar observações |
| 4. Escolha medidas conforme o tipo de variável | Classificar variáveis; Distinguir códigos de quantidades; Escolher resumos adequados |
| 5. Trate ausências sem inventar observações | Contar ausências; Distinguir zero de desconhecido; Documentar uma decisão de limpeza |
| 6. Transforme contagens em um gráfico legível | Calcular frequências e proporções; Escolher barras ou histograma; Rotular um gráfico e interpretá-lo |
| 7. Compare centro e espalhamento | Calcular média, mediana e quantis; Distinguir desvios amostral e populacional; Comparar grupos além da média |
| 8. Investigue variabilidade, viés e incerteza | Distinguir população e amostra; Simular médias amostrais; Distinguir desvio padrão e erro padrão |
| 9. Interprete associação sem afirmar causalidade | Calcular correlação de Pearson; Examinar um gráfico de dispersão; Identificar limites de uma conclusão causal |
| 10. Entregue uma análise que outra pessoa possa revisar | Formular uma pergunta analisável; Integrar limpeza, medidas e gráficos; Entregar notebook e conclusão com limitações |

A entrega final é um notebook com pergunta, preparação dos dados, medidas, gráficos e conclusão com limitações. Tempo estimado: cerca de 12 horas de leitura e prática, além dos vídeos. Dados fictícios para ensino, sem estudantes reais.

## Progresso e avaliação

O curso guarda textos, conferências e rubricas no navegador e oferece exportação/importação. Visitar uma aula não equivale a concluir atividade. A conclusão combina conferência numérica e autoavaliação; não comprova domínio. Não há cadastro obrigatório no site, tutor com API paga ou certificado. O site não importa automaticamente resultados do Colab.

## Curso original no terminal

As três lições da CLI e seu progresso continuam compatíveis. Instale Python 3.10 ou superior e execute a partir do repositório:

```sh
python -m python_swirl
```

No Windows, use `py -3 -m python_swirl`. [Instalação](docs/INSTALACAO.md), [uso e comandos](docs/USO.md). O código digitado executa localmente sem isolamento; use materiais de confiança. As [prévias conceituais antigas](https://sidineyr.github.io/python-swirl-statistics/media-mediana.html) também permanecem disponíveis.

## Documentação

- [Matriz curricular e entregas](docs/CURRICULO-ONLINE.md).
- [Vídeos, autores e nível de verificação](docs/VIDEOS.md).
- [Reconstrução, testes e limitações](docs/RECONSTRUCAO-2026-10-08.md).
- [Manutenção e rubrica do projeto](docs/MANUTENCAO-ONLINE.md).
- [Autoria da CLI](docs/AUTORIA.md), [contribuição](CONTRIBUTING.md), [histórico](CHANGELOG.md).
- [Indexação](docs/INDEXACAO.md), [licenças](LICENSE.md), [créditos](CREDITS.md).

## Estado e limites

Testes técnicos e revisão dos exemplos não substituem piloto com estudantes. Reprodução integral dos vídeos, legendas, revisão visual em dispositivos reais e acessibilidade assistiva precisam de revisão. Os vídeos possuem título/autoria confirmados e correspondência temática examinada, com limites registrados na curadoria. Colab autenticado não foi testado; os notebooks executaram localmente.

Inspirado no [swirl do R](https://swirlstats.com/); projeto independente sem vínculo oficial. Elaborado com assistência de ChatGPT/Codex sob orientação do idealizador. Código original MIT; conteúdo e dados sintéticos originais CC BY 4.0. Vídeos e materiais externos conservam suas próprias condições; respostas de estudantes não são abrangidas pela licença pública.

Caso gere lucro, o idealizador declara que será destinado ao **[Hospital Pequeno Príncipe](https://pequenoprincipe.org.br/doadores/apoie-o-pequeno-principe/)**. Isso não comprova doações nem representa parceria ou endosso institucional.
