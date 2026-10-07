# Python Swirl

**Aprenda estatística praticando em Python.**

Curso interativo gratuito idealizado por **Sidiney Rodrigues, pedagogo**. A versão 0.1 contém três lições em português brasileiro. O estudante prevê, calcula, observa e explica resultados. Código e respostas são salvos localmente, sem cadastro, API, telemetria ou dependências externas para estudar.

Inspirado no [swirl do R](https://swirlstats.com/), sem vínculo oficial. As lições e o motor deste projeto foram escritos para Python; não são cópias de cursos do swirl.

## Comece aqui

1. Instale Python 3.10 ou superior, se ainda não estiver instalado.
2. Extraia este projeto e abra um terminal na raiz do projeto, onde está o README.md.
3. Execute:

```sh
python -m python_swirl
```

No Windows, também pode usar `py -3 -m python_swirl`. No Linux, `python3 -m python_swirl`. Não é necessário executar `pip install` para começar.

Escolha **1** e siga a primeira lição. `mean(tempos)` calcula uma média; `sum(tempos) / len(tempos)` também é aceito. As funções estatísticas usadas na lição já estão carregadas. Digite somente o código, sem o sinal `>`.

## O que você pode estudar agora

| Lição | Pergunta | O que você pratica |
| --- | --- | --- |
| 1 | O que uma média esconde? | Média, mediana, valor extremo e escolha de medida |
| 2 | Duas turmas, a mesma média. São iguais? | Amplitude, desvio padrão, gráfico de pontos e limites das conclusões |
| 3 | Uma amostra conta toda a história? | População, amostra, simulação, variabilidade e viés |

Todos os dados são **simulados**. Nenhuma pessoa ou escola é representada. A sequência recomendada é 1 → 2 → 3. Você pode abrir qualquer lição; estimativa editorial de duração: 15 a 25 minutos por lição, ainda não medida com estudantes.

## Comandos durante a lição

| Comando | Ação |
| --- | --- |
| `:ajuda` | Mostrar comandos |
| `:dica` | Receber uma dica; repetir oferece apoio maior e depois solução comentada |
| `:repetir` | Reler a etapa atual |
| `:explorar` | Experimentar uma linha em contexto separado, sem avançar ou alterar a resposta |
| `:bloco` | Escrever código em várias linhas; terminar com uma linha contendo `.` |
| `:sair` | Pausar e salvar |
| `:restaurar` | Recuperar os dados originais, mantendo posição e respostas; recalcular variáveis criadas por você |
| `:revisar` | Ler suas explicações e critérios de autoavaliação |
| `:editar` | Registrar uma revisão de reflexão, mantendo o texto anterior |
| `:reiniciar` | Apagar progresso desta lição após digitar REINICIAR para confirmar |

O menu também aceita `:reiniciar` e pede o número da lição. Respostas abertas são registradas com critérios para autoavaliação, sem nota automática. Releia os critérios e compare sua explicação com os números.

```sh
python -m python_swirl --editar 1
python -m python_swirl --revisar 1
python -m python_swirl --listar
python -m python_swirl --licao 1
python -m python_swirl --exportar minhas-respostas.json
python -m python_swirl --progress meu-progresso.json
```

O progresso padrão fica em `~/.python-swirl/progresso.json`. A exportação inclui suas respostas e os códigos executados, inclusive tentativas que rodaram sem responder corretamente à tarefa. Compartilhe apenas se desejar. Para corrigir uma reflexão já registrada, use `:editar` durante uma lição, informe o número da etapa e escreva a revisão. O texto anterior permanece no histórico. Para ler sem iniciar a lição, use `--revisar 1`. Para revisar uma reflexão depois de concluir, use `--editar 1` ou `:editar` no menu e escolha a lição.

## Gráficos e execução

`grafico(turma_a, "Turma A", limits=(0, 10))` produz um SVG de pontos e imprime uma descrição com todas as frequências. Abra o arquivo indicado no navegador. Para comparar notas, use `limits=(0, 10)` em ambos os gráficos: os limites e as marcações serão iguais. Sem limits, o eixo se ajusta ao conjunto; esses gráficos não servem para comparar larguras diretamente. Os SVGs são salvos na pasta temporária `python-swirl-graficos` do sistema.

**Python é executado localmente com os privilégios do usuário. O motor não é uma sandbox.** Pode executar código Python arbitrário, ler arquivos e acessar a rede se o estudante escrever comandos para isso. O programa do curso não envia dados. Use somente código e lições de confiança. Ao retomar, o motor reexecuta os códigos registrados para reconstruir variáveis; comandos com efeitos externos podem repetir esses efeitos. Não hospede este executor como serviço web. `Ctrl+C` interrompe código demorado; código ainda não registrado não é retomado.

Se um comando falhar depois de alterar variáveis, o motor reconstrói as variáveis a partir das tentativas anteriormente registradas. Efeitos externos, como gravações feitas pelo próprio código, não podem ser revertidos. Progresso inválido não é sobrescrito: use outro arquivo com `--progress` ou restaure sua cópia. Mudanças futuras nas lições devem prever migração do progresso.

## Documentação

- [Proposta, pesquisa, currículo, matriz e arquitetura](PROJETO.md)
- [Instalação e funcionamento](INSTALACAO.md)
- [Criar novas lições](AUTORIA.md)
- [Avaliação com iniciantes e critérios de interpretação](AVALIACAO.md)
- [Validação técnica e limitações](VALIDACAO.md)
- [Licenças e atribuições](../LICENSE.md)

## Desenvolvimento

```sh
python -m unittest discover -s tests -v
```

Opcionalmente, em um ambiente virtual, instale o pacote com `python -m pip install .` e use o comando `python-swirl`. Essa instalação exige setuptools e pode precisar de internet para obter a ferramenta de empacotamento. O curso em si funciona offline.

## Limitações iniciais

Protótipo executável, com validação técnica. Ainda sem testes com estudantes, auditoria com leitores de tela ou validação em macOS e Windows 10 pessoal. A matriz técnica de CI passou em Linux e Windows com Python 3.10 e 3.12; veja VALIDACAO.md. O currículo completo está planejado; apenas as três lições acima estão implementadas. Não há tutoria com IA, certificado, publicação no PyPI; consulte o repositório para a versão publicada.

## Contrato das respostas e precisão

Nas etapas de número, são aceitos expressão (`mean(tempos)`), `print` com um único valor (`print(mean(tempos))`) e atribuição final (`resposta = mean(tempos)`). O motor captura o objeto, não interpreta strings de stdout. Dois valores impressos são ambíguos. Valida-se o resultado; fornecer um literal correto não comprova que você aprendeu o procedimento.

Nas etapas que pedem variável, crie-a ou mostre-a explicitamente. Uma expressão sem relação, como `0`, não aprova uma variável antiga. Código equivalente, incluindo laços, é permitido. A simulação usa uma referência independente da população editável; exige semente 42, 200 amostras de cinco pessoas e a ordem dos sorteios. Uma distribuição semelhante não basta para essa tarefa determinística.

A precisão aparece na pergunta. Desvios populacionais aceitam valor completo ou duas casas decimais; outras etapas pedem valor completo. Em Python use ponto decimal: `0.63`; a vírgula pode significar tupla ou separação de argumentos. As prévias web aceitam ponto ou vírgula em campos numéricos, pois não são campos de código.

A exploração não é registrada nem altera variáveis da resposta. Uma tentativa de código pode alterar o contexto: `:restaurar` recupera os dados originais sem apagar o histórico. Na retomada, eventos anteriores a essa restauração não permanecem no contexto, mas continuam no histórico de respostas.

## Atualização do percurso

A revisão 2 acrescenta três etapas antes da simulação da lição 3. Progresso antigo dessa lição que já passou do ponto é retomado na primeira etapa adicionada. Respostas antigas e posição anterior ficam preservadas; não se declara que o estudante realizou exercícios novos. Índices de respostas antigas posteriores são ajustados. As outras lições mantêm a ordem das etapas. Mantenha cópia do progresso antes de atualizações futuras.
