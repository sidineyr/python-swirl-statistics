# Correções da auditoria · revisão 2

A auditoria do commit 19c3aa032d683f68c7d00eb5a96837c647fa0943 encontrou falhas reproduzíveis de avaliação e obstáculos para iniciantes. Esta revisão corrige o comportamento técnico e organiza o percurso; não demonstra aumento de aprendizagem.

| Antes | Depois | Evidência |
| --- | --- | --- |
| População editada podia alterar o gabarito da simulação | Referência fixa independente do namespace | Caso adulterado e lista artificial rejeitados |
| print de um cálculo correto era rejeitado | Captura do objeto de um único print; sem comparar texto de stdout | Expressão, print e atribuição; strings e múltiplos prints rejeitados |
| Valor antigo de medias podia aprovar 0 | Entrada precisa produzir ou mostrar a variável | 0, lambda não executada e ramo não executado rejeitados; lista mostrada aceita |
| 0.63 era rejeitado sem precisão visível | Duas casas declaradas somente para os desvios populacionais | Fórmula independente, valor completo e arredondado; desvio amostral rejeitado |
| Exploração alterava a tarefa | Contexto separado; :restaurar mantém respostas | Retomada após restauração e reflexão preservada |
| Escalas ajustadas individualmente | limits=(0,10) comum e marcações iguais | Mesma nota ocupa mesma posição; amplitude maior ocupa largura maior |
| Simulação oferecia solução grande de imediato | Um sorteio, sua média, repetição e transferência | Percurso integral e laço equivalente |
| Site apenas apresentava texto e resposta | Três prévias conceituais com previsão, tentativa, feedback e exploração | Testes dos cálculos/entradas e inspeção no navegador após publicação |
| Início levava a documento técnico | Entradas distintas, download e guia Windows/Linux | Links locais e sitemap; download conferido |
| Reflexões disponíveis só em JSON | Leitura, critérios e revisões preservando texto anterior | Teste de edição e leitura |

Progresso antigo é preservado; na lição 3 a migração retoma no primeiro apoio acrescentado, em vez de anunciar etapas novas como concluídas. Exploração não é persistida. Reinício requer REINICIAR e remove as respostas dessa lição; restauração do contexto apenas reinicia variáveis.

As prévias usam JavaScript, sem executor Python, requisições de respostas, cadastro, anúncios ou armazenamento persistente. Metadados, canonical, privacidade, autoria, MIT/CC BY 4.0, compromisso com Hospital Pequeno Príncipe e informação real sobre indexação são preservados.

Vinte testes Python passaram localmente; cálculos web, sintaxe JS, links e seis páginas do sitemap foram conferidos. A matriz CI e publicação devem ser consultadas nos jobs do commit entregue. Testes com participantes, leitores de tela, Windows pessoal, macOS e dispositivos móveis reais não foram realizados. Zoom e teclado são inspecionados no navegador disponível, sem alegação de conformidade integral WCAG.

O protocolo para cinco iniciantes está em AVALIACAO.md. Não há resultados humanos inventados. Pendências reais de indexação e AdSense permanecem em INDEXACAO.md e ADSENSE.md; esta revisão não declara entrada confirmada nos índices nem aprovação de anúncios.
