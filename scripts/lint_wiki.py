"""Check source records, references, local links, and the generated HTML."""
from html.parser import HTMLParser
import re
from urllib.parse import unquote, urlsplit

from build_wiki import LINK, ROOT, document, wiki_pages

SOURCE_ID = re.compile(r"\bS\d{2,}\b")
CORE = {
    "rag", "llm-limits", "flow", "chunking", "embedding",
    "retrieval", "generation", "applications", "limits",
}


class HtmlLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.links = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if "id" in values:
            self.ids.add(values["id"])
        if tag == "a" and "href" in values:
            self.links.append(values["href"])


def check_links(page, links, errors, anchors=None):
    count = 0
    for href in links:
        url = urlsplit(href)
        if url.scheme or url.netloc:
            continue
        count += 1
        path = page.parent / unquote(url.path) if url.path else page
        if not path.is_file() and not path.is_dir():
            errors.append(f"{page.relative_to(ROOT)}: missing target {href}")
        elif anchors is not None and path == page and url.fragment not in anchors:
            errors.append(f"{page.relative_to(ROOT)}: missing anchor {href}")
    return count


def main():
    errors = []
    pages = {page: page.read_text(encoding="utf-8") for page in wiki_pages()}
    sources = {page.stem: content for page, content in pages.items()
               if page.parent.name == "sources" and SOURCE_ID.fullmatch(page.stem)}
    ingested = set()
    for source, content in sources.items():
        has_url = any(label == "原始文件" and urlsplit(url).scheme == "https"
                      and urlsplit(url).hostname for label, url in LINK.findall(content))
        if not has_url:
            errors.append(f"{source}: missing original HTTPS source link")
        if has_url and "- Ingest 狀態：完成" in content.splitlines() and "## 摘要與定位" in content:
            ingested.add(source)
    required = {f"S{number:02}" for number in range(1, 6)}
    if not required <= ingested:
        errors.append("Incomplete ingest: " + ", ".join(sorted(required - ingested)))

    concepts = {page.stem for page in pages if page.parent.name == "concepts"}
    if CORE - concepts:
        errors.append("Missing concept pages: " + ", ".join(sorted(CORE - concepts)))
    citation_pages = 0
    link_count = 0
    for page, content in pages.items():
        links = LINK.findall(content)
        link_count += check_links(page, [href for _, href in links], errors)
        invalid = set(SOURCE_ID.findall(content)) - ingested
        if invalid:
            errors.append(f"{page.name}: invalid source IDs {', '.join(sorted(invalid))}")
        if page.parent.name == "concepts":
            has_citation = any(
                label.startswith(source + " ") and label.strip() != source
                and href == f"../sources/{source}.md"
                for label, href in links for source in ingested
            )
            if has_citation:
                citation_pages += 1
            else:
                errors.append(f"{page.name}: missing linked source with a section locator")

    html_page = ROOT / "wiki.html"
    html_links = 0
    if html_page.is_file():
        html = html_page.read_text(encoding="utf-8")
        if html != document():
            errors.append("wiki.html differs from the Markdown build")
        parser = HtmlLinks()
        parser.feed(html)
        html_links = check_links(html_page, parser.links, errors, parser.ids)
    else:
        errors.append("Missing wiki.html")

    print(f"Ingested with an original HTTPS link: {len(ingested)} ({', '.join(sorted(ingested))})")
    print(f"Wiki Markdown pages checked for source IDs: {len(pages)}")
    print(f"Concept pages with section citations: {citation_pages}/{len(concepts)}")
    print(f"Local Markdown links checked: {link_count}")
    print(f"Local HTML links checked: {html_links}")
    for error in errors:
        print(f"ERROR: {error}")
    print(f"{'FAIL' if errors else 'PASS'}: {len(errors)} error(s)")
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
