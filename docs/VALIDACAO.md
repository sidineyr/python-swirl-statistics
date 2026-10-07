# Validação da revisão 2

Data: 7 de outubro de 2026. Ambiente local: Linux, Python 3.12.14.

- `python3 -m unittest discover -s tests -v`: 20 testes aprovados, incluindo percurso integral real da CLI, pausa/retomada, print/atribuição, população adulterada, alvo antigo, laço equivalente, precisão declarada, escala comum, revisão de reflexão e migração de progresso antigo.
- `node scripts/test_activities.cjs`: cálculos independentes e formatos de entrada das três atividades web aprovados.
- `node --check site/activities.js`: sintaxe válida.
- `python3 scripts/check_site.py`: seis páginas, canonical, JSON-LD, links/âncoras/recursos locais e sitemap aprovados.
- Instalação em pasta temporária e carregamento dos três JSONs fora do projeto: verificado localmente com instalação sem dependências em /tmp, fora da pasta do projeto; JSONs e 11/13/16 etapas presentes. A matriz CI repete a instalação em todos os jobs.

A suíte compara desvios com fórmula independente, e não apenas solução e gabarito do mesmo JSON. Testes de interface preparados verificam comportamento, não aprendizagem. A migração específica da lição 3 preserva respostas e solicita as etapas novas; não há migração genérica de qualquer curso.

A matriz Linux/Windows × Python 3.10/3.12 executa testes, módulo, apresentação web, instalação e carregamento dos JSONs. O estado de cada versão está nos [jobs do GitHub Actions](https://github.com/sidineyr/python-swirl-statistics/actions); a validação da versão anterior não é prova da revisão atual. Não confundir Windows no runner com experiência pessoal de instalação.

Prévia conceitual web: JavaScript local; sem execução de Python, anúncios, telemetria ou armazenamento persistente de respostas. Inspeção por teclado, zoom e dos três percursos deve ser registrada após publicação. Leitores de tela e dispositivos móveis reais ainda não foram auditados. Não se declara conformidade WCAG.

Código Python local arbitrário não é isolado. Retomada reexecuta códigos registrados; efeitos externos não são revertidos. A exploração usa namespace separado, mas seus comandos ainda têm os mesmos privilégios locais e podem produzir efeitos externos. Respostas abertas usam autoavaliação e revisão humana.

Piloto com estudantes, Windows pessoal, macOS, concorrência entre sessões e validação completa de lições externas permanecem pendentes. Protocolo em [AVALIACAO.md](AVALIACAO.md). Veja [as correções e evidências](CORRECOES-AUDITORIA.md).
