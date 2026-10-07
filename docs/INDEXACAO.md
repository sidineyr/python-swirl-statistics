# Publicação e indexação

## Estado verificado em 7 de outubro de 2026

- Site publicado: https://sidineyr.github.io/python-swirl-statistics/
- Deployment aprovado: https://github.com/sidineyr/python-swirl-statistics/actions/runs/37685116940
- HTTP 200 confirmado na raiz, index.html, media-mediana.html, privacidade.html, sitemap.xml e styles.css. Nenhum X-Robots-Tag de bloqueio nessas respostas. O robots.txt da raiz do domínio permite rastreamento; suas regras foram apenas lidas, sem alteração.
- Sitemap XML validado com as três URLs canonical. About atualizado com o site publicado.
- Google: usada a propriedade existente https://sidineyr.github.io/, que inclui a subpasta do curso. Sitemap enviado com confirmação do painel. Indexação de index.html e media-mediana.html solicitada e aceita na fila prioritária. Na inspeção, ambas ainda apareciam como não indexadas.
- Leitura do sitemap no Google: o relatório inicial mostrou “Não foi possível buscar o sitemap”, apesar da resposta pública HTTP 200 e XML válido. A leitura pelo Google precisa ser acompanhada; não equivale à confirmação de recebimento.
- Bing: submissão não realizada. A autenticação Microsoft informou que não conseguiu enviar a notificação de confirmação. Nenhuma credencial, código ou dado de autenticação foi publicado no repositório.
- Anúncios continuam desativados. Publicação do site não comprova aprovação AdSense.

## Procedimento para manutenção

Os arquivos web estão em `site/`. O site já usa GitHub Actions como fonte do Pages. Alterações na pasta pública disparam publicação em main; também há execução manual. Antes de reenviar aos buscadores, confirme a URL efetiva e as respostas HTTP.

1. Configure Settings → Pages → Source → GitHub Actions no repositório. Execute manualmente o workflow “Publicar apresentação no GitHub Pages”. Ele publica somente `site/`, sem respostas de estudantes nem arquivos de preparação de anúncios.
2. Após o job passar, abra a URL devolvida pelo deployment. Confirme respostas HTTP 200 das três páginas e de `sitemap.xml`. Se o domínio ou caminho mudar, atualize todos os canonical, og:url, dados estruturados e URLs do sitemap antes de publicar novamente.
3. Reutilize a propriedade existente que abrange a URL, ou cadastre a URL efetiva no Google Search Console como propriedade de prefixo de URL. Utilize somente a verificação real fornecida pelo painel. Para a subpasta de github.io, não reivindique controle DNS do domínio github.io. Não invente códigos de verificação.
4. Na propriedade verificada, envie o sitemap e inspecione a página inicial e a lição. Solicite indexação quando o painel permitir. Registre a data, a URL e o resultado observado.
5. Adicione e verifique o site no Bing Webmaster Tools, ou importe uma propriedade já verificada do Search Console quando disponível. Envie o sitemap e registre o resultado.
6. Revise posteriormente os relatórios de cobertura/indexação. Envio de sitemap, solicitação de indexação e presença no índice são estados diferentes. Nenhum deles garante posição nos resultados.

## Rastreamento e metadados

Há títulos, descrições, canonical, Open Graph e JSON-LD com informações fiéis ao projeto. `site/sitemap.xml` contém apenas as três páginas públicas, com a data de alteração real. Altere `lastmod` quando houver mudança significativa; não renove a data artificialmente.

`seo/robots-domain-root.txt` é um modelo, não um arquivo ativo. Os buscadores consultam robots.txt na raiz do domínio, não em `/python-swirl-statistics/robots.txt`. Não altere outro repositório nem substitua regras do domínio sem revisar o contexto. A submissão do sitemap na propriedade verificada dispensa colocar esse modelo na subpasta.

Não use endpoints antigos de ping nem a Google Indexing API para estas páginas educacionais comuns. Não há tokens novos Search Console/Bing nos arquivos. O estado efetivamente observado está registrado acima; a indexação ainda não foi confirmada. O AdSense preparado não comprova aprovação de site ou indexação e não foi ativado na página.

## Referências oficiais

- https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages
- https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap
- https://developers.google.com/crawling/docs/robots-txt/robots-txt-spec
- https://www.bing.com/webmasters/help/sitemaps-3b5cf6ed

Execute `python scripts/check_site.py` para verificar estrutura e links locais. Isso não verifica disponibilidade HTTP nem indexação.
