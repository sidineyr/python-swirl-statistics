# Criar lições

As lições são arquivos JSON UTF-8 em `python_swirl/lessons`. O prefixo numérico do nome define a ordem no menu. Textos não exigem modificar o motor; novos tipos de validação exigem programação e testes.

Cada lição tem `id` único e estável, `title`, `locale`, `intro`, `objectives`, `setup` e `steps`. `setup` é código Python de confiança que inicializa os dados. Funções disponíveis: mean, median, pstdev, stdev, Random, grafico e funções padrão Python.

Exemplo de etapa:

```json
{
  "type": "code",
  "text": "Calcule a média de tempos.",
  "check": {"kind": "number", "value": 14},
  "solution": "mean(tempos)",
  "hints": [
    "Considere todos os tempos.",
    "Some e divida pela quantidade.",
    "mean(tempos) resulta em 14."
  ],
  "feedback_ok": "A média é 14 minutos.",
  "feedback_wrong": "Compare o resultado com a soma dos tempos dividida pela quantidade."
}
```

Sem `target`, o motor valida o resultado inequívoco da expressão, de uma atribuição final ou de um único valor passado a print. Com `target`, a entrada deve produzir ou mostrar explicitamente a variável nomeada; uma variável antiga não aprova código sem relação. `check.kind` admite number, sequence e sample_means (este último é específico da simulação da lição 3). Bool não conta como número. O campo solution documenta a solução de referência e é usado nos testes; o comando :dica usa os textos em hints, então inclua a solução comentada na última dica.

Tipos de etapa:

| Tipo | Campos específicos | Uso |
| --- | --- | --- |
| info | text, feedback_ok | Explicação; Enter avança |
| code | check, solution, hints, feedback_wrong, feedback_ok; target opcional | Prática executável |
| choice | options, answer (índice a partir de 1), feedbacks, feedback_wrong, feedback_ok | Interpretação com feedback por alternativa |
| reflection | rubric, feedback_ok | Resposta aberta com critérios, sem correção automática |

O motor não oferece validação completa do esquema para lições externas. Antes de distribuir, execute todos os exemplos, soluções e testes. Não entregue JSON de terceiros sem revisar o setup: ele executa código com os privilégios locais.

Checklist de autoria:

1. Defina uma pergunta e uma evidência de compreensão.
2. Informe se os dados são simulados; para dados reais, registre fonte, licença e período.
3. Apresente uma previsão antes do cálculo.
4. Explique uma pequena operação Python em contexto.
5. Escreva dicas que progridam de conceito para operação e solução.
6. Inclua interpretação e um conjunto diferente para transferência.
7. Revise unidades, arredondamentos, pressupostos e limites.
8. Execute soluções, tentativas equivalentes e erros previstos.
9. Teste pausa e retomada e observe a experiência com iniciantes.

Não mude id nem a ordem das etapas de uma lição publicada sem planejar migração. A versão 0.1 salva o índice e os eventos de uma estrutura fixa. Renomear apenas um texto pode ser seguro; inserir ou remover etapas invalida a associação entre progresso e percurso. A revisão 2 possui migração específica do percurso da lição 3; não há migração genérica. Toda alteração estrutural nova precisa de migração e teste próprios.

O menu e --licao usam a ordem dos arquivos automaticamente. Uma nova lição que use os tipos e validadores existentes não exige mudar o motor.

`check.decimals` é opcional para number: compara o arredondamento nessa quantidade de casas e deve aparecer na pergunta. Sem esse campo a tolerância numérica permanece 1e-7. `sample_means` usa a população de referência fixa 10 a 109, independente do namespace do estudante; não reutilize esse validador para outra população sem mudar a implementação e testar. `revision` identifica a revisão de percurso. IDs e eventos de etapas precisam de migração explícita quando a ordem mudar.
