"""Build the Week 2 issue: template.html + style.css -> index.html, magazine.html.

index.html references assets/; magazine.html inlines every photo so it opens as one file.
`python3 build.py --check` prints per-page overflow and bottom slack from headless Chrome;
`--pdf` prints index.html to The_Lana_Straw_Ledger_2026_Week2.pdf.
"""
import base64, json, pathlib, re, subprocess, sys

HERE = pathlib.Path(__file__).parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
BASE = "https://j-r-j.github.io/lana-straw-week2-2026/"
DESC = ("Boom Baum is 0-2 and asked the league for forty-five trades. The league sent him a letter from a child. "
        "Plus #Pointgate, Bijan on the move again, and a knockout bid with one zero too many.")
JSONLD = {
    "@context": "https://schema.org",
    "@graph": [
        {
            "@type": "Periodical", "@id": BASE + "#periodical", "name": "Lana Straw Weekly",
            "alternateName": "The Straw", "genre": "Fantasy football league magazine",
        },
        {
            "@type": "PublicationIssue", "@id": BASE + "#issue", "issueNumber": "2",
            "name": "Week 2, 2026", "datePublished": "2026-09-23",
            "isPartOf": {"@id": BASE + "#periodical"}, "url": BASE, "image": BASE + "og-image.jpg",
            "encoding": {"@type": "MediaObject", "encodingFormat": "application/pdf",
                         "contentUrl": BASE + "The_Lana_Straw_Ledger_2026_Week2.pdf"},
        },
        {
            "@type": "NewsArticle", "@id": BASE + "#cover-story", "isPartOf": {"@id": BASE + "#issue"},
            "headline": "Maybe You Should Make Sume Trades?",
            "alternativeHeadline": "The Minimum Is 45",
            "description": DESC,
            "image": [BASE + "og-image.jpg", BASE + "assets/wire_otter.jpg", BASE + "assets/wire_boom_breakfast.jpg"],
            "datePublished": "2026-09-23", "inLanguage": "en-US", "url": BASE,
            "author": {"@type": "Organization", "name": "The Straw editors"},
            "publisher": {"@type": "Organization", "name": "Lana Straw Weekly"},
            "about": [
                {"@type": "SportsTeam", "name": "Boom Baum"},
                {"@type": "SportsTeam", "name": "Fart Toot Squeek"},
                {"@type": "SportsTeam", "name": "Jerry GM + Jerry Owner"},
                {"@type": "SportsTeam", "name": "Shiny Hineys"},
                {"@type": "SportsTeam", "name": "The Kickers n Jigba"},
            ],
            "keywords": "Lana Straw, fantasy football, #Pointgate, Bijan Robinson, knockout league, Week 2",
            "hasPart": [
                {"@type": "WebPageElement", "name": "A Grave Mistake", "description": "#Pointgate: the kicker-scoring confession that flipped a Week 1 result."},
                {"@type": "WebPageElement", "name": "Was That a Real Trade?!", "description": "Bijan Robinson changes addresses again."},
                {"@type": "WebPageElement", "name": "Double Tap the Zero", "description": "The knockout league, and a hundred-dollar bid with an extra zero."},
                {"@type": "WebPageElement", "name": "I'm Not Going to Overreact", "description": "On the Airwaves: S05 EP03 with the Guy Next Door."},
            ],
        },
    ],
}

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=850"/>
<link rel="icon" href="favicon.ico" sizes="16x16">
<title>Maybe You Should Make Sume Trades? &#183; Lana Straw Weekly, Week 2</title>
<meta name="description" content="{DESC}"/>
<link rel="canonical" href="{BASE}"/>
<meta name="theme-color" content="#8a1a28"/>
<meta property="og:type" content="article"/>
<meta property="og:site_name" content="Lana Straw Weekly"/>
<meta property="og:url" content="{BASE}"/>
<meta property="og:title" content="Maybe You Should Make Sume Trades?"/>
<meta property="og:description" content="{DESC}"/>
<meta property="og:image" content="{BASE}og-image.jpg"/>
<meta property="og:image:type" content="image/jpeg"/>
<meta property="og:image:width" content="1200"/>
<meta property="og:image:height" content="630"/>
<meta property="og:image:alt" content="A child's handwritten letter to Boom Baum, pinned beside a photo of him reading it at breakfast"/>
<meta property="article:published_time" content="2026-09-23T23:59:00-05:00"/>
<meta property="article:section" content="Week 2"/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:title" content="Maybe You Should Make Sume Trades?"/>
<meta name="twitter:description" content="{DESC}"/>
<meta name="twitter:image" content="{BASE}og-image.jpg"/>
<script type="application/ld+json">
{JSONLD}
</script>
</head>
<body>
<div class="share-bar">
  <div class="brand">Lana Straw Weekly &#183; Week 2, 2026</div>
  <div class="actions">
    <a class="pdf" href="The_Lana_Straw_Ledger_2026_Week2.pdf">Download PDF</a>
    <a class="top" href="#top">Top</a>
  </div>
