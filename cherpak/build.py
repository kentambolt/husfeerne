# -*- coding: utf-8 -*-
"""Bygger Husfeernes interne arkiv paa /cherpak/.

Kilder:   cherpak/_src/<sprog>/<dokument>.md   (udgives ikke – rammes af *.md-filteret i workflowet)
Output:   cherpak/<sprog>/<dokument>.html  +  cherpak/index.html

Koer:     python cherpak/build.py
Ret altid i kilderne, aldrig i de genererede .html-filer.
"""
import io, os, re, html, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(ROOT, '_src')
LANGS = ['da', 'en', 'ru']
DOCS  = ['plan', 'analyse', 'priser']

UI = {
  'da': dict(
    kode='DA', navn='Dansk', arkiv='Arkiv', arkiv_lang='Ejer- og medarbejderarkiv',
    landing_h='Vores fælles arkiv', landing_p='Planer, tal og beslutninger for Husfeerne – samlet ét sted, på tre sprog. Vi er tre, der driver og planlægger firmaet sammen, og her ligger det, vi bliver enige om.',
    opdateret='Opdateret', til_site='Til husfeerne.dk', andre_sprog='Samme dokument på',
    titler={'plan': 'Kom-i-gang-plan', 'analyse': 'Konkurrentanalyse', 'priser': 'Sådan regner vi prisen ud'},
    blurbs={'plan': 'Fase for fase: hvad der skal på plads, før og efter vi går i luften.',
            'analyse': 'Hvad konkurrenterne i Aalborg tager, hvad de sælger på – og hvor vi står.',
            'priser': 'Hele regnestykket bag 325 kr. i timen, så alle tre kan forklare det.'}),
  'en': dict(
    kode='EN', navn='English', arkiv='Archive', arkiv_lang='Owner & team archive',
    landing_h='Our shared archive', landing_p='Plans, numbers and decisions for Husfeerne – in one place, in three languages. The three of us run and plan the company together, and this is where what we agree on lives.',
    opdateret='Updated', til_site='Go to husfeerne.dk', andre_sprog='Same document in',
    titler={'plan': 'Getting-started plan', 'analyse': 'Competitor analysis', 'priser': 'How we work out our price'},
    blurbs={'plan': 'Phase by phase: what needs to be in place before and after launch.',
            'analyse': 'What competitors in Aalborg charge, what they sell on – and where we stand.',
            'priser': 'The full calculation behind DKK 325 an hour, so all three of us can explain it.'}),
  'ru': dict(
    kode='RU', navn='Русский', arkiv='Архив', arkiv_lang='Архив владельцев и команды',
    landing_h='Наш общий архив', landing_p='Планы, цифры и решения Husfeerne — в одном месте, на трёх языках. Мы втроём ведём и планируем компанию вместе, и здесь лежит то, о чём мы договорились.',
    opdateret='Обновлено', til_site='На husfeerne.dk', andre_sprog='Тот же документ на',
    titler={'plan': 'План запуска', 'analyse': 'Анализ конкурентов', 'priser': 'Как мы считаем цену'},
    blurbs={'plan': 'Шаг за шагом: что должно быть готово до запуска и после.',
            'analyse': 'Что берут конкуренты в Ольборге, на чём они продают — и где мы.',
            'priser': 'Полный расчёт за 325 кронами в час — чтобы каждый из нас троих мог его объяснить.'}),
}

MAANEDER = {
  'da': ['januar','februar','marts','april','maj','juni','juli','august','september','oktober','november','december'],
  'en': ['January','February','March','April','May','June','July','August','September','October','November','December'],
  'ru': ['января','февраля','марта','апреля','мая','июня','июля','августа','сентября','октября','ноября','декабря'],
}
def dato(lang, d=None):
    d = d or datetime.date.today()
    m = MAANEDER[lang][d.month - 1]
    return {'da': '%d. %s %d', 'en': '%d %s %d', 'ru': '%d %s %d'}[lang] % (d.day, m, d.year)

