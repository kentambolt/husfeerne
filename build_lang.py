# -*- coding: utf-8 -*-
"""Husfeerne – bygger de engelske, tyske og ukrainske udgaver af sitet.

    python build_lang.py harvest   -> i18n/todo/<side>.json  (tekster uden oversættelse)
    python build_lang.py build     -> /en/, /de/, /uk/, hreflang i de danske sider, sitemap.xml

De danske sider er kilden. Oversættelserne ligger i i18n/tr/*.json som
{ "dansk tekst": {"en": "...", "de": "...", "uk": "..."} }. Inline-tags i teksten
(<a>, <span>, <b>, <small>, <br>) skrives uden attributter i nøglerne og sættes
tilbage med de oprindelige attributter, når siden bygges. Nøgler og oversættelser
er almindelig tekst (uden HTML-entities): & skrives som &, ikke &amp;.
Kør fra repoets rod. *.py og i18n/ udgives ikke (se .github/workflows/main.yml).
"""
import io, os, re, sys, json, glob, html

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)
SITE = 'https://husfeerne.dk'
LANGS = ['en', 'de', 'uk']
LANG_META = {
    'da': {'name': 'Dansk', 'locale': 'da_DK'},
    'en': {'name': 'English', 'locale': 'en_GB'},
    'de': {'name': 'Deutsch', 'locale': 'de_DE'},
    'uk': {'name': 'Українська', 'locale': 'uk_UA'},
}
# Danske sider -> URL-sti pr. sprog (slug med søgeord på det pågældende sprog)
PAGES = {
    'index.html': {'da': '/', 'en': '/en/', 'de': '/de/', 'uk': '/uk/'},
    'privat-rengoering-aalborg.html': {'en': '/en/home-cleaning-aalborg.html', 'de': '/de/privatreinigung-aalborg.html', 'uk': '/uk/prybyrannia-domu-aalborg.html'},
    'erhvervsrengoering-aalborg.html': {'en': '/en/office-cleaning-aalborg.html', 'de': '/de/bueroreinigung-aalborg.html', 'uk': '/uk/prybyrannia-ofisiv-aalborg.html'},
    'flytterengoering-aalborg.html': {'en': '/en/move-out-cleaning-aalborg.html', 'de': '/de/umzugsreinigung-aalborg.html', 'uk': '/uk/prybyrannia-pry-vyizdi-aalborg.html'},
    'hovedrengoering-aalborg.html': {'en': '/en/deep-cleaning-aalborg.html', 'de': '/de/grundreinigung-aalborg.html', 'uk': '/uk/heneralne-prybyrannia-aalborg.html'},
    'vinduespudsning-aalborg.html': {'en': '/en/window-cleaning-aalborg.html', 'de': '/de/fensterreinigung-aalborg.html', 'uk': '/uk/myttia-vikon-aalborg.html'},
    'trappevask-aalborg.html': {'en': '/en/stairwell-cleaning-aalborg.html', 'de': '/de/treppenhausreinigung-aalborg.html', 'uk': '/uk/prybyrannia-pidizdiv-aalborg.html'},
}
for _p, _m in PAGES.items():
    _m.setdefault('da', '/' + _p)
LASTMOD = '2026-09-08'

INLINE = {'a', 'span', 'b', 'strong', 'em', 'i', 'small', 'br', 'sup', 'sub', 'u', 'abbr', 'time'}
VOID = {'meta', 'link', 'img', 'input', 'br', 'hr', 'source', 'path', 'rect', 'circle', 'use'}
TEXT_ATTRS = {'alt', 'aria-label', 'placeholder', 'title'}
META_TRANSLATE = {'description', 'og:title', 'og:description', 'og:image:alt', 'twitter:title', 'twitter:description'}
DATA_ATTRS = ('data-en', 'data-de', 'data-uk', 'data-da', 'data-enph', 'data-deph', 'data-ukph', 'data-daph')
# Tekster, der er ens på alle sprog (bynavne, adresse, navne)
NO_TRANSLATE = {'Husfeerne', 'Dansk', 'English', 'Deutsch', 'Українська', 'Dansk · English · Deutsch · Українська',
                'Akvavitvej 7, 15. 3, 9000 Aalborg', 'CVR: NNNNNNNN', 'Vælg sprog / Choose language', 'Airbnb',
                'Menu', 'Husfeerne Rengøring', '© 2026 Husfeerne',
                'Aalborg', '★ Aalborg', 'Nørresundby', 'Hjørring', 'Frederikshavn', 'Skagen', 'Brønderslev', 'Hobro',
                'Thisted', 'Aabybro', 'Hadsund', 'Støvring', 'Sæby', 'Nibe', 'Hals', 'Løkken', 'Hasseris', 'Gug',
                'Vejgaard', 'Skalborg', 'Svenstrup', 'Klarup', 'Vodskov', 'Vadum', 'Frejlev', 'Kærby', 'Vestbyen'}
