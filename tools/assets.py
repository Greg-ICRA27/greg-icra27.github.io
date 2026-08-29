#!/usr/bin/env python3
"""Collect and web-optimize every figure referenced by supplementary.tex."""
import re, os, json, subprocess, shutil

PAPER = os.environ.get('GREG_PAPER_DIR', '../GREG_paper')
OUT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(OUT, 'site')
IMGDIR = os.path.join(SITE, 'static', 'images')
os.makedirs(IMGDIR, exist_ok=True)

EXTRA = ['figures/Greg.pdf', 'figures/Overview.pdf', 'figures/model.pdf']

def resolve(p):
    cands = [p, p + '.pdf', p + '.png', p + '.jpg', p + '.jpeg']
    for c in cands:
        f = os.path.join(PAPER, c)
        if os.path.exists(f):
            return f
    return None

def convert(src, stem):
    ext = os.path.splitext(src)[1].lower()
    dst = os.path.join(IMGDIR, stem + '.jpg')
    if ext == '.pdf':
        dst = os.path.join(IMGDIR, stem + '.png')
        subprocess.run(['pdftoppm', '-png', '-r', '160', '-singlefile', src,
                        os.path.join(IMGDIR, stem)], check=True)
        subprocess.run(['convert', dst, '-resize', '1600x1600>', '-strip', dst], check=True)
    else:
        subprocess.run(['convert', src, '-resize', '1400x1400>', '-quality', '86',
                        '-strip', dst], check=True)
    return 'static/images/' + os.path.basename(dst)

def main():
    tex = open(os.path.join(PAPER, 'sections/supplementary.tex')).read()
    tex = '\n'.join(re.sub(r'(?<!\\)%.*', '', l) for l in tex.split('\n'))
    tex = re.sub(r'\\begin\{comment\}.*?\\end\{comment\}', '', tex, flags=re.S)
    paths = re.findall(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]*)\}', tex)
    mapping, missing = {}, []
    for p in dict.fromkeys(paths + EXTRA):
        src = resolve(p)
        if not src:
            missing.append(p); continue
        stem = re.sub(r'[^A-Za-z0-9]+', '_', os.path.splitext(p)[0]).strip('_')
        try:
            mapping[p] = convert(src, stem)
        except subprocess.CalledProcessError as e:
            missing.append(p)
    json.dump(mapping, open(os.path.join(OUT, 'assets.json'), 'w'), indent=1)
    print('converted', len(mapping), 'missing', missing)

if __name__ == '__main__':
    main()