FAVICON = ('<link rel="icon" type="image/svg+xml" href=\'data:image/svg+xml,'
  '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="15" fill="%23113E29"/>'
  '<path d="M33 55 C33 36 39 22 52 13 C52 34 45 48 33 55 Z" fill="%23E9C8C1"/>'
  '<path d="M31 55 C31 40 25 29 13 22 C13 40 19 50 31 55 Z" fill="%23FAF7F1"/>'
  '<path d="M32 57 L32 40" stroke="%23FAF7F1" stroke-width="2.4" stroke-linecap="round"/></svg>\'>')
FONTE = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
  '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
  '<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,600'
  '&family=Lato:wght@400;700&display=swap" rel="stylesheet">')

# ------------------------------------------------------------------ markdown
def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])', r'<em>\1</em>', t)
    t = re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', r'<a href="\2">\1</a>', t)
    return t

def slug(t):
    t = re.sub(r'<[^>]+>', '', t).lower()
    t = re.sub(r'[^\w\s-]', '', t, flags=re.U)
    return re.sub(r'[\s_]+', '-', t).strip('-')[:60]

BULLET = re.compile(r'^(\s*)([-*]|\d+\.)\s+(.*)$')

def parse_list(lines, i, indent):
    """Parser en liste paa niveau `indent`. Returnerer (html, naeste_index)."""
    m0 = BULLET.match(lines[i])
    ordered = m0.group(2)[0].isdigit()
    items, out = [], []
    while i < len(lines):
        m = BULLET.match(lines[i])
        if m and len(m.group(1)) == indent:
            items.append([m.group(3)]); i += 1; continue
        if m and len(m.group(1)) > indent and items:
            sub, i = parse_list(lines, i, len(m.group(1)))
            items[-1].append(sub); continue
        if lines[i].strip() and lines[i].startswith(' ' * (indent + 1)) and items and not m:
            items[-1].append(lines[i].strip()); i += 1; continue
        break
    for parts in items:
        text = parts[0]; cls = ''
        tm = re.match(r'^\[( |x|X)\]\s+(.*)$', text)
        if tm:
            done = tm.group(1).lower() == 'x'
            cls = ' class="task%s"' % (' done' if done else '')
            text = ('<span class="box" aria-hidden="true">%s</span>' % ('☑' if done else '☐')) + inline(tm.group(2))
        else:
            text = inline(text)
        rest = []
        for p in parts[1:]:
            if p.startswith('<ul') or p.startswith('<ol'): rest.append(p)
            else: text += ' ' + inline(p)
        out.append('<li%s>%s%s</li>' % (cls, text, ''.join(rest)))
    tag = 'ol' if ordered else 'ul'
    return '<%s>%s</%s>' % (tag, ''.join(out), tag), i

def md_to_html(md):
    lines = md.replace('\r\n', '\n').split('\n')
    out, i, n = [], 0, len(lines)
    while i < n:
        line = lines[i]
        if not line.strip():
            i += 1; continue
        if re.match(r'^-{3,}\s*$', line):
            out.append('<hr>'); i += 1; continue
        hm = re.match(r'^(#{1,4})\s+(.*)$', line)
        if hm:
            lvl = len(hm.group(1)); txt = inline(hm.group(2))
            out.append('<h%d id="%s">%s</h%d>' % (lvl, slug(txt), txt, lvl)); i += 1; continue
        if line.lstrip().startswith('|'):
            rows = []
            while i < n and lines[i].lstrip().startswith('|'):
                rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')]); i += 1
            head, body = rows[0], [r for r in rows[2:]] if len(rows) > 2 and set(''.join(rows[1])) <= set('-:| ') else rows[1:]
            th = ''.join('<th>%s</th>' % inline(c) for c in head)
            trs = ''.join('<tr>%s</tr>' % ''.join('<td>%s</td>' % inline(c) for c in r) for r in body)
            out.append('<div class="tbl"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % (th, trs)); continue
        if line.startswith('>'):
            buf = []
            while i < n and lines[i].startswith('>'):
                buf.append(lines[i][1:].strip()); i += 1
            paras = ' '.join(buf).split('  ')
            out.append('<blockquote>%s</blockquote>' % ''.join('<p>%s</p>' % inline(p) for p in ' '.join(buf).split('\n\n')))
            continue
        if BULLET.match(line):
            h, i = parse_list(lines, i, len(BULLET.match(line).group(1)))
            out.append(h); continue
        buf = []
        while i < n and lines[i].strip() and not BULLET.match(lines[i]) and not lines[i].startswith(('#', '>', '|', '---')):
            buf.append(lines[i].strip()); i += 1
        out.append('<p>%s</p>' % inline(' '.join(buf)))
    return '\n'.join(out)

# ------------------------------------------------------------------ sider
def side_skelet(lang, title, body, rel_root, nav_docs, nav_langs, klasse='doc'):
    ui = UI[lang]
    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title) if klasse=='landing' else html.escape(title) + ' · ' + ui['arkiv']} | Husfeerne</title>
