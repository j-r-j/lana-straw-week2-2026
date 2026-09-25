"""Build the Week 2 issue: template.html + style.css -> index.html, magazine.html.

index.html references assets/; magazine.html inlines every photo so it opens as one file.
`python3 build.py --check` prints per-page overflow and bottom slack from headless Chrome;
`--pdf` prints index.html to The_Lana_Straw_Ledger_2026_Week2.pdf.
"""
import base64, pathlib, re, subprocess, sys

HERE = pathlib.Path(__file__).parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=850"/>
<link rel="icon" href="favicon.ico" sizes="16x16">
<title>Lana Straw Weekly &#183; Week 2, 2026</title>
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
    html = HEAD + f"<style>\n{css}\n</style>\n" + body + "\n</body>\n</html>\n"
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
    if "--pdf" in sys.argv:
        chrome("--no-pdf-header-footer", f"--print-to-pdf={HERE / 'The_Lana_Straw_Ledger_2026_Week2.pdf'}",
               (HERE / "index.html").as_uri())


if __name__ == "__main__":
    main()