SKIP_RE = re.compile(r'^[\w.+-]+@[\w-]+\.[\w.]+$|^[+\d][\d ]+$')
# JSON-LD: nøgler der oversættes, og @type hvor "name" oversættes
LD_KEYS = {'description', 'text', 'slogan'}
LD_NAME_TYPES = {'Question', 'Service', 'Offer', 'OfferCatalog', 'ListItem', 'ItemList', 'WebPage', 'ImageObject'}

TOKEN_RE = re.compile(r'<!--.*?-->|<script\b[^>]*>.*?</script>|<style\b[^>]*>.*?</style>|<[^>]+>|[^<]+', re.S)
TAG_RE = re.compile(r'<(/?)([a-zA-Z][a-zA-Z0-9-]*)((?:\s+[^\s=>/]+(?:\s*=\s*(?:"[^"]*"|\'[^\']*\'|[^\s>]+))?)*)\s*(/?)>', re.S)
ATTR_RE = re.compile(r'([^\s=>/]+)(?:\s*=\s*("[^"]*"|\'[^\']*\'|[^\s>]+))?', re.S)
LETTERS = re.compile(r'[A-Za-zÆØÅæøåÄÖÜäöüßЀ-ӿ]')


def norm(s):
    return re.sub(r'\s+', ' ', s).strip()


def esc_text(s):
    """Oversat tekst -> HTML-tekst (kun & skal escapes; tags skrives af os selv)."""
    return re.sub(r'&(?!#?\w+;)', '&amp;', s)


def esc_attr(s):
    return esc_text(s).replace('"', '&quot;')


def parse_tag(tok):
    m = TAG_RE.match(tok)
    if not m:
        return None
    return {'close': m.group(1) == '/', 'name': m.group(2).lower(), 'attrs': m.group(3), 'self': m.group(4) == '/', 'raw': tok}


def attrs_list(attrs):
    out = []
    for m in ATTR_RE.finditer(attrs):
        k, v = m.group(1), m.group(2)
        if v is not None and v[:1] in '"\'':
            v = v[1:-1]
        out.append([k, v])
    return out


def build_tag(name, attrs, self_close=False):
    parts = [name]
    for k, v in attrs:
        parts.append(k if v is None else '%s="%s"' % (k, v))
    return '<' + ' '.join(parts) + ('/>' if self_close else '>')


def tokens_of(s):
    return TOKEN_RE.findall(s)


def is_tag(t):
    return t.startswith('<') and not t.startswith('<!--')


# ------------------------------------------------------------------ enheder
def key_of(inner_tokens):
    """Nøgle for en tekstenhed: inline-tags uden attributter, entities opløst, whitespace normaliseret."""
    parts = []
    for t in inner_tokens:
        if is_tag(t):
            tg = parse_tag(t)
            parts.append('</%s>' % tg['name'] if tg['close'] else '<%s>' % tg['name'])
        else:
            parts.append(html.unescape(t))
    return norm(''.join(parts))


def trim(toks, start):
    """Fjern whitespace, uparrede tags og ét omsluttende inline-element ad gangen.
    Returnerer (start, end) på det indre stykke i den globale tokenliste."""
    end = start + len(toks)
    while True:
        changed = False
        while start < end and not is_tag(toks[0]) and not toks[0].strip():
            toks = toks[1:]; start += 1; changed = True
        while start < end and not is_tag(toks[-1]) and not toks[-1].strip():
            toks = toks[:-1]; end -= 1; changed = True
        if start >= end:
            return start, end
        # omsluttende element
        if is_tag(toks[0]) and is_tag(toks[-1]) and len(toks) >= 2:
            a, b = parse_tag(toks[0]), parse_tag(toks[-1])
            if a and b and not a['close'] and b['close'] and a['name'] == b['name'] and not a['self'] and a['name'] != 'br':
                depth = 0; ok = True
                for t in toks[1:-1]:
                    if is_tag(t):
                        tg = parse_tag(t)
                        if tg['name'] == a['name'] and not tg['self']:
                            depth += -1 if tg['close'] else 1
                            if depth < 0:
                                ok = False; break
                if ok and depth == 0:
                    toks = toks[1:-1]; start += 1; end -= 1; changed = True
        if not changed:
            return start, end


