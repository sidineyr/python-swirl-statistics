"""Check local public pages; does not verify hosting or search indexing."""
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1] / "site"
BASE = "https://sidineyr.github.io/python-swirl-statistics/"

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.canonical = []
        self.links = []
        self.titles = 0
        self.in_svg = False
        self.headings = 0
        self.json_blocks = []
        self.in_json = False
        self.ids = set()
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"): self.ids.add(attrs["id"])
        if attrs.get("src"): self.links.append(attrs["src"])
        if tag == "svg": self.in_svg = True
        if tag == "title" and not self.in_svg: self.titles += 1
        if tag == "h1": self.headings += 1
        if tag == "link" and attrs.get("rel") == "canonical": self.canonical.append(attrs["href"])
        if tag in ("a", "link") and attrs.get("href"): self.links.append(attrs["href"])
        if tag == "meta" and attrs.get("name", "").lower() == "robots":
            assert "noindex" not in attrs.get("content", "").lower(), "Unexpected noindex"
        if tag == "script" and attrs.get("type") == "application/ld+json":
            self.in_json = True
            self.json_blocks.append("")
    def handle_data(self, data):
        if self.in_json: self.json_blocks[-1] += data
    def handle_endtag(self, tag):
        if tag == "svg": self.in_svg = False
        if tag == "script": self.in_json = False

pages = sorted(ROOT.glob("*.html"))
modules = json.loads((ROOT.parent / 'curriculum/modules.json').read_text(encoding='utf-8'))
assert len(modules) == 10 and len({module['slug'] for module in modules}) == 10
expected_pages = {module['slug'] + '.html' for module in modules} | {
    'index.html', 'como-estudar.html', 'recursos.html', 'instalacao.html',
    'privacidade.html', 'media-mediana.html', 'dispersao.html', 'amostragem.html',
    'materiais.html',
}
assert {path.name for path in pages} == expected_pages, 'Missing or unexpected public pages'
assert (ROOT / 'assets/educational-ads.js').read_bytes() == (
    ROOT.parent / 'scripts/templates/educational-ads.js'
).read_bytes(), 'Generated affiliate module differs from its reviewed source'
urls = []
for path in pages:
    parsed = Page()
    parsed.feed(path.read_text(encoding="utf-8"))
    assert parsed.titles == 1 and parsed.headings == 1, path.name
    assert parsed.canonical == [BASE + path.name], path.name
    assert parsed.json_blocks, path.name
    assert 'conteudo' in parsed.ids and '#conteudo' in parsed.links, path.name
    if path.name in ('media-mediana.html', 'dispersao.html', 'amostragem.html'):
        assert 'prediction-note' in parsed.ids and any(urlparse(link).path == 'activities.js' for link in parsed.links), path.name
    for block in parsed.json_blocks:
        data = json.loads(block)
        assert data["url"] == parsed.canonical[0]
    for href in parsed.links:
        if not urlparse(href).scheme:
            parsed_url = urlparse(href)
            target = path.parent / parsed_url.path if parsed_url.path else path
            assert target.is_file(), (path.name, href)
            if parsed_url.fragment:
                target_page = Page()
                target_page.feed(target.read_text(encoding="utf-8"))
                assert parsed_url.fragment in target_page.ids, (path.name, href)
    urls.extend(parsed.canonical)
sitemap = ET.parse(ROOT / "sitemap.xml")
locations = [node.text for node in sitemap.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
assert sorted(locations) == sorted(urls)
print(f"OK: {len(pages)} pages, canonical URLs, JSON-LD, local links, reviewed affiliate module and sitemap")

