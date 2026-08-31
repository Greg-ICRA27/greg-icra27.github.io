#!/usr/bin/env python3
"""Assemble site/index.html from the converted body, TOC and references."""
import os, json, shutil, subprocess

OUT = os.path.dirname(os.path.abspath(__file__))
PAPER = os.environ.get('GREG_PAPER_DIR', '../GREG_paper')
SITE = os.environ.get('GREG_SITE_DIR', os.path.dirname(OUT))

body = open(os.path.join(OUT, 'body.html')).read()
toc = open(os.path.join(OUT, 'toc.html')).read()
refs = open(os.path.join(OUT, 'refs.html')).read()
macros = json.load(open(os.path.join(OUT, 'macros.json')))

TITLE = 'Greg: Guided Reinforcement Fine-Tuning for Sensorimotor Driving'



BIBTEX = """@article{greg2026,
  title   = {Greg: Guided Reinforcement Fine-Tuning for Sensorimotor Driving},
  author  = {Anonymous},
  journal = {Under review},
  year    = {2026}
}"""

CSS = r"""
:root{
  --bg:#ffffff; --fg:#1a1c1f; --muted:#5c6470; --line:#e3e6ea; --soft:#f6f7f9;
  --accent:#1f5fd0; --accent-soft:#e8f0fd; --best:#dff3e3; --second:#eef3fb;
  --gain:#dff3e3; --drop:#fbe4e4; --maxw:860px;
}
@media (prefers-color-scheme: dark){
  :root{ --bg:#14161a; --fg:#e7e9ec; --muted:#9aa3ae; --line:#2b3038; --soft:#1b1e24;
         --accent:#7ba7f0; --accent-soft:#1e2836; --best:#1e3326; --second:#1d2735;
         --gain:#1e3326; --drop:#3a2323; }
}
*{box-sizing:border-box}
html{scroll-behavior:smooth; scroll-padding-top:1.2rem}
body{margin:0;background:var(--bg);color:var(--fg);
     font:16px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,Helvetica,Arial,sans-serif;
     -webkit-font-smoothing:antialiased}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
.wrap{max-width:var(--maxw);margin:0 auto;padding:0 20px}

/* ---------- hero ---------- */
header.hero{padding:56px 0 28px;border-bottom:1px solid var(--line);background:var(--soft)}
.kicker{text-transform:uppercase;letter-spacing:.14em;font-size:.72rem;color:var(--muted);
        font-weight:600;margin-bottom:14px}
h1.title{font-size:2.05rem;line-height:1.22;margin:0 0 18px;font-weight:700;letter-spacing:-.015em}
.authors{color:var(--muted);font-size:.95rem;margin-bottom:6px}
.venue{color:var(--muted);font-size:.9rem;margin-bottom:22px}
.buttons{display:flex;flex-wrap:wrap;gap:10px}
.btn{display:inline-flex;align-items:center;gap:7px;padding:8px 16px;border-radius:999px;
     background:var(--fg);color:var(--bg);font-size:.88rem;font-weight:500}
.btn:hover{opacity:.85;text-decoration:none}
.btn.ghost{background:transparent;color:var(--fg);border:1px solid var(--line)}
.btn.dim{opacity:.45;pointer-events:none}

/* ---------- generic sections ---------- */
section{padding:34px 0}
section+section{border-top:1px solid var(--line)}
h2,h3,h4{line-height:1.3;font-weight:650;letter-spacing:-.01em}
h2{font-size:1.4rem;margin:6px 0 14px}
h3{font-size:1.12rem;margin:30px 0 10px}
h4{font-size:1rem;margin:22px 0 8px}
h2 .num,h3 .num,h4 .num{color:var(--muted);font-weight:500;margin-right:.6em;font-variant-numeric:tabular-nums}
p{margin:0 0 14px}
.lead{font-size:1.02rem}
strong.bp{font-weight:650}
.sc{font-variant:small-caps}
.note{color:#b04a4a}

.teaser{margin:26px 0 0}
.teaser img{width:100%;height:auto;border-radius:10px;border:1px solid var(--line);background:#fff}
.teaser figcaption{color:var(--muted);font-size:.85rem;margin-top:10px}

/* ---------- toc ---------- */
ul.toc{list-style:none;margin:0;padding:0;columns:2;column-gap:34px}
@media (max-width:640px){ul.toc{columns:1}}
ul.toc li{break-inside:avoid;margin:0 0 5px;font-size:.92rem}
ul.toc li.d0{margin-top:10px;font-weight:600}
ul.toc li.d1{padding-left:16px}
ul.toc li.d2{padding-left:32px;font-size:.88rem}
ul.toc .num{color:var(--muted);display:inline-block;min-width:3.1em;font-variant-numeric:tabular-nums}
ul.toc a{color:var(--fg)}

/* ---------- floats ---------- */
figure{margin:26px 0}
figure .caption,figcaption{color:var(--muted);font-size:.86rem;line-height:1.55;margin-top:10px}
figure.tbl .caption{margin:0 0 10px}
figure img{max-width:100%;height:auto;display:block;border-radius:6px}
figure img.single{width:100%;border:1px solid var(--line);background:#fff;padding:6px}
.figgrid{display:grid;gap:8px}
.figgrid.cols3{grid-template-columns:repeat(3,1fr)}
.figgrid.cols2{grid-template-columns:repeat(2,1fr)}
@media (max-width:600px){.figgrid.cols3,.figgrid.cols2{grid-template-columns:1fr 1fr}}
.subfig img{width:100%;border:1px solid var(--line)}
.subcap{color:var(--muted);font-size:.78rem;text-align:center;margin-top:4px}
.missing{padding:10px;border:1px dashed var(--line);color:var(--muted);font-size:.85rem}

/* ---------- tables ---------- */
.tablewrap{overflow-x:auto;-webkit-overflow-scrolling:touch;border:1px solid var(--line);
           border-radius:8px}
table{border-collapse:collapse;width:100%;font-size:.87rem;font-variant-numeric:tabular-nums}
th,td{padding:7px 12px;border-bottom:1px solid var(--line);white-space:nowrap}
thead th{background:var(--soft);font-weight:650;border-bottom:2px solid var(--line)}
tbody tr:last-child td{border-bottom:none}
td.left,th.left{text-align:left}
td.center,th.center{text-align:center}
td.right,th.right{text-align:right}
td.best{background:var(--best);font-weight:650}
td.second{background:var(--second)}
td.hl{background:var(--accent-soft)}
.gain{background:var(--gain);border-radius:4px;padding:0 4px;font-size:.8em}
.drop{background:var(--drop);border-radius:4px;padding:0 4px;font-size:.8em}
.yes{color:#2a8a4a;font-weight:700}
.no{color:#c05252;font-weight:700}

/* ---------- equations / algorithms ---------- */
.eqn{overflow-x:auto;overflow-y:hidden;margin:16px 0;padding:2px 0}
figure.algo{border:1px solid var(--line);border-radius:8px;padding:14px 16px;background:var(--soft)}
figure.algo .caption{margin:0 0 10px;color:var(--fg);font-size:.9rem;
                     border-bottom:1px solid var(--line);padding-bottom:8px}
.algobody{font-size:.85rem;overflow-x:auto}
.algline{padding-top:2px;white-space:nowrap}
.algline .ln{display:inline-block;width:2.1em;color:var(--muted);
             font-variant-numeric:tabular-nums;font-size:.8em}
.cmt{color:var(--muted)}

/* ---------- refs / cites ---------- */
.cite a{font-size:.86em}
.mainref{font-weight:600}
ol.refs{list-style:none;margin:0;padding:0;font-size:.85rem;color:var(--muted)}
ol.refs li{margin:0 0 7px;padding-left:2.6em;text-indent:-2.6em;line-height:1.5}
ol.refs .rn{display:inline-block;width:2.4em;text-indent:0;color:var(--fg)}
ol.refs li:target{background:var(--accent-soft);border-radius:4px}

pre.bibtex{background:var(--soft);border:1px solid var(--line);border-radius:8px;padding:14px;
           overflow-x:auto;font-size:.82rem;line-height:1.5}
footer{padding:34px 0 60px;color:var(--muted);font-size:.82rem;border-top:1px solid var(--line)}
mjx-container[display="true"]{overflow-x:auto;overflow-y:hidden}
"""

