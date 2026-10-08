> A descrição histórica abaixo refere-se à CLI 0.1. O curso web reconstruído possui dez módulos; veja [a matriz atual](CURRICULO-ONLINE.md) e [o relatório](RECONSTRUCAO-2026-10-08.md).

# Proposta pedagógica e técnica · versão 0.1

## 1. Produto e público

Python Swirl é um curso local de introdução ao pensamento estatístico, em português brasileiro, para pessoas sem experiência em programação. Cada comando tem uma finalidade de investigação. A primeira versão trabalha dados univariados pequenos e simulados, com três lições, preservando uma entrada simples. Não pretende ensinar toda a estatística ou todo o Python em três lições.

Resultado pretendido: o estudante calcula, compara, interpreta e reconhece limites dos resultados. A eficácia dessa experiência é uma hipótese a avaliar, não um resultado já demonstrado.

## 2. Pesquisa e decisões

Fontes consultadas em 7 de outubro de 2026:

| Fonte primária | Informação utilizada | Decisão para o projeto |
| --- | --- | --- |
| [swirl](https://github.com/swirldev/swirl) | Ambiente interativo no console R para programação e estatística | Prática no próprio ambiente Python, com feedback por etapa |
| [swirlify](https://swirlstats.com/swirlify/introduction.html) | Cursos divididos em lições; ferramenta para autoria | Lições declarativas separadas do motor |
| [Cursos swirl](https://github.com/swirldev/swirl_courses) | Organização de cursos e recursos em pastas de lições | Conteúdo independente e extensível; sem transcrever as lições |
| [ASA: GAISE 2016](https://magazine.amstat.org/blog/2017/09/01/gaisecollegereport/) | Investigação, compreensão conceitual, contexto, atividade e avaliação | Interpretar os números e formular limites, além de executar código |
| [ASA: anúncio GAISE 2026](https://magazine.amstat.org/blog/2026/09/01/gaisecollege/) | Amplia atenção à comunicação, ética, inclusão e ciência de dados | Relatório final, autoavaliação e experiência sem punição por erros |
| [Python statistics](https://docs.python.org/3/library/statistics.html) | Média, mediana e distinção entre desvio populacional e amostral | Usar biblioteca padrão no MVP, explicitando população definida |
| [Python random](https://docs.python.org/3/library/random.html) | Geradores locais e amostragem sem reposição | Semente 42 e objeto Random independente para simulações |
| [NumPy: início](https://numpy.org/doc/stable/user/absolute_beginners.html) | Arrays e operações numéricas | Introduzir depois de listas e investigação básica |
| [pandas: tutoriais](https://pandas.pydata.org/docs/getting_started/intro_tutorials/) | Tabelas e operações de exploração | Recurso futuro para CSV, filtros e valores ausentes |
| [Matplotlib: início](https://matplotlib.org/stable/users/getting_started/) | Visualização em Python | Recurso futuro para histogramas e dispersão; SVG simples no MVP |
| [SciPy: estatística](https://docs.scipy.org/doc/scipy/tutorial/stats.html) | Distribuições e procedimentos estatísticos | Futuro módulo de inferência, com pressupostos |
| [statsmodels: início](https://www.statsmodels.org/stable/gettingstarted.html) | Modelos e resultados de estimação | Futuro módulo de regressão, diagnóstico e interpretação |

O anúncio da ASA de setembro de 2026 informa um lançamento formal para o outono do hemisfério norte. Esta versão usa o anúncio e o resumo de 2016; não afirma que examinou todo o novo relatório. A pesquisa orienta o desenho, mas não demonstra que esta implementação produz aprendizagem.

O swirl oferece uma inspiração operacional: atividade curta, resposta e orientação dentro do console. A leitura da documentação e da organização dos repositórios não substitui um estudo de usabilidade do swirl. Limitações a testar na adaptação: instalação para iniciantes, leitura prolongada no terminal, apoio a respostas abertas e transferência para problemas novos. São riscos de desenho identificados, não defeitos empiricamente comprovados do swirl.

## 3. Matriz de objetivos, atividades e evidências

| Objetivo | Atividade | Evidência | Escopo |
| --- | --- | --- | --- |
| Formular pergunta investigável | Escrever pergunta antes do projeto final | Pergunta com variável, população e finalidade | Currículo futuro; MVP apresenta perguntas prontas |
| Reconhecer variável e unidade | Ler contexto dos tempos e notas | Identifica minutos, pontos e pessoa observada | Introdução no MVP; avaliação explícita futura |
| Organizar tabela e escolher gráfico | Frequências, CSV e exploração gráfica | Tabela coerente e escolha justificada | MVP usa listas e gráfico de pontos; tabelas futuras |
| Escolher medida de centro | Lição 1, média e mediana | Cálculo mais justificativa contextual | Implementado |
| Reconhecer variabilidade | Lição 2, médias iguais e dispersões distintas | Explicação com amplitude ou desvio padrão | Implementado |
| Interpretar incerteza e viés | Lição 3, sorteios e conveniência | Distingue variação aleatória de seleção enviesada | Implementado em nível introdutório |
| Distinguir descrição, associação e inferência | Comparar conclusões nos módulos 7 a 10 | Escolhe alcance compatível com desenho do estudo | MVP enfatiza descrição e limites; associação futura |
| Comunicar conclusão e limites | Reflexão final em cada lição | Evidência numérica, contexto e uma limitação | Implementado com autoavaliação |
| Adaptar Python a dados novos | Exercícios de transferência | Resolve nova lista sem exigir código idêntico | Implementado; independência requer observar uso de dicas |

## 4. Currículo completo

| Módulo | Pré-requisito | Conceito e atividade | Python necessário | Estado |
| --- | --- | --- | --- | --- |
| 1. Perguntas e dados | Nenhum | Definir variável, unidade e pergunta | Expressões e listas | Introdução incorporada nas três lições |
| 2. Tabelas e proporções | 1 | Frequência e comparação de taxas | DataFrame, seleção, contagem | Planejado |
| 3. Centro e dispersão | 1 | Média, mediana, amplitude e desvio | Funções e argumentos | MVP; quantis planejados |
| 4. Distribuições e gráficos | 3 | Forma, extremos e escolha de gráfico | Matplotlib | Gráfico de pontos no MVP; restante planejado |
| 5. Qualidade dos dados | 2 e 4 | Ausentes, duplicatas e erros | Filtros e isna | Planejado |
| 6. Probabilidade | 1 | Frequência relativa em simulações | Random, repetições | Planejado; ferramenta usada na lição 3 |
| 7. População e amostra | 3 | Variabilidade entre amostras e viés | sample e compreensão de listas | MVP |
| 8. Estimação e bootstrap | 6 e 7 | Reamostragem e intervalo | NumPy e quantis | Planejado |
| 9. Testes e efeitos | 8 | Compatibilidade com modelo nulo e relevância | SciPy | Planejado |
| 10. Associação e regressão | 4 e 9 | Relações, confundimento e diagnóstico | pandas e statsmodels | Planejado |
| 11. Projeto final | 2 a 10 | Investigar dados reais e comunicar | Fluxo integrado | Planejado |

Nos módulos futuros, trabalhar explicitamente: valor-p não é probabilidade da hipótese nula; intervalo frequencista descreve cobertura de um procedimento, não probabilidade posterior do parâmetro fixo; significância não é tamanho de efeito; associação não é causalidade; amostra maior não elimina viés; valores ausentes e extremos exigem investigação. Esses temas não são anunciados como lições já disponíveis.

MVP: três lições de 11 a 14 etapas, dados simulados, perguntas de previsão, exemplos resolvidos, código, dicas, interpretação e transferência. Retomadas conceituais entre as lições reforçam centro e variabilidade. Revisão espaçada de verdade dependerá de sessões posteriores e ainda não está implementada como agendamento.

## 5. Exemplo de percurso

1. O estudante abre o curso e escolhe a primeira lição.
2. Lê cinco tempos e prevê o efeito de trocar 18 por 88.
3. Executa `mean(tempos_com_atraso)` e vê `28`.
4. Executa `median(tempos_com_atraso)` e vê `14`.
5. Recebe feedback se tratar a média como tempo de todas as pessoas.
6. Explora outro valor e resolve um novo conjunto.
7. Escreve uma conclusão, compara com critérios e salva para revisão.

Erro de sintaxe produz orientação operacional. Resultado numérico inadequado produz uma dica de cálculo. Alternativa conceitual inadequada produz explicação específica. Respostas abertas não são classificadas automaticamente. As dicas chegam à solução, sem penalizar; o teste de transferência deve observar quando essa ajuda foi usada.

## 6. Interface e arquitetura

| Opção | Facilidade | Limitação | Escolha |
| --- | --- | --- | --- |
| Console Python | Executa o curso sem instalar bibliotecas | Terminal pode intimidar; gráficos abrem separadamente | Principal no MVP |
| Jupyter | Combina texto, código e gráficos | Instalação adicional e ordem de execução de células | Considerar após teste com iniciantes |
| Interface local visual | Pode reduzir esforço de navegação | Mais componentes, foco, execução e manutenção | Considerar depois de validar o percurso |

`engine.py`: ambiente Python, validação, progresso e SVG. `__main__.py`: navegação e feedback. `lessons/*.json`: textos e atividades em português. `tests/`: testes técnicos. `docs/`: decisões e autoria. `pyproject.toml`: empacotamento opcional.

Validação numérica aceita expressões equivalentes e tolerância. A atividade de simulação verifica a sequência reproduzível de 200 médias, rejeitando uma lista constante. O progresso grava eventos e índice da etapa. Na retomada o setup e os códigos são reexecutados; isso evita serializar objetos Python inseguros, mas não isola execução nem protege contra efeitos externos do código. A gravação do JSON usa substituição atômica. Uso simultâneo de duas sessões no mesmo arquivo não é suportado.

Sem dependências para estudar. NumPy, pandas, Matplotlib, SciPy e statsmodels são escolhas futuras por finalidade pedagógica, não requisitos atuais. O campo locale prepara identificação do idioma; tradução de mensagens do motor ainda exige trabalho.

## 7. Licenças e dados

Recomendação adotada nesta entrega: MIT para código; CC BY 4.0 para textos educacionais originais e conjuntos simulados. Autoria atribuída a Sidiney Rodrigues. Fontes externas são referenciadas, não relicenciadas. Ver LICENSE.md. Antes de importar uma lição externa, verifique autoria e licença específica.

Dados incluídos no setup das lições: listas de tempos em minutos e notas em pontos; população sintética de 100 inteiros entre 10 e 109. Não há dados pessoais nem coleta externa. Um futuro projeto com dados reais deverá registrar fonte, período, licença, dicionário, método de coleta e cuidados éticos.

## 8. Próximas decisões

Primeiro, testar as três lições com iniciantes e revisar os pontos em que compreensão ou navegação falham. Depois, introduzir tabelas e dados reais. A integração ao GitHub adiciona uma matriz de CI em Linux e Windows. Consulte o histórico de Actions para resultados efetivamente executados. Uma tutoria com IA pode ser opcional no futuro, com limites claros; não é necessária para esta versão.
