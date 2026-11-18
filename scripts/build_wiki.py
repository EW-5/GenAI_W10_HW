"""Build the static browser view from the Wiki's Markdown files."""
from html import escape
from pathlib import Path
import re
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"\[([^\]\n]+)\]\(([^)\s]+)\)")
INLINE = re.compile(r"\[([^\]\n]+)\]\(([^)\s]+)\)|\*\*([^*]+)\*\*")


def wiki_pages():
    wiki = ROOT / "wiki"
    return [wiki / "index.md", *sorted(wiki.glob("*/*.md")), wiki / "log.md"]


def section_id(path):
    return path.relative_to(ROOT / "wiki").with_suffix("").as_posix().replace("/", "-")


def render_inline(line, page, pages):
    parts = []
    previous = 0
    for match in INLINE.finditer(line):
        parts.append(escape(line[previous:match.start()]))
        label, href, bold = match.groups()
        if bold:
            parts.append(f"<strong>{escape(bold)}</strong>")
        else:
            url = urlsplit(href)
            if not url.scheme and not url.netloc:
                target = (page.parent / url.path).resolve()
                if target in pages and not url.fragment:
                    href = f"#{section_id(target)}"
                else:
                    href = target.relative_to(ROOT).as_posix()
                    if url.fragment:
                        href += f"#{url.fragment}"
                    if href == "wiki.html":
                        href = "#index"
            parts.append(f'<a href="{escape(href, quote=True)}">{escape(label)}</a>')
        previous = match.end()
    parts.append(escape(line[previous:]))
    return "".join(parts)


def render_page(page, pages):
    lines = page.read_text(encoding="utf-8").strip().splitlines()
    title = lines[0].removeprefix("# ")
    blocks = [f"<h2>{escape(title)}</h2>"]
    for block in "\n".join(lines[1:]).strip().split("\n\n"):
        if block.startswith("## "):
            blocks.append(f"<h3>{escape(block[3:])}</h3>")
        elif block.startswith("- "):
            items = [f"<li>{render_inline(line[2:], page, pages)}</li>"
                     for line in block.splitlines()]
            blocks.append("<ul>\n" + "\n".join(items) + "\n</ul>")
        else:
            blocks.append(f"<p>{render_inline(block, page, pages)}</p>")
    return f'<article id="{section_id(page)}">\n' + "\n".join(blocks) + "\n</article>"


def document():
    pages = wiki_pages()
    articles = "\n".join(render_page(page, pages) for page in pages)
    return TEMPLATE.replace("<!-- ARTICLES -->", articles)


TEMPLATE = """<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>RAG 檢索增強生成入門</title>
<style>
:root { color-scheme: light; background: #f5f7f5; color: #172b2a; }
body { margin: 0 auto; max-width: 54rem; padding: 1rem; font: 1.05rem/1.75 system-ui, sans-serif; }
header { display: flex; align-items: baseline; justify-content: space-between; flex-wrap: wrap; gap: .5rem 1rem; }
h1 { font-size: clamp(1.45rem, 4vw, 2.1rem); line-height: 1.3; }
nav { display: flex; gap: 1rem; }
a { color: #075c51; text-underline-offset: .18em; }
a:focus-visible { outline: 2px solid #075c51; outline-offset: 3px; }
article { margin: 1rem 0; padding: clamp(1rem, 3vw, 2rem); background: #fff;
  border: 1px solid #d3ded9; border-radius: .65rem; scroll-margin-top: 1rem; overflow-wrap: anywhere; }
article:target { border-color: #075c51; }
h2 { margin-top: 0; }
li + li { margin-top: .35rem; }
</style>
</head>
<body>
<header id="top">
  <h1>RAG 檢索增強生成入門</h1>
  <nav aria-label="Wiki 導覽">
    <a href="#index">知識索引</a>
    <a href="#log">維護紀錄</a>
    <a href="wiki/index.md">Markdown</a>
  </nav>
</header>
<main>
<!-- ARTICLES -->
</main>
<footer><a href="#top">回頁首</a></footer>
<script>
  // When following a Wiki link, move keyboard focus to the selected article.
  function focusArticle() {
    const article = document.getElementById(location.hash.slice(1));
    if (article?.matches('article')) {
      article.tabIndex = -1;
      article.focus({ preventScroll: true });
    }
  }
  window.addEventListener('hashchange', focusArticle);
  focusArticle();
</script>
</body>
</html>
"""


if __name__ == "__main__":
    (ROOT / "wiki.html").write_text(document(), encoding="utf-8")
    print(f"Built wiki.html from {len(wiki_pages())} Markdown pages.")
