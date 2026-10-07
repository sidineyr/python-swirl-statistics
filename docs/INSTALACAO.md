# Instalação e retomada

## Sem instalar pacotes

Extraia o ZIP. Abra um terminal na pasta `python-swirl-statistics`, onde estão README.md e a pasta python_swirl.

Windows:

```powershell
py -3 --version
py -3 -m python_swirl
```

Linux:

```sh
python3 --version
python3 -m python_swirl
```

macOS, com Python já instalado:

```sh
python3 -m python_swirl
```

Requer Python 3.10 ou superior. Os comandos de Windows e macOS são orientações de compatibilidade, ainda não testes realizados nesses sistemas. A execução e os testes desta entrega foram feitos em Linux; veja VALIDACAO.md para versão exata.

Para usar dentro de uma sessão Python local:

```python
from python_swirl.__main__ import main
main()
```

Não execute essa chamada em Jupyter nesta versão: argumentos do kernel e entrada interativa podem exigir adaptação. Escolha o console como percurso principal.

## Instalação opcional

```sh
python3 -m venv .venv
```

Linux/macOS: ative com `source .venv/bin/activate`. Windows PowerShell: `.venv\Scripts\Activate.ps1`. Se a política do PowerShell bloquear ativação, execute diretamente `.venv\Scripts\python.exe -m pip install .`, sem mudar a política global.

```sh
python -m pip install .
python-swirl
```

A instalação pode acessar a internet para obter setuptools. Não é necessária para seguir o curso a partir da pasta extraída.

## Progresso

Cada tentativa Python que termina sem exceção é salva; cada etapa concluída atualiza o índice. Reflexões e escolhas corretas também são salvas. Entradas incompletas ou código interrompido não são salvos. Ao pausar, o arquivo permanece no computador.

Retome com o mesmo comando e escolha a mesma lição. As variáveis são reconstruídas pela reexecução do setup e dos códigos registrados. Não altere o JSON de progresso manualmente. Para copiar suas respostas:

```sh
python -m python_swirl --exportar respostas.json
```

O caminho de destino deve ser novo. Para estudar em um arquivo separado:

```sh
python -m python_swirl --progress progresso-teste.json
```

O arquivo padrão está na pasta `.python-swirl` dentro da sua pasta pessoal. Para apagar seus dados, remova esse JSON; para apagar gráficos, remova os SVGs da pasta temporária `python-swirl-graficos`. O programa não transmite essas informações.

## Problemas comuns

- “No module named python_swirl”: confirme que o terminal está na pasta do README ou instale o pacote.
- “Python não encontrado”: tente `py -3` no Windows ou `python3` no Linux; caso contrário instale Python.
- Caracteres ilegíveis no terminal: tente `python -X utf8 -m python_swirl`.
- Progresso ilegível: preserve o original e abra outro arquivo com `--progress`.
- Comando muito demorado: use Ctrl+C. A última tentativa ainda não registrada será descartada.
- Gráfico não abre automaticamente: copie o caminho impresso e abra o SVG no navegador. A descrição textual permanece no console.

Não há limite de tempo imposto às tarefas. Nunca execute duas sessões com o mesmo arquivo de progresso ao mesmo tempo.