</div>
<a id="top"></a>
"""

CHECK_JS = """<script>
window.addEventListener('load', function () {
  var out = [];
  document.querySelectorAll('.page').forEach(function (pg, i) {
    var flow = pg.querySelector('.flow');
    var over = 0, slack = 0;
    if (flow) {
      over = flow.scrollHeight - flow.clientHeight;
      var sp = flow.querySelector(':scope > .spacer');
      slack = sp ? sp.getBoundingClientRect().height : 0;
    }
    out.push('p' + (i + 1) + ' over=' + over + ' slack=' + Math.round(slack));
  });
  document.body.setAttribute('data-check', out.join(' | '));
});
</script>"""


def head():
    ld = json.dumps(JSONLD, indent=1, ensure_ascii=True).replace("</", "<\\/")
    return HEAD.replace("{BASE}", BASE).replace("{DESC}", DESC).replace("{JSONLD}", ld)


def render(inline_images):
    body = (HERE / "template.html").read_text().split("{{STYLE}}", 1)[1]
    css = (HERE / "style.css").read_text()

    def img(match):
        name = match.group(1).lower() + ".jpg"
        if not inline_images:
            return f"assets/{name}"
        data = base64.b64encode((HERE / "assets" / name).read_bytes()).decode()
        return f"data:image/jpeg;base64,{data}"

    body = re.sub(r"\{\{(WIRE_[A-Z_]+)\}\}", img, body)
    html = head() + f"<style>\n{css}\n</style>\n" + body + "\n</body>\n</html>\n"
    if re.search(r"[^\x00-\x7f]", html):
        sys.exit("non-ASCII character in output")
    return html


def chrome(*args):
    return subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--virtual-time-budget=4000", *args],
                          capture_output=True, text=True).stdout


def main():
    (HERE / "index.html").write_text(render(False))
    (HERE / "magazine.html").write_text(render(True))
    if "--check" in sys.argv:
        probe = HERE / "_check.html"
        probe.write_text(render(False).replace("</body>", CHECK_JS + "</body>"))
        dom = chrome("--dump-dom", probe.as_uri())
        probe.unlink()
        m = re.search(r'data-check="([^"]*)"', dom)
        print(m.group(1).replace(" | ", "\n") if m else "no check output")
    if "--og" in sys.argv:
        png = HERE / "_og.png"
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--window-size=1200,630",
                        "--virtual-time-budget=3000", f"--screenshot={png}", (HERE / "og-card.html").as_uri()],
                       capture_output=True)
        subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "88", str(png),
                        "--out", str(HERE / "og-image.jpg")], capture_output=True)
        png.unlink()
    if "--pdf" in sys.argv:
        chrome("--no-pdf-header-footer", f"--print-to-pdf={HERE / 'The_Lana_Straw_Ledger_2026_Week2.pdf'}",
               (HERE / "index.html").as_uri())


if __name__ == "__main__":
    main()
