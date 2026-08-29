# greg-icra27.github.io

Project page for **Greg: Guided Reinforcement Fine-Tuning for Sensorimotor Driving**,
under double-anonymous review at ICRA 2027. It hosts implementation details, ablations,
Grad-CAM visualizations, failure cases, the video, and the code release.

**ICRA has no supplementary material.** Everything that carries the argument must live in
the 8-page PDF; this page is an optional extra that reviewers are not obliged to open, and
it must not be load-bearing. The page is deliberately framed as a *project page*, never as
a supplement.

## Layout

```
index.html               the whole page (self-contained CSS, MathJax from CDN)
static/images/           every figure, rasterized for the web
static/videos/           supplementary.mp4, the supplementary video
static/code/             greg_code.zip, the anonymized code release
tools/                   the LaTeX -> HTML build scripts
.nojekyll                tells GitHub Pages to serve the files as-is
```

## Publishing

Settings -> Pages -> Source: *Deploy from a branch*, branch `main`, folder `/ (root)`.
The site then serves at `https://greg-icra27.github.io/`.

The repo name must stay `greg-icra27.github.io`, matching the org. GitHub serves an org page
only when the repo is named `<org>.github.io`; under any other name it becomes a *project*
page at `https://greg-icra27.github.io/<repo>/`, and the URL printed in the paper 404s.

**Note:** GitHub Pages will only publish from a *private* repository on a paid plan
(Pro / Team / Enterprise). On a free plan the repo has to be public for the URL to go
live. The files can sit here privately until you are ready either way.

## Video and code

`static/videos/supplementary.mp4` (30 MB) is the supplementary video, re-encoded from the
1080p master at CRF 23 so it stays well under GitHub's 100 MB per-file limit. It plays
inline in the `#video` section.

`static/code/greg_code.zip` (2.5 MB) is the code release, linked from the header button and
the `#code` section. It was anonymized before packaging: absolute paths that named
an author, a home directory, a cluster mount point, or the experiment-tracker entity were
replaced with placeholders.

**Re-run that check on any new drop**, before it is committed. Unzip it and grep for your
own identifiers -- username, surname, institution, cluster mount points, tracker entity --
plus the generic shapes they hide in:

```bash
grep -rIhoE '/[a-z][a-z0-9_]*/[A-Za-z0-9_.-]+' <unzipped> | sort -u | head -50
grep -rIhoE '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}' <unzipped> | sort -u
```

The first lists every absolute path prefix in the archive, the second every email address;
anything in either that is not upstream third-party code has to go. Do not commit the
literal identifiers into this repo -- it is the public artifact.

## Adding the paper PDF

The paper PDF is not published while the paper is under review. To add it once review
concludes, copy the PDF into the repo root as `main.pdf` and point the disabled
"Paper (coming soon)" button in `index.html` at it.

## Rebuilding from the LaTeX source

The page is generated from `sections/supplementary.tex` in the paper repo. From a checkout
of the paper repo:

```bash
python3 tools/assets.py    # rasterize every referenced figure into static/images/
python3 tools/build.py     # supplementary.tex -> body.html + toc.html + refs.html
python3 tools/page.py      # stitch everything into index.html
```

`tools/build.py` resolves cross-references, citations (from `supplemental.bbl`), tables,
algorithms, and equations. References into the main paper are resolved from `main.aux`,
so compile `main.tex` first if those numbers have moved. Equations, figures, tables, and
sections are numbered with an `S` prefix, matching the supplement; plain numbers in the
text refer to the main paper.

The scripts read the paper repo from `$GREG_PAPER_DIR`, defaulting to `../GREG_paper`.
Point it wherever your checkout lives:

```bash
GREG_PAPER_DIR=/path/to/GREG_paper python3 tools/build.py
```

Never hard-code that path back into the scripts: this repo is the public artifact, and an
absolute path is an identifier.

## Cross-references into the main paper

The page body is generated from `supplementary.tex`, whose `MAIN-` prefixed `\ref`s point
into the main paper. `tools/build.py` resolves them against `ICRA/icra8/greg_icra8.aux`, so
the numbers on the page always match the 8-page ICRA build and no manual remapping is
needed. Set `GREG_MAIN_AUX` to resolve against a different build of the paper.

Build the paper first: a stale or missing `.aux` leaves the numbers unresolved, and
`tools/build.py` reports them at the end of its run.

Check for regressions with:

```bash
grep -oE '<span class="mainref">[^<]+</span>' index.html | sort -u
```

Only Fig. 1-3, Eq. 1-8, Table I-III, and Sec. I-V (with -A..-D) are valid.

`supplemental.pdf` is **not** published: it is the journal-length supplement, and its
internal cross-references point at the 16-page manuscript rather than the submitted paper.
The page body supersedes it. Restore with `git checkout <rev> -- supplemental.pdf` if that
ever changes.
