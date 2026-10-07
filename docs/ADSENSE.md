# Google AdSense: dados preparados, sem anúncios ativos

O identificador público do idealizador foi incluído a pedido de Sidiney Rodrigues:

- Publisher ID: `pub-4924241177850142`.
- Client ID: `ca-pub-4924241177850142`.

O identificador foi recuperado de contexto anterior da conta; não foi inventado. Esta entrega não entrou no painel AdSense nem confirmou aprovação de um site para o Python Swirl. Não inclui senhas, tokens, dados bancários ou relatórios financeiros.

## Arquivos incluídos

| Arquivo | Finalidade |
| --- | --- |
| [adsense.json](../monetization/adsense.json) | Registrar identificadores e estado real da preparação |
| [adsense-head.html](../monetization/adsense-head.html) | Fragmento HTML com metatag e código de integração para uma página web |
| [ads.txt.example](../monetization/ads.txt.example) | Declaração a adaptar e publicar como ads.txt no local exigido pelo domínio |

O curso atual roda no console Python. O GitHub não executa scripts de publicidade inseridos no README. Portanto, esses arquivos **não ativam anúncios no curso nem na página github.com do repositório**. A apresentação web está publicada; ainda não há aprovação AdSense confirmada.

## Próxima integração necessária

1. Usar a apresentação publicada indicada abaixo e conferir o endereço no painel.
2. Adicionar o site no AdSense e verificar a configuração e o status no painel.
3. Integrar o fragmento HTML no head da página, respeitando requisitos aplicáveis de privacidade, consentimento e políticas de anúncios.
4. Publicar a declaração ads.txt no diretório de domínio exigido pelo AdSense, preservando entradas existentes. Em sites hospedados num subcaminho, não presuma que um arquivo dentro do repositório atende à raiz do domínio.
5. Confirmar o status do site e do ads.txt no painel. Somente depois afirmar que a integração está ativa.

O status em adsense.json permanece `prepared-not-connected`, com `ads_enabled: false`, até existir evidência de integração. Não há slot de anúncio informado, portanto nenhum número de slot foi criado.

## Referências oficiais

- [Encontrar o ID de publisher](https://support.google.com/adsense/answer/105516?hl=pt-br).
- [Conectar um site ao AdSense](https://support.google.com/adsense/answer/7584263?hl=pt-br).
- [Guia do ads.txt](https://support.google.com/adsense/answer/12171612?hl=pt-br).

AdSense é a ferramenta de monetização de um site com anúncios. Sua inclusão não cria campanha no Google Ads nem usa crédito de publicidade.

O compromisso de destinar eventuais lucros ao Hospital Pequeno Príncipe está em [CREDITS.md](../CREDITS.md). O código de publisher não torna o hospital titular da conta ou parceiro do projeto.

## Site publicado

A apresentação está publicada em https://sidineyr.github.io/python-swirl-statistics/ desde 7 de outubro de 2026. O endereço foi registrado na configuração preparada. Isso não confirma cadastro ou aprovação do site no AdSense: anúncios e scripts publicitários permanecem desativados.