def split_top_level(toks):
    """Deler en buffer i topniveau-stykker: [(offset, tokens)]. Står der almindelig tekst med
    bogstaver på topniveau, er hele bufferen én enhed."""
    items = []; depth = 0; cur_start = None
    for i, t in enumerate(toks):
        if is_tag(t):
            tg = parse_tag(t)
            if tg['name'] == 'br' or tg['self']:
                if depth == 0:
                    items.append((i, [t]))
                continue
            if not tg['close']:
                if depth == 0:
                    cur_start = i
                depth += 1
            else:
                depth -= 1
                if depth == 0:
                    items.append((cur_start, toks[cur_start:i + 1]))
        elif depth == 0:
            if LETTERS.search(html.unescape(t)):
                return [(0, toks)]
    return [it for it in items if any(not is_tag(x) for x in it[1])]


def scan(page_html):
    """Gennemløber siden og finder tekstenheder: {'start','end','key'} (token-indeks på det indre stykke)."""
    toks = tokens_of(page_html)
    units = []
    block_stack = []      # åbne blok-elementer (for at udelukke svg/script m.m.)
    buf_start = None
    inline_stack = []     # åbne inline-tags i den aktuelle buffer

    def add_unit(start, end):
        if start >= end:
            return
        key = key_of(toks[start:end])
        if key and LETTERS.search(key) and key not in NO_TRANSLATE and not SKIP_RE.match(key):
            units.append({'start': start, 'end': end, 'key': key})

    def flush(end):
        nonlocal buf_start, inline_stack
        if buf_start is None:
            return
        excluded = any(n in ('svg', 'script', 'style', 'textarea') for n in block_stack)
        buf = toks[buf_start:end]
        # uparrede åbne inline-tags i slutningen hører ikke med
        while buf and is_tag(buf[-1]) and not parse_tag(buf[-1])['close'] and parse_tag(buf[-1])['name'] != 'br':
            buf = buf[:-1]
        if not excluded:
            s0, e0 = trim(buf, buf_start)
            for off, sub in split_top_level(toks[s0:e0]):
                s1, e1 = trim(sub, s0 + off)
                # et stykke kan igen bestå af flere topniveau-elementer (fx <a><b>..</b><span>..</span></a>)
                add_unit(s1, e1)
        buf_start = None; inline_stack = []

    for i, t in enumerate(toks):
        if t.startswith('<!--') or t.startswith('<script') or t.startswith('<style'):
            flush(i); continue
        if t.startswith('<'):
            tg = parse_tag(t)
            if tg is None or tg['name'] == '!doctype':
                flush(i); continue
            if tg['name'] in INLINE:
                if tg['name'] == 'br' or tg['self']:
                    if buf_start is None:
                        buf_start = i
                    continue
                if tg['close']:
                    if inline_stack and inline_stack[-1] == tg['name']:
                        inline_stack.pop()
                    else:
                        flush(i)          # lukker et element, der blev åbnet før bufferen
                    continue
                if buf_start is None:
                    buf_start = i
                inline_stack.append(tg['name'])
                continue
            flush(i)
            if tg['close']:
                if tg['name'] in block_stack:
                    while block_stack and block_stack[-1] != tg['name']:
                        block_stack.pop()
                    block_stack.pop()
            elif not tg['self'] and tg['name'] not in VOID:
                block_stack.append(tg['name'])
        else:
            if buf_start is None:
                if not t.strip():
                    continue
                buf_start = i
    flush(len(toks))
    return toks, units


def attr_units(page_html):
    """Attributter, der skal oversættes: alt, aria-label, placeholder, meta-content, <title>."""
    keys = []
    for t in tokens_of(page_html):
        if not is_tag(t) or t.startswith('<script'):
            continue
        tg = parse_tag(t)
        if not tg or tg['close']:
            continue
        al = attrs_list(tg['attrs']); d = dict(al)
        if tg['name'] == 'meta':
            nm = d.get('name') or d.get('property')
            if nm in META_TRANSLATE and d.get('content'):
                keys.append(html.unescape(d['content']))
        for k, v in al:
            if k in TEXT_ATTRS and v:
                v = html.unescape(v)
                if LETTERS.search(v) and v not in NO_TRANSLATE:
                    keys.append(v)
    m = re.search(r'<title>(.*?)</title>', page_html, re.S)
    if m:
        keys.append(html.unescape(norm(m.group(1))))
    return keys