MATHJAX = """
window.MathJax = {
  loader: { load: ['[tex]/tagformat'] },
  tex: {
    packages: { '[+]': ['tagformat'] },
    inlineMath: [['$','$'],['\\\\(','\\\\)']],
    displayMath: [['$$','$$'],['\\\\[','\\\\]']],
    processEnvironments: true,
    tags: 'ams',
    tagformat: { number: (n) => 'S' + n },
    macros: Object.assign(%s, {num:['{#1}',1], si:['{#1}',1], SI:['{#1}\\\\,{#2}',2]})
  },
  options: { skipHtmlTags: ['script','noscript','style','textarea','pre','code'] },
  svg: { fontCache: 'global' }
};
""" % json.dumps(macros)

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="Project page for Greg: Guided Reinforcement Fine-Tuning for Sensorimotor Driving.">
<meta property="og:title" content="{title}">
<meta property="og:description" content="Project page: implementation details, ablations, and qualitative results.">
<meta property="og:image" content="static/images/figures_Greg.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>&#128663;</text></svg>">
<style>{css}</style>
<script>{mathjax}</script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
</head>
<body>

<header class="hero">
  <div class="wrap">
    <div class="kicker">Project Page</div>
    <h1 class="title">{title}</h1>
    <div class="authors">Anonymous Authors</div>
    <div class="venue">Under review</div>
    <div class="buttons">
      <!-- paper link pending -->
      <a class="btn ghost dim" href="#">&#128196; Paper (coming soon)</a>
      <a class="btn" href="static/code/greg_code.zip">&#128187; Code (ZIP)</a>
      <a class="btn ghost" href="#video">&#127909; Video</a>
    </div>
    <figure class="teaser">
      <img src="static/images/figures_Greg.png" alt="Overview of the Greg framework">
      <figcaption><b>Greg</b> fine-tunes a sensorimotor driving policy in closed loop with
      imitation, constraint, and exploration guidance.</figcaption>
    </figure>
  </div>
