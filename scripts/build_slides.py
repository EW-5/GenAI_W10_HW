"""Render checked drafts into a self-contained HTML slide deck."""
from html import escape

from validate_slides import ROOT, load_drafts

TITLE = "RAG 是什麼？讓 AI 學會先查資料再回答"


def format_body(line):
    label, separator, detail = line.partition("｜")
    if not separator:
        return escape(line)
    return (f'<strong class="label">{escape(label)}</strong>'
            f'<span class="divider">{separator}</span>{escape(detail)}')



def render_slide(number, slide):
    title, layout, body, citations = slide
    hidden = "" if number == 1 else " hidden"
    content = "\n".join(f'      <li data-field="body">{format_body(line)}</li>' for line in body)
    links = "\n".join(f'      <a data-field="citation" href="{href}">{escape(label)}</a>'
                      for label, href in citations)
    heading = "h1" if number == 1 else "h2"
    heading_text = escape(title)
    if number == 1:
        question, separator, rest = title.partition("？")
        heading_text = (f'{escape(question + separator)}'
                        f'<span class="cover-line">{escape(rest)}</span>')
    body_tag = "ol" if layout == "flow" else "ul"
    return f"""  <section data-slide="{number}" class="{layout}" aria-labelledby="title-{number}"{hidden}>
    <{heading} id="title-{number}" tabindex="-1" data-field="title">{heading_text}</{heading}>
    <{body_tag} class="body">
{content}
    </{body_tag}>
    <div class="references" aria-label="來源與 Wiki 連結">
{links}
    </div>
  </section>"""


TEMPLATE = """<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title><!-- TITLE --></title>
<style>
:root {
  color-scheme: light;
  font-family: "Microsoft JhengHei", "PingFang TC", system-ui, sans-serif;
  color: #242620;
  background: #ebe8df;
  --paper: #fcfaf4;
  --ink: #242620;
  --muted: #53574d;
  --line: #cfcbbd;
  --accent: #8c3a24;
  --serif: Georgia, "Noto Serif TC", "Songti TC", "PMingLiU", serif;
}
* { box-sizing: border-box; }
body { margin: 0; }
.shell { width: min(100% - 2rem, 74rem); margin: auto; }
.top, .controls { display: flex; align-items: center; gap: .85rem; min-height: 3.5rem; }
.top { justify-content: space-between; font-size: .875rem; }
a { color: var(--muted); text-underline-offset: .24em; }
a:hover { color: var(--accent); }
:focus-visible { outline: 2px solid var(--accent); outline-offset: 4px; }
section {
  display: grid;
  grid-template-rows: auto 1fr auto;
  min-height: min(75vh, 45rem);
  align-items: start;
  padding: clamp(1.35rem, 4.5vw, 4rem) clamp(1.35rem, 5.2vw, 5rem) clamp(1rem, 3vw, 2.1rem);
  background: var(--paper);
  border: 1px solid var(--line);
  border-top: 4px solid var(--ink);
  overflow-wrap: anywhere;
}
section[hidden] { display: none; }
section h1, section h2 {
  font-family: var(--serif);
  line-height: 1.18;
  margin: 0 0 clamp(1.3rem, 3.7vw, 3.25rem);
  text-wrap: balance;
}
section h1 { font-size: clamp(2.05rem, 5.7vw, 5.15rem); }
section h2 { font-size: clamp(1.8rem, 4.4vw, 3.55rem); }
.intro { border-top-color: var(--accent); }
.intro h1 { max-width: 12em; }
.intro h1 .cover-line { display: block; color: var(--accent); }
.body {
  margin: 0;
  padding-inline-start: 1.15em;
  max-width: 39em;
  font-size: clamp(1.04rem, 2vw, 1.57rem);
  line-height: 1.63;
}
.body li + li { margin-top: .5em; }
.body li::marker { color: var(--accent); }
.label { color: var(--accent); font-weight: 700; }
.compare .body {
  list-style: none;
  padding: 0;
  max-width: none;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: clamp(1.35rem, 4vw, 3.6rem);
}
.compare .body li {
  margin: 0;
  padding-top: .85rem;
  border-top: 2px solid var(--ink);
}
.compare .body li + li { border-top-color: var(--accent); }
.compare .label { display: block; margin-bottom: .38rem; font-size: 1.08em; }
.compare .divider { font-size: 0; }
.flow .body { max-width: none; padding-inline-start: 1.4em; }
.flow .body li {
  margin: 0;
  border-bottom: 1px solid var(--line);
  padding: .35rem 0 .35rem .25rem;
}
.flow .body li:last-child { border: 0; }
.summary .body { font-weight: 600; }
.references {
  display: flex;
  flex-wrap: wrap;
  column-gap: 1.15rem;
  row-gap: .3rem;
  border-top: 1px solid var(--line);
  padding-top: .7rem;
  margin-top: clamp(1.15rem, 2.5vw, 2rem);
  font-size: .8rem;
  line-height: 1.43;
}
.controls { justify-content: center; }
button {
  font: inherit;
  font-size: .875rem;
  background: transparent;
  border: 1px solid #929383;
  color: var(--ink);
  padding: .35rem .85rem;
  cursor: pointer;
}
button:hover:not(:disabled) { border-color: var(--accent); color: var(--accent); }
button:disabled { opacity: .45; cursor: default; }
#counter { min-width: 6ch; text-align: center; color: var(--muted); font-variant-numeric: tabular-nums; }
@media (max-width: 620px) {
  .shell { width: calc(100% - 1.25rem); }
  section { min-height: min(70vh, 36rem); }
  .compare .body { grid-template-columns: 1fr; gap: 1.1rem; }
  .references { font-size: .75rem; }
}
</style>
</head>
<body>
<div class="shell">
  <nav class="top" aria-label="專案連結"><a href="index.html">專案首頁</a><a href="wiki.html">LLM Wiki</a></nav>
  <main aria-label="RAG 教學簡報">
<!-- SLIDES -->
  </main>
  <nav class="controls" aria-label="簡報切換">
    <button id="prev" type="button" disabled>← 上一頁</button>
    <output id="counter" aria-live="polite">1 / 10</output>
    <button id="next" type="button">下一頁 →</button>
  </nav>
</div>
<script>
const slides = Array.from(document.querySelectorAll('[data-slide]'));
const previous = document.querySelector('#prev');
const next = document.querySelector('#next');
const counter = document.querySelector('#counter');
let current = 0;

function show(index) {
  if (index < 0 || index >= slides.length) return;
  slides[current].hidden = true;
  current = index;
  slides[current].hidden = false;
  counter.textContent = (current + 1) + ' / ' + slides.length;
  previous.disabled = current === 0;
  next.disabled = current === slides.length - 1;
  slides[current].querySelector('[data-field="title"]').focus({ preventScroll: true });
  window.scrollTo(0, 0);
}

previous.addEventListener('click', () => show(current - 1));
next.addEventListener('click', () => show(current + 1));
window.addEventListener('keydown', event => {
  if (event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) return;
  if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
    event.preventDefault();
    show(current + (event.key === 'ArrowRight' ? 1 : -1));
  }
});
</script>
</body>
</html>
"""


if __name__ == "__main__":
    slides = load_drafts()
    sections = "\n".join(render_slide(n, slide) for n, slide in enumerate(slides, 1))
    html = TEMPLATE.replace("<!-- TITLE -->", escape(TITLE)).replace("<!-- SLIDES -->", sections)
    (ROOT / "slides.html").write_text(html, encoding="utf-8", newline="\n")
    print(f"Built slides.html from {len(slides)} checked drafts.")