def walk_ld(node, fn):
    if isinstance(node, dict):
        typ = node.get('@type')
        for k, v in node.items():
            if isinstance(v, str):
                if k in LD_KEYS or (k == 'name' and typ in LD_NAME_TYPES):
                    if LETTERS.search(v) and v not in NO_TRANSLATE:
                        new = fn(v)
                        if new is not None:
                            node[k] = new
            else:
                walk_ld(v, fn)
    elif isinstance(node, list):
        for v in node:
            walk_ld(v, fn)


def ld_strings(page_html):
    keys = []
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', page_html, re.S):
        walk_ld(json.loads(m.group(1)), lambda s: keys.append(s))
    return keys


def strip_tags(s):
    return norm(re.sub(r'<[^>]+>', '', s))


def seeds_from(page_html):
    """Eksisterende oversættelser i data-en/de/uk og data-enph/deph/ukph."""
    seeds = {}
    toks = tokens_of(page_html)
    for i, t in enumerate(toks):
        if not is_tag(t) or t.startswith('<script'):
            continue
        tg = parse_tag(t)
        if not tg or tg['close']:
            continue
        d = dict(attrs_list(tg['attrs']))
        if 'data-en' in d and i + 2 < len(toks) and not is_tag(toks[i + 1]):
            key = html.unescape(norm(toks[i + 1]))
            if key:
                seeds[key] = {l: html.unescape(d.get('data-' + l, '')) for l in LANGS}
        if 'data-enph' in d and d.get('placeholder'):
            seeds[html.unescape(d['placeholder'])] = {l: html.unescape(d.get('data-%sph' % l, '')) for l in LANGS}
    return seeds


def load_translations():
    tr = {}
    for f in sorted(glob.glob('i18n/tr/*.json')):
        for k, v in json.load(io.open(f, encoding='utf-8')).items():
            if any(v.get(l) for l in LANGS):
                tr[k] = v
    return tr


class Lookup:
    """Oversættelse af en nøgle: direkte, via seeds eller via tag-løs udgave af en anden nøgle."""

    def __init__(self, tr, seeds):
        self.tr = dict(seeds); self.tr.update(tr)
        self.stripped = {}
        for k, v in self.tr.items():
            if '<' in k:
                self.stripped.setdefault(strip_tags(k), {l: strip_tags(v.get(l, '')) for l in LANGS})

    def get(self, key, lang):
        v = self.tr.get(key)
        if v and v.get(lang):
            return v[lang]
        v = self.stripped.get(key)
        if v and v.get(lang):
            return v[lang]
        return None

    def has(self, key):
        return all(self.get(key, l) for l in LANGS)


# ------------------------------------------------------------------ harvest
def harvest():
    seeds = {}
    for p in PAGES:
        seeds.update(seeds_from(io.open(p, encoding='utf-8').read()))
    io.open('i18n/seeds.json', 'w', encoding='utf-8').write(json.dumps(seeds, ensure_ascii=False, indent=1))
    look = Lookup(load_translations(), seeds)
    os.makedirs('i18n/todo', exist_ok=True); os.makedirs('i18n/tr', exist_ok=True)
    seen = set(); total = 0
    for p in PAGES:
        s = io.open(p, encoding='utf-8').read()
        toks, units = scan(s)
        keys = [u['key'] for u in units] + attr_units(s) + ld_strings(s)
        todo = {}
        for k in keys:
            if k in seen or k in NO_TRANSLATE or look.has(k):
                continue
            seen.add(k)
            todo[k] = {'en': '', 'de': '', 'uk': ''}
        name = 'index' if p == 'index.html' else p[:-5]
        out = 'i18n/todo/%s.json' % name
        if todo:
            io.open(out, 'w', encoding='utf-8').write(json.dumps(todo, ensure_ascii=False, indent=1))
        elif os.path.exists(out):
            os.remove(out)
        total += len(todo)
        print('  %-34s enheder %3d  attr %3d  ld %3d  -> mangler %3d' % (p, len(units), len(attr_units(s)), len(ld_strings(s)), len(todo)))
    print('Mangler i alt: %d tekster (i18n/todo/*.json). Seeds: %d' % (total, len(seeds)))


