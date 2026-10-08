# Manutenção do curso on-line

`curriculum/modules.json` é a fonte dos dez módulos; `curriculum/videos.json` registra a curadoria. `site/dados/turmas.csv` contém dados sintéticos. Edite as fontes e execute `python scripts/build_course.py`; não altere manualmente as páginas ou notebooks gerados.

O gerador cria dez páginas, dez notebooks iniciais e dez soluções, a página inicial, ajuda, fontes e sitemap. As páginas anteriores e a CLI foram mantidas. `site/course.js` confere números; não executa Python. Os notebooks executam Python real no Colab ou no Jupyter. Colab exige conta Google para execução; há alternativa local sem cadastro. O site não lê resultados nem salva arquivos do Colab.

Progresso web usa a chave nova `python-swirl-online-v1`. Arquivos de progresso da CLI não foram alterados. Visita, conferências numéricas, execução autodeclarada e autoavaliação são registros separados. Editar uma resposta remove a marca de conclusão. Refazer mantém textos. Importação de conflitos concatena textos e pede nova conferência. Exportação é a cópia portátil; não há servidor ou sincronização de contas.

## Verificação antes de publicar

```sh
python -m unittest discover -s tests -v
python scripts/build_course.py
python scripts/check_site.py
python -m pip install pandas matplotlib
python scripts/check_notebooks.py
npm ci
npm test
```

O workflow Pages publica `site/` a partir de main. O workflow do curso mantém a matriz original da CLI e adiciona execução de notebooks e testes DOM em Linux. Testes DOM não substituem revisão visual, uso com leitor de tela, dispositivos reais ou piloto pedagógico.

Para atualizar vídeos, confirme título/canal pelo oEmbed e examine descrição e conteúdo. Registre o nível real de verificação, não apenas status HTTP. Se um vídeo sair do ar, mantenha a explicação textual e substitua a curadoria sem bloquear o percurso.

## Rubrica do projeto

Para cada um dos seis critérios do módulo 10, use 0 (ausente/incorreto), 1 (parcial, precisa de revisão) ou 2 (completo e fundamentado). O objetivo é identificar o que revisar, não certificar domínio por soma de pontos. O site registra checklist autodeclarado; a revisão de qualidade exige leitura humana do notebook.