<!-- Internt arkiv. Ikke hemmeligt, men skal ikke konkurrere med salgssiderne i Google. -->
<meta name="robots" content="noindex, nofollow">
{FAVICON}
<meta name="theme-color" content="#113E29">
{FONTE}
<link rel="stylesheet" href="{rel_root}cherpak/cherpak.css">
</head>
<body>
<header class="bar">
  <div class="wrap">
    <a class="brand" href="{rel_root}cherpak/index.html"><img src="{rel_root}husfeerne-logo.png" alt="Husfeerne" width="440" height="196"><span>{ui['arkiv']}</span></a>
    <nav class="docs" aria-label="Dokumenter">{nav_docs}</nav>
    <nav class="langs" aria-label="Sprog">{nav_langs}</nav>
  </div>
</header>
<main class="wrap {klasse}">
{body}
</main>
<footer class="wrap foot">
  <span>Husfeerne · {ui['arkiv_lang']} · {ui['opdateret']} {dato(lang)}</span>
  <a href="{rel_root}index.html">{ui['til_site']} →</a>
</footer>
<!-- Genereret af cherpak/build.py fra cherpak/_src/ – ret i kilden, ikke her. -->
</body>
</html>
'''

def byg_dokument(lang, doc):
    ui = UI[lang]
    md = io.open(os.path.join(SRC, lang, doc + '.md'), encoding='utf-8').read()
    body = md_to_html(md)
    nav_docs = ''.join('<a href="%s.html"%s>%s</a>' % (d, ' class="on"' if d == doc else '', ui['titler'][d]) for d in DOCS)
    nav_langs = ''.join('<a href="../%s/%s.html" hreflang="%s"%s>%s</a>' % (l, doc, l, ' class="on"' if l == lang else '', UI[l]['kode']) for l in LANGS)
    out = side_skelet(lang, ui['titler'][doc], body, '../../', nav_docs, nav_langs)
    os.makedirs(os.path.join(ROOT, lang), exist_ok=True)
    io.open(os.path.join(ROOT, lang, doc + '.html'), 'w', encoding='utf-8').write(out)

def byg_landing():
    kolonner = []
    for l in LANGS:
        ui = UI[l]
        kort = ''.join(
            '<a class="card" href="%s/%s.html" lang="%s"><h3>%s</h3><p>%s</p></a>' % (l, d, l, ui['titler'][d], ui['blurbs'][d])
            for d in DOCS)
        kolonner.append('<section class="col" lang="%s"><h2><span class="kode">%s</span>%s</h2><p class="lead">%s</p>%s</section>'
                        % (l, ui['kode'], ui['navn'], ui['landing_p'], kort))
    body = '<h1>%s <span class="sep">·</span> %s <span class="sep">·</span> %s</h1>\n<div class="cols">%s</div>' % (
        UI['da']['landing_h'], UI['en']['landing_h'], UI['ru']['landing_h'], ''.join(kolonner))
    nav_langs = ''.join('<a href="%s/plan.html" hreflang="%s">%s</a>' % (l, l, UI[l]['kode']) for l in LANGS)
    out = side_skelet('da', 'Arkiv · Archive · Архив', body, '../', '', nav_langs, klasse='landing')
    io.open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8').write(out)

if __name__ == '__main__':
    antal = 0
    for lang in LANGS:
        for doc in DOCS:
            p = os.path.join(SRC, lang, doc + '.md')
            if not os.path.exists(p):
                print('  MANGLER  %s/%s.md' % (lang, doc)); continue
            byg_dokument(lang, doc); antal += 1
            print('  ok       cherpak/%s/%s.html' % (lang, doc))
    byg_landing(); print('  ok       cherpak/index.html')
    print('\n%d dokumentsider + landing bygget.' % antal)