# ------------------------------------------------------------------ build
def lang_url(href, lang):
    """href/src fra en dansk side -> absolut sti i sproget."""
    if not href or href.startswith(('http://', 'https://', 'mailto:', 'tel:', 'data:', 'javascript:', '#')):
        return href
    path, _, frag = href.partition('#')
    rel = path if path.startswith('/') else '/' + path
    if rel == '/index.html':
        rel = '/'
    for p, m in PAGES.items():
        if rel == m['da']:
            rel = m[lang]; break
    return rel + ('#' + frag if frag else '')


def abs_site_url(u, lang):
    if u.startswith(SITE):
        path, _, frag = u[len(SITE):].partition('#')
        for p, m in PAGES.items():
            if path == m['da']:
                return SITE + m[lang] + ('#' + frag if frag else '')
    return u


def hreflang_block(page):
    m = PAGES[page]
    lines = ['<link rel="alternate" hreflang="%s" href="%s%s">' % (l, SITE, m[l]) for l in ('da', 'en', 'de', 'uk')]
    lines.append('<link rel="alternate" hreflang="x-default" href="%s%s">' % (SITE, m['da']))
    return '\n'.join(lines)


HREFLANG_RE = re.compile(r'(?:<link rel="alternate" hreflang="[^"]+" href="[^"]+">\n?)+')
KUNDANSK_RE = re.compile(r'\n<div class="sprognotits" id="kunDansk" hidden>.*?</div>\s*</div>\n', re.S)


def update_danish(page):
    """Idempotent: hreflang-links efter canonical, og sprognotitsen 'kun på dansk' fjernes."""
    s = io.open(page, encoding='utf-8').read()
    s2 = HREFLANG_RE.sub('', s)
    can = re.search(r'<link rel="canonical" href="[^"]+">\n', s2)
    s2 = s2[:can.end()] + hreflang_block(page) + '\n' + s2[can.end():]
    s2 = KUNDANSK_RE.sub('\n', s2)
    if s2 != s:
        io.open(page, 'w', encoding='utf-8').write(s2)


def translate_ld(ld_text, look, lang, log):
    data = json.loads(ld_text)

    def fn(s):
        t = look.get(s, lang)
        if not t:
            log.append('ld: %s' % s[:60]); return None
        return t
    walk_ld(data, fn)

    def urls(node):
        if isinstance(node, dict):
            for k, v in list(node.items()):
                if k in ('url', 'item', 'mainEntityOfPage', '@id') and isinstance(v, str):
                    node[k] = abs_site_url(v, lang) if k != '@id' or '#organization' not in v else v
                elif k == 'inLanguage':
                    node[k] = lang
                else:
                    urls(v)
        elif isinstance(node, list):
            for v in node:
                urls(v)
    urls(data)
    if data.get('@type') in ('FAQPage', 'Service', 'WebPage'):
        data['inLanguage'] = lang
    return json.dumps(data, ensure_ascii=False, indent=1)


def rewrite_tag(tok, look, lang, log):
    tg = parse_tag(tok)
    if not tg or tg['close']:
        return tok
    al = [[k, v] for k, v in attrs_list(tg['attrs']) if k not in DATA_ATTRS]
    d = dict(al)
    for kv in al:
        k, v = kv
        if v is None:
            continue
        if k in ('href', 'src'):
            kv[1] = lang_url(v, lang)
        elif k in ('srcset', 'imagesrcset'):
            kv[1] = ', '.join(' '.join([lang_url(part.split()[0], lang)] + part.split()[1:]) for part in v.split(','))
        elif k in TEXT_ATTRS:
            vv = html.unescape(v)
            if LETTERS.search(vv) and vv not in NO_TRANSLATE:
                t = look.get(vv, lang)
                if t:
                    kv[1] = esc_attr(t)
                else:
                    log.append('attr %s: %s' % (k, vv[:50]))
        elif k == 'content' and tg['name'] == 'meta':
            nm = d.get('name') or d.get('property')
            if nm in META_TRANSLATE:
                t = look.get(html.unescape(v), lang)
                if t:
                    kv[1] = esc_attr(t)
                else:
                    log.append('meta %s: %s' % (nm, v[:50]))
            elif nm == 'og:locale':
                kv[1] = LANG_META[lang]['locale']
            elif nm == 'og:url':
                kv[1] = abs_site_url(v, lang)
    if tg['name'] == 'link' and d.get('rel') == 'canonical':
        for kv in al:
            if kv[0] == 'href':
                kv[1] = abs_site_url(kv[1], lang)
    if tg['name'] == 'html':
        for kv in al:
            if kv[0] == 'lang':
                kv[1] = lang
    if tg['name'] == 'input' and d.get('id') in ('kontaktSprog', 'jobSprog'):
        for kv in al:
            if kv[0] == 'value':
                kv[1] = '%s (%s)' % (LANG_META[lang]['name'], lang)
    if tg['name'] == 'button' and d.get('role') == 'option' and d.get('data-lang'):
        for kv in al:
            if kv[0] == 'aria-selected':
                kv[1] = 'true' if d['data-lang'] == lang else 'false'
    return build_tag(tg['name'], al, tg['self'])


