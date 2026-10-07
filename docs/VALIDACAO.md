# Validação da versão 0.1

Data: 7 de outubro de 2026. Ambiente: Linux, Python 3.12.14.

## Verificações realizadas

`python3 -m unittest discover -s tests -v`: **10 testes aprovados**.

| Verificação | Resultado |
| --- | --- |
| Soluções de referência de todas as atividades executáveis | Passaram |
| Percurso de interação das três lições com entrada simulada | Concluiu todas as etapas |
| Código equivalente e números incorretos | Aceita equivalentes e rejeita incorretos, bool e NaN |
| Cálculos independentes de média e dispersão | Valores conferidos |
| Lista constante falsificando simulação | Rejeitada |
| Estado das listas após retomada | Preservado por reexecução |
| Pausa, dica e índice salvo | Funcionaram |
| Reinício e tentativa sem avanço | Funcionaram |
| Comando que altera dados e termina com exceção | Reconstrói variáveis anteriores |
| Progresso com JSON inválido | Preservado, sem sobrescrita |
| SVG com descrição e caracteres escapados | XML válido, descrição presente |

Instalação verificada: `python3 -m pip install --no-build-isolation --no-deps --target <pasta-temporaria> .`. O wheel foi construído e instalado com sucesso. Fora da pasta do projeto, o módulo instalado listou as três lições, confirmando inclusão dos JSONs. A instalação usou ferramentas de empacotamento já disponíveis; não comprovou instalação em máquina sem setuptools.

O teste de percurso usa respostas preparadas para verificar o funcionamento; não mede aprendizagem nem usabilidade humana. Cálculos e casos negativos foram verificados separadamente. A descrição SVG foi testada estruturalmente; não houve auditoria visual ou com leitor de tela.

## Limitações presentes

- Sem testes com estudantes, Windows, macOS ou diferentes versões de Python.
- Interface principal no console, com gráficos em SVG abertos separadamente.
- Três lições implementadas; o restante do currículo é planejamento.
- Sem leitor de tela auditado, internacionalização completa ou revisão espaçada agendada.
- Respostas abertas usam autoavaliação; não recebem avaliação automática de qualidade.
- Código local arbitrário não é isolado. A retomada repete códigos registrados.
- Reiniciar uma lição remove suas respostas daquele arquivo de progresso; exporte antes se desejar preservá-las.
- Não há concorrência entre sessões, migração automática de lições alteradas ou validação completa de JSON de terceiros.
- Dependência da sequência pseudoaleatória para resultados de referência da lição 3; a versão testada é Python 3.12.14.
- Sem publicação no PyPI ou serviço web; sem participantes ou resultados educacionais inventados.
- Os testes em GitHub Actions serão reportados somente após execução dos jobs.

## Próximo passo prioritário

Realizar o piloto de AVALIACAO.md, começando pela primeira lição no Windows. Revisar instruções e feedback conforme dificuldades observadas antes de ampliar o currículo.
