# Como contribuir

Obrigado por ajudar a tornar estatística mais compreensível. Contribuições de educadores, estudantes e desenvolvedores são bem-vindas.

## Relatar um problema

Abra uma issue e escolha erro técnico ou dificuldade de aprendizagem. Informe o número da lição e a etapa. Não publique arquivos de progresso completos, informações pessoais, senhas ou dados reais de estudantes. Copie apenas o trecho necessário e use dados simulados.

## Propor uma mudança

1. Leia o README, [projeto pedagógico](docs/PROJETO.md) e [guia de autoria](docs/AUTORIA.md).
2. Crie uma branch a partir de main.
3. Faça uma alteração pequena com objetivo claro.
4. Execute `python -m unittest discover -s tests -v`.
5. Abra um pull request explicando o problema, a mudança e como foi verificada.

Para lições: indique objetivo, pergunta, previsão, prática, interpretação e transferência. Verifique cálculos, unidades, possíveis equívocos e dicas. Prefira português brasileiro simples. Não transforme falha em punição e não trate execução correta como evidência suficiente de aprendizagem.

Para código: preserve a separação entre motor e conteúdo, evite dependências obrigatórias desnecessárias e teste pausa/retomada se alterar estado. Considere que o código do estudante executa localmente; não exponha o motor na internet.

Dados externos precisam de fonte, licença, período e dicionário. Não inclua materiais com direitos incompatíveis. Ao contribuir, aceite MIT para código e CC BY 4.0 para conteúdo educacional original, conforme [licenças](LICENSE.md).

## Créditos

Idealização e direção pedagógica: [Sidiney Rodrigues](https://github.com/sidineyr). Contribuições efetivamente aceitas ficam registradas no histórico Git e podem ser adicionadas a [CREDITS.md](CREDITS.md). Indique uso de IA quando relevante à revisão e verifique seus resultados antes de enviar.
