"""Validate draft evidence and compare rendered slide text with the approved drafts."""
import argparse
from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.parse import urlsplit

from build_wiki import LINK, ROOT, section_id

WORKFLOW = ROOT / "workflow"
REF = re.compile(r"- (?:([C]\d{2}) )?\[([^\]]+)\]\(([^)]+)\)")
BODY = re.compile(r"- (C\d{2}) (.+)")
LAYOUTS = {"intro", "list", "compare", "flow", "summary"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read(path):
    return path.read_text(encoding="utf-8").strip()


def wiki_target(file, href):
    target = (file.parent / href).resolve()
    require(target.is_file() and target.is_relative_to(ROOT / "wiki"),
            f"{file.name}: invalid Wiki target {href}")
    return target


def load_cards():
    cards = {}
    for path in sorted((WORKFLOW / "cards").glob("C*.md")):
        links = dict(LINK.findall(read(path)))
        wiki = wiki_target(path, links.pop("Wiki 條目"))
        origins = {name[-3:]: href for name, href in links.items() if name.startswith("原始文件 ")}
        links = {name: href for name, href in links.items() if not name.startswith("原始文件 ")}
        require(bool(links), f"{path.stem}: missing source locator")
        entries = set()
        for label, href in links.items():
            source = wiki_target(path, href)
            source_text = read(source)
            original = origins.get(source.stem, "")
            require(re.match(r"^S\d{2}(?:\s|「)", label) and
                    source.stem == label[:3] and source.parent.name == "sources",
                    f"{path.stem}: source ID does not match its source page")
            require((label, f"../sources/{source.name}") in LINK.findall(read(wiki)),
                    f"{path.stem}: source locator not found in the concept page")
            require(dict(LINK.findall(source_text)).get("原始文件") == original
                    and urlsplit(original).scheme == "https"
                    and "- Ingest 狀態：完成" in source_text.splitlines(),
                    f"{path.stem}: original source does not match the ingested record")
            entries.add((label, wiki))
        cards[path.stem] = entries
    return cards


def load_drafts():
    cards = load_cards()
    pages = sorted((WORKFLOW / "drafts").glob("*.md"))
    require([p.stem for p in pages] == [f"{n:02}" for n in range(1, 11)],
            "expected drafts 01–10")
    outline = read(WORKFLOW / "outline.md").splitlines()
    slides = []
    for page in pages:
        header, layout, body_heading, body, refs_heading, refs = read(page).split("\n\n")
        prefix = f"# {page.stem} · "
        require(header.startswith(prefix) and len(header) > len(prefix), f"{page.name}: invalid title")
        title = header.removeprefix(prefix)
        require(any(line.startswith(f"{int(page.stem)}. {title}。") for line in outline),
                f"{page.name}: title missing from outline")
        layout = layout.removeprefix("版型：")
        require(layout in LAYOUTS, f"{page.name}: invalid layout")
        require((body_heading, refs_heading) == ("## 正文", "## 引用"),
                f"{page.name}: missing body or citations")
        claims = [BODY.fullmatch(line) for line in body.splitlines()]
        require(claims and all(claims), f"{page.name}: invalid claim/evidence format")
        claim_ids = {match[1] for match in claims}
        text = [match[2] for match in claims]
        citations = []
        used = {}
        references = set()
        for line in refs.splitlines():
            match = REF.fullmatch(line)
            require(match is not None, f"{page.name}: invalid citation {line}")
            card, label, href = match.groups()
            target = wiki_target(page, href)
            if card:
                require((label, target) in cards.get(card, set()) and
                        (label, target) not in used.get(card, set()),
                        f"{page.name}: citation does not match {card}: {label}")
                used.setdefault(card, set()).add((label, target))
            else:
                source = label.split(" · ", 1)[0]
                require(page.stem == "10" and re.fullmatch("S0[1-5]", source)
                        and target == ROOT / "wiki" / "sources" / f"{source}.md",
                        f"{page.name}: invalid bibliography entry {label}")
                references.add(source)
            citations.append((label, f"wiki.html#{section_id(target)}"))
        require(set(used) == claim_ids and all(used[c] == cards[c] for c in used), f"{page.name}: claims and evidence citations differ")
        if page.stem == "10":
            require(references == {f"S0{i}" for i in range(1, 6)}, "incomplete final bibliography")
        slides.append((title, layout, text, citations))
    return slides


class SlideText(HTMLParser):
    """Extract only visible slide content fields, ignoring navigation and styling."""
    def __init__(self):
        super().__init__()
        self.slides = []
        self.slide = None
        self.field = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "section" and "data-slide" in attrs:
            self.slide = [attrs["data-slide"], "", [], []]
        if self.slide is not None and "data-field" in attrs:
            self.field = (tag, attrs["data-field"], attrs.get("href"), [])

    def handle_data(self, data):
        if self.field is not None:
            self.field[3].append(data)

    def handle_endtag(self, tag):
        if self.field is not None and tag == self.field[0]:
            _, name, href, pieces = self.field
            value = "".join(pieces)
            if name == "title":
                self.slide[1] = value
            elif name == "body":
                self.slide[2].append(value)
            elif name == "citation":
                self.slide[3].append((value, href))
            self.field = None
        if tag == "section" and self.slide is not None:
            self.slides.append(self.slide)
            self.slide = None


class WikiAnchors(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if "id" in values:
            self.ids.add(values["id"])


def validate_html(slides, html):
    rendered = SlideText()
    rendered.feed(html)
    expected = [[str(n), title, body, refs]
                for n, (title, _, body, refs) in enumerate(slides, 1)]
    require(len(rendered.slides) == len(expected), "HTML slide count differs from drafts")
    for actual, draft in zip(rendered.slides, expected):
        require(actual == draft, f"slide {draft[0]}: HTML title/body/citations differ from draft")
    anchors = WikiAnchors()
    anchors.feed(read(ROOT / "wiki.html"))
    for _, _, _, refs in slides:
        for label, href in refs:
            require(urlsplit(href).fragment in anchors.ids, f"missing Wiki anchor for {label}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cards", action="store_true", help="run the N3 evidence link check")
    parser.add_argument("--drafts", action="store_true", help="run N6 checks before building HTML")
    args = parser.parse_args()
    try:
        if args.cards:
            cards = load_cards()
            require(bool(cards), "no evidence cards found")
            print(f"PASS evidence: {len(cards)} cards, {sum(map(len, cards.values()))} Wiki locators")
            return
        slides = load_drafts()
        claims = sum(len(body) for _, _, body, _ in slides)
        refs = sum(len(refs) for _, _, _, refs in slides)
        print(f"PASS drafts: {len(slides)} pages, {claims} body items, {refs} citations")
        if not args.drafts:
            validate_html(slides, read(ROOT / "slides.html"))
            print(f"PASS HTML: {len(slides)} exact title/body/citation matches; {refs} Wiki anchors")
    except (OSError, KeyError, ValueError) as error:
        parser.exit(1, f"FAIL {error}\n")


if __name__ == "__main__":
    main()