def restore_tags(translation, orig_tokens):
    """Sæt de oprindelige tags (med attributter) ind i oversættelsen i samme rækkefølge."""
    orig = [parse_tag(t) for t in orig_tokens if is_tag(t)]
    out = []; i = 0
    for t in tokens_of(translation):
        if is_tag(t):
            tg = parse_tag(t)
            if tg is None or i >= len(orig) or orig[i]['name'] != tg['name'] or orig[i]['close'] != tg['close']:
                raise ValueError('tags matcher ikke i oversættelsen: %s' % translation[:70])
            out.append(orig[i]['raw']); i += 1
        else:
            out.append(esc_text(t))
    if i != len(orig):
        raise ValueError('for få tags i oversættelsen: %s' % translation[:70])
    return ''.join(out)


def build_page(page, lang, look):
    s = io.open(page, encoding='utf-8').read()
    log = []
    toks, units = scan(s)
    unit_at = {u['start']: u for u in units}
    rw = lambda x: rewrite_tag(x, look, lang, log) if is_tag(x) else x
    out = []; i = 0
    while i < len(toks):
        t = toks[i]
        if i in unit_at:
            u = unit_at[i]
            inner = toks[u['start']:u['end']]
            trans = look.get(u['key'], lang)
            if trans:
                try:
                    trans = ''.join(rw(x) for x in tokens_of(restore_tags(trans, inner)))
                except ValueError as e:
                    log.append(str(e)); trans = None
            if trans is None:
                log.append('tekst: %s' % u['key'][:60])
                trans = ''.join(rw(x) for x in inner if not x.startswith('<!--'))
            out.append(trans); i = u['end']; continue
        if t.startswith('<!--'):
            i += 1; continue
        if t.startswith('<script type="application/ld+json">'):
            m = re.match(r'(<script type="application/ld\+json">)(.*)(</script>)$', t, re.S)
            out.append(m.group(1) + '\n' + translate_ld(m.group(2), look, lang, log) + '\n' + m.group(3))
            i += 1; continue
        if t.startswith('<script') or t.startswith('<style'):
            out.append(t.replace('src="app.js"', 'src="/app.js"')); i += 1; continue
        if is_tag(t):
            tg = parse_tag(t)
            if tg and tg['name'] == 'title' and not tg['close']:
                title = html.unescape(norm(toks[i + 1]))
                tt = look.get(title, lang)
                if not tt:
                    log.append('title: ' + title); tt = title
                out.append('<title>%s</title>' % esc_text(tt)); i += 3; continue
            if tg and tg['name'] == 'option' and not tg['close']:
                # den danske tekst sendes til Formspree, så medarbejderne ser det samme uanset sprog
                al = attrs_list(tg['attrs'])
                danish = norm(toks[i + 1]) if i + 1 < len(toks) and not is_tag(toks[i + 1]) else ''
                if danish and 'value' not in dict(al):
                    al.append(['value', danish])
                out.append(rw(build_tag('option', al))); i += 1; continue
            out.append(rw(t)); i += 1; continue
        out.append(t); i += 1
    result = ''.join(out)
    result = HREFLANG_RE.sub('', result)
    can = re.search(r'<link rel="canonical" href="[^"]+">\n', result)
    result = result[:can.end()] + hreflang_block(page) + '\n' + result[can.end():]
    result = result.replace('<span id="langName">Dansk</span>', '<span id="langName">%s</span>' % LANG_META[lang]['name'])
    result = result.replace('<svg class="flag" id="langFlag" aria-hidden="true"><use href="#f-da"></use></svg>',
                            '<svg class="flag" id="langFlag" aria-hidden="true"><use href="#f-%s"></use></svg>' % lang)
    result = KUNDANSK_RE.sub('\n', result)
    result = sync_faq_ld(result)
    if lang == 'uk':
        # Lato har ingen kyrilliske tegn; Cormorant Garamond har. Brødteksten sættes derfor i Source Sans 3, og den preloades i stedet for Lato.
        result = result.replace('href="/fonts/lato-400-latin.woff2">', 'href="/fonts/source-sans-3-400-700-cyrillic.woff2">')
        result = result.replace('<link rel="stylesheet" href="/styles.css">',
                                '<link rel="stylesheet" href="/styles.css">\n<style>:root{--body:\'Source Sans 3\',system-ui,-apple-system,sans-serif}</style>')
    result = re.sub(r'\n{3,}', '\n\n', result)
    result = result.replace('<!DOCTYPE html>\n', '<!DOCTYPE html>\n<!-- Genereret af build_lang.py ud fra %s. Ret ikke her: ret den danske side og i18n/tr/*.json, og kør "python build_lang.py build". -->\n' % page, 1)
    return result, log


