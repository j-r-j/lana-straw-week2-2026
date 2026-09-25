# 2026 Volume — Week 2

Week 2 of **Lana Straw Weekly** (The Straw), closed Wednesday, Sept. 23, 2026, before Thursday.
Eleven pages in the Week 1 chrome (Georgia body, crimson/gold, kicker + hed + dek, runhead/folio).

Running order: cover (Otter's daughter's letter to Boom Baum), Editor's Letter + The Week in
Numbers, Boom's 0-2 week, #Pointgate (the kicker-scoring confession that flipped Jerry GM's
Week 1 loss), the Bijan trade, short stories, the knockout, On the Airwaves (S05 EP03, guest
the Guy Next Door), the Desk, Premier and Champeens scoreboards, Point After, colophon.

- `template.html` is the source; `style.css` is inlined into it at build time.
- `build.py` writes `index.html` (photos from `assets/`) and `magazine.html` (photos inlined).
  `python3 build.py --check` prints overflow and bottom slack per page from headless Chrome;
  `--pdf` prints `The_Lana_Straw_Ledger_2026_Week2.pdf`. The build refuses non-ASCII output.
- `assets/` holds the Discord wire photos; `wire_boom_breakfast.jpg` is a still from Otter's
  Sept. 22 video.

Sourcing notes: scores are ESPN finals (the 2026 match record was unsynced at press time).
Quotes are verbatim from the Discord or the S05 EP03 transcript; the transcript's "boom, bomb"
prints as Boom Baum. The Week 1 issue printed Neaux Gold over Jerry by 0.30; the commissioner's
Sept. 15 fix flipped it, and this issue carries the correction. The Guy Next Door / Boom Baum
trade is one deal stored twice. The $5 on the Bijan deal and the 400 FAAB on the Henry deal are
the Hineys' word, not the slip's.
