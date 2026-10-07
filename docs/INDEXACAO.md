# Publicação e indexação

Os arquivos web estão preparados em `site/`. A publicação e a indexação ainda não foram verificadas. Endereço previsto: https://sidineyr.github.io/python-swirl-statistics/. Não envie esse endereço aos buscadores antes de confirmar a publicação.

1. Configure Settings → Pages → Source → GitHub Actions no repositório. Execute manualmente o workflow “Publicar apresentação no GitHub Pages”. Ele publica somente `site/`, sem respostas de estudantes nem arquivos de preparação de anúncios.
2. Após o job passar, abra a URL devolvida pelo deployment. Confirme respostas HTTP 200 das três páginas e de `sitemap.xml`. Se o domínio ou caminho mudar, atualize todos os canonical, og:url, dados estruturados e URLs do sitemap antes de publicar novamente.
3. Cadastre a URL efetiva no Google Search Console como propriedade de prefixo de URL. Utilize somente a verificação real fornecida pelo painel. Para a subpasta de github.io, não reivindique controle DNS do domínio github.io. Não invente códigos de verificação.
4. Na propriedade verificada, envie o sitemap e inspecione a página inicial e a lição. Solicite indexação quando o painel permitir. Registre a data, a URL e o resultado observado.
5. Adicione e verifique o site no Bing Webmaster Tools, ou importe uma propriedade já verificada do Search Console quando disponível. Envie o sitemap e registre o resultado.
6. Revise posteriormente os relatórios de cobertura/indexação. Envio de sitemap, solicitação de indexação e presença no índice são estados diferentes. Nenhum deles garante posição nos resultados.

## Rastreamento e metadados

Há títulos, descrições, canonical, Open Graph e JSON-LD com informações fiéis ao projeto. `site/sitemap.xml` contém apenas as três páginas públicas, com a data de alteração real. Altere `lastmod` quando houver mudança significativa; não renove a data artificialmente.

`seo/robots-domain-root.txt` é um modelo, não um arquivo ativo. Os buscadores consultam robots.txt na raiz do domínio, não em `/python-swirl-statistics/robots.txt`. Não altere outro repositório nem substitua regras do domínio sem revisar o contexto. A submissão do sitemap na propriedade verificada dispensa colocar esse modelo na subpasta.

Não use endpoints antigos de ping nem a Google Indexing API para estas páginas educacionais comuns. Não há tokens Search Console/Bing nos arquivos, publicação confirmada, submissão realizada ou indexação comprovada nesta preparação. O AdSense preparado não comprova aprovação de site ou indexação e não foi ativado na página.

## Referências oficiais

- https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages
- https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap
- https://developers.google.com/crawling/docs/robots-txt/robots-txt-spec
- https://www.bing.com/webmasters/help/sitemaps-3b5cf6ed

Execute `python scripts/check_site.py` para verificar estrutura e links locais. Isso não verifica disponibilidade HTTP nem indexação.