</header>

<section id="abstract">
  <div class="wrap">
    <h2>Abstract</h2>
    <p class="lead">Reinforcement learning (RL) can improve sensorimotor driving policies, but closed-loop
training in a photorealistic simulator has remained impractical: rollouts are expensive and
small-batch off-policy optimization is unstable. We introduce <b>Greg</b>, a reinforcement
fine-tuning framework that stabilizes it. Greg formulates driving as a constrained Markov
decision process with a logically structured reward and augmented Lagrangian constraint
handling, trains distributional critic ensembles whose disagreement prioritizes a stratified
replay buffer, and expands both the reward and the cost value target through a recurrent latent
model that takes no RL gradient. Fine-tuning an imitation-learned policy with Greg reaches a 92.0
driving score (DS) on Bench2Drive, level with the strongest published camera-only policy, at
27FPS and within 480 GPU hours on two RTX 3090 GPUs, from camera images to steering and
acceleration with no high-definition map and no PID controller in between. The advantage widens
on adversarial scenarios that expert demonstrations never contain: 54.2 DS against 27.9 for the
strongest imitation baseline, with no collisions. Those situations have to be handled by
reacting, and demonstrations of clean driving contain no examples of that.</p>
  </div>
</section>

<section id="video">
  <div class="wrap">
    <h2>Video</h2>
    <p>Closed-loop rollouts of the fine-tuned policy.</p>
    <video controls playsinline preload="metadata" style="width:100%;border-radius:8px"
           poster="static/images/figures_Greg.png">
      <source src="static/videos/supplementary.mp4" type="video/mp4">
      Your browser does not support the video tag.
      <a href="static/videos/supplementary.mp4">Download the video</a> instead.
    </video>
    <p style="color:var(--muted);font-size:.9rem">
      <a href="static/videos/supplementary.mp4" download>Download the video</a> (MP4, 30&nbsp;MB).</p>
  </div>
</section>

<section id="code">
  <div class="wrap">
    <h2>Code</h2>
    <p>The full training and evaluation code is available as a single archive: imitation
    pre-training, the distributed reinforcement fine-tuning trainer and workers, and the
    Bench2Drive, HUGSIM, BlackOut and Agility evaluation harnesses. No path, host, or account is hard-coded: every machine-specific value is read from the
    environment, so a fresh checkout runs unmodified. Copy the <code>.env.example</code> files
    and fill them in; see the per-directory <code>README.md</code> files for setup.</p>
    <p><a class="btn" href="static/code/greg_code.zip">&#128187; Download code (ZIP, {zipmb}&nbsp;MB)</a></p>
  </div>
</section>

<section id="contents">
  <div class="wrap">
    <h2>Contents</h2>
    {toc}
  </div>
</section>

<section id="content">
  <div class="wrap">
{body}
  </div>
</section>

<section id="references">
  <div class="wrap">
    <h2>References</h2>
    {refs}
  </div>
</section>

<section id="bibtex">
  <div class="wrap">
    <h2>BibTeX</h2>
    <pre class="bibtex">{bibtex}</pre>
  </div>
</section>

<footer>
  <div class="wrap">
    Numbers prefixed with S refer to this page; plain numbers refer to the main paper.
  </div>
</footer>

</body>
</html>
"""

def main():
    os.makedirs(SITE, exist_ok=True)
    zip_path = os.path.join(SITE, 'static', 'code', 'greg_code.zip')
    zipmb = '%.1f' % (os.path.getsize(zip_path) / 1e6) if os.path.exists(zip_path) else '?'
    html = HTML.format(title=TITLE, css=CSS, mathjax=MATHJAX,
                       toc=toc, body=body, refs=refs, bibtex=BIBTEX,
                       zipmb=zipmb)
    open(os.path.join(SITE, 'index.html'), 'w').write(html)
    open(os.path.join(SITE, '.nojekyll'), 'w').write('')
    os.makedirs(os.path.join(SITE, 'static', 'videos'), exist_ok=True)
    open(os.path.join(SITE, 'static', 'videos', '.gitkeep'), 'w').write('')
    print('wrote', os.path.join(SITE, 'index.html'),
          os.path.getsize(os.path.join(SITE, 'index.html')), 'bytes')

if __name__ == '__main__':
    main()