FAQ_VIS_RE = re.compile(r'<details>\s*<summary><span[^>]*>(.*?)</span></summary>\s*<p[^>]*>(.*?)</p>', re.S)


def sync_faq_ld(page_html):
    """FAQPage-JSON-LD skal ord for ord svare til den synlige FAQ; den genereres derfor ud fra HTML'en."""
    vis = FAQ_VIS_RE.findall(page_html)
    if not vis:
        return page_html
    for m in re.finditer(r'(<script type="application/ld\+json">)(.*?)(</script>)', page_html, re.S):
        data = json.loads(m.group(2))
        if data.get('@type') != 'FAQPage':
            continue
        data['mainEntity'] = [{'@type': 'Question', 'name': html.unescape(strip_tags(q)),
                               'acceptedAnswer': {'@type': 'Answer', 'text': html.unescape(strip_tags(a))}} for q, a in vis]
        return page_html[:m.start()] + m.group(1) + '\n' + json.dumps(data, ensure_ascii=False, indent=1) + '\n' + m.group(3) + page_html[m.end():]
    return page_html


def write_sitemap():
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for p, m in PAGES.items():
        for l in ('da', 'en', 'de', 'uk'):
            lines.append('  <url>')
            lines.append('    <loc>%s%s</loc>' % (SITE, m[l]))
            lines.append('    <lastmod>%s</lastmod>' % LASTMOD)
            for l2 in ('da', 'en', 'de', 'uk'):
                lines.append('    <xhtml:link rel="alternate" hreflang="%s" href="%s%s"/>' % (l2, SITE, m[l2]))
            lines.append('    <xhtml:link rel="alternate" hreflang="x-default" href="%s%s"/>' % (SITE, m['da']))
            lines.append('  </url>')
    lines.append('</urlset>')
    io.open('sitemap.xml', 'w', encoding='utf-8').write('\n'.join(lines) + '\n')


def build():
    seeds = json.load(io.open('i18n/seeds.json', encoding='utf-8')) if os.path.exists('i18n/seeds.json') else {}
    look = Lookup(load_translations(), seeds)
    problems = 0
    for p in PAGES:
        update_danish(p)
        for lang in LANGS:
            html_out, log = build_page(p, lang, look)
            target = PAGES[p][lang]
            path = target.lstrip('/') + ('index.html' if target.endswith('/') else '')
            os.makedirs(os.path.dirname(path), exist_ok=True)
            io.open(path, 'w', encoding='utf-8').write(html_out)
            problems += len(log)
            print('  %-42s %s' % (path, 'ok' if not log else '%d mangler' % len(log)))
            for l in log[:6]:
                print('      - ' + l)
            if len(log) > 6:
                print('      ... og %d mere' % (len(log) - 6))
    write_sitemap()
    print('sitemap.xml: %d URL\'er' % (len(PAGES) * 4))
    print('Færdig.' if not problems else 'Færdig med %d mangler.' % problems)
    return problems


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'harvest'
    if cmd == 'harvest':
        harvest()
    elif cmd == 'build':
        sys.exit(1 if build() else 0)
    else:
        print(__doc__)
