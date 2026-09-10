"""Render BOOKS.md, CATEGORIES.md, and the README category summary from JSON."""
import collections
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / 'data/library.json').read_text())
books = data['books']
assert len(books) == data['source']['displayed_title_count'] == 238
assert len({b['id'] for b in books}) == len(books)
assert len({b['audible_asin'] for b in books}) == len(books)
assert all(b['cover_url'].startswith('https://') and b['audible_url'].startswith('https://www.audible.com/pd/') for b in books)
category_definitions = {c['name']: c for c in data['category_scheme']['categories']}
assert all(b['primary_category'] in category_definitions for b in books)
assert all(b['fiction_or_nonfiction'] == category_definitions[b['primary_category']]['type'] for b in books)
category_counts = collections.Counter(b['primary_category'] for b in books)
assert sum(category_counts.values()) == len(books)
category_names = sorted(category_counts, key=lambda c: (-category_counts[c], c.casefold()))
category_anchors = {name:f'category-{i+1:02d}' for i,name in enumerate(category_names)}
type_counts = collections.Counter(b['fiction_or_nonfiction'] for b in books)

def category_summary(link_prefix='CATEGORIES.md'):
    rows = ['## Books by category', '',
        'Each library title is assigned one primary genre or subject. These are editorial classifications; overlapping genres are counted once, and each box set counts as one title.', '',
        '| Category | Titles | Share |', '|---|---:|---:|']
    for name in category_names:
        count = category_counts[name]
        rows.append(f'| [{name}]({link_prefix}#{category_anchors[name]}) | {count} | {count / len(books):.1%} |')
    rows += [f'| **Total** | **{len(books)}** | **100%** |', '',
        f'**Fiction: {type_counts["Fiction"]} · Nonfiction: {type_counts["Nonfiction"]}.** Percentages are rounded.', '',
        '“Educational” here covers science, data, and learning. History, business, health, and self-help are counted separately. See [the category index](CATEGORIES.md) for definitions, individual titles, and crossover notes.']
    return rows

def esc(s):
    return html.escape(str(s), quote=True).replace('|', '&#124;')

def order(b):
    match = re.match(r'\d+(?:\.\d+)?', b['sequence'])
    return (float(match[0]) if match else 10000, b['title'].casefold())

def timestamp(seconds):
    return f'{int(seconds)//60}:{int(seconds)%60:02d}'

groups = collections.defaultdict(list)
for book in books:
    groups[(book['group_kind'], book['group'])].append(book)
keys = sorted(groups, key=lambda k: (0 if k[0] == 'series' else 1, k[1].casefold()))
anchors = {key:f'group-{i+1:02d}' for i,key in enumerate(keys)}
series_count = sum(key[0] == 'series' for key in keys)
standalone_count = sum(b['group_kind'] == 'standalone' for b in books)
lines = [
    '# My Audiobook Collection', '',
    f'**238 library titles · {series_count} series or named collections · {standalone_count} titles without a cataloged series**', '',
    'Cataloged from the supplied Audible library recording on **September 10, 2026**. The extracted total matches the **238 titles** displayed in the video. Box sets count as one library title.', '',
    'Click any cover or **Audible** link to open the product page. **Cover art** opens the full image. **Video** is the first observed timestamp in the source recording, rounded down to a whole second.', '',
    'Series are sorted by Audible’s sequence, including novellas and omnibus ranges. This is a catalog of the books shown, not a claim that every series is complete. Books without a cataloged series are grouped by subject. See [verification and edition notes](VERIFICATION.md).', '',
    '**Edition exceptions:** *Start with Why* and *Getting Things Done* link to current editions that may differ from the recordings owned. The edition of *Intelligence in War* remains unconfirmed. *The Iliad* and *Team of Rivals* are matched to the abridged editions shown.', '',
    *category_summary(), '',
    '## Index', '', '| Series / collection / category | Titles |', '|---|---:|'
]
for key in keys:
    lines.append(f'| [{key[1]}](#{anchors[key]}) | {len(groups[key])} |')
for key in keys:
    kind,name = key
    lines += ['', f'<a id="{anchors[key]}"></a>', '', f'## {name}', '', f'{len(groups[key])} title'+('s' if len(groups[key]) != 1 else '')+'.', '']
    if name == 'Good to Great':
        lines += ['Audible’s named collection. Its numbering is not publication order; *Good to Great* has no sequence in its individual listing.', '']
    if name == 'Revelation Space':
        lines += ['The Prefect Dreyfus books are grouped separately under **The Prefect Dreyfus Emergencies**. Audible’s sequence here is a catalog order, not a recommended chronological reading order.', '']
    if name == 'Uplift Saga':
        lines += ['*Brightness Reef*, *Infinity’s Shore*, and *Heaven’s Reach* also form the Uplift Trilogy (books 1–3), corresponding to Uplift Saga books 4–6.', '']
    lines += ['| Cover | Order | Book and author | Links | Video |', '|---|---:|---|---|---|']
    for b in sorted(groups[key], key=order):
        cover=f'<a href="{esc(b["audible_url"])}"><img src="{esc(b["cover_url"])}" alt="{esc(b["title"])} cover" width="80" height="80"></a>'
        description=f'**{esc(b["title"])}**<br>{esc("; ".join(b["authors"]))}<br><small>{esc(b["primary_category"])}</small>'
        if b['notes']:
            description += '<br><em>'+esc(b['notes'])+'</em>'
        links=f'[Audible]({b["audible_url"]}) · [Cover art]({b["cover_url"]})'
        lines.append(f'| {cover} | {esc(b["sequence"] or "—")} | {description} | {links} | {timestamp(b["evidence_seconds"])} |')
lines += ['', '## Sources', '',
    'Book identities and timestamps come from the supplied screen recording. Authors, narrators, ASINs, series positions, and cover URLs come from Audible’s US catalog, retrieved September 10, 2026. Each title links directly to its Audible record; per-book catalog source URLs are retained in [data/library.json](data/library.json).', '',
    'The four volumes of *A History of the English-Speaking Peoples* are grouped using their Audible subtitles and the [publisher description for The Great Democracies](https://www.audible.com/pd/The-Great-Democracies-Audiobook/B002V1OIRW). The *Start with Why* grouping follows [Audible’s series index](https://www.audible.com/series/Start-with-Why-Series-Audiobooks/B0F79MT9ZX).', '',
    'Cover images remain hosted by Audible/Amazon and belong to their respective rights holders. Availability and cover designs can change by date and region.', '']
(ROOT / 'BOOKS.md').write_text('\n'.join(lines))

category_lines = ['# My Audiobook Collection — Category Index', '',
    'Browse all **238 library titles** by primary genre or subject. Return to the [series catalog](BOOKS.md) for cover art, series numbers, and edition notes.', '',
    *category_summary(''), '', '## How crossover books are counted', '',
    *['- '+note for note in data['category_scheme']['boundary_notes']], '',
    'The assignments are editorial judgments informed by book content, series, and publisher descriptions; they are not a verbatim export of Audible taxonomy. For example, the [Convergence description](https://www.audible.com/pd/B09ZZ8VMKL) calls it urban fantasy, the [Four Minutes publisher description](https://www.blackstonepublishing.com/products/book-edrn) describes its speculative premise, and [Beneath the Dark Ice](https://www.audible.com/pd/B0065717C2) is presented as supernatural suspense.', '']
for name in category_names:
    category_lines += [f'<a id="{category_anchors[name]}"></a>', '', f'## {name}', '',
        f'**{category_counts[name]} titles** · {category_definitions[name]["type"]}', '',
        category_definitions[name]['definition'], '',
        '| Title | Author | Series / collection |', '|---|---|---|']
    for b in sorted((b for b in books if b['primary_category'] == name), key=lambda b:b['title'].casefold()):
        series = b['group'] if b['group_kind'] == 'series' else '—'
        if b['group_kind'] == 'series' and b['sequence']:
            series += ' · '+b['sequence']
        category_lines.append(f'| [{esc(b["title"])}]({b["audible_url"]}) | {esc("; ".join(b["authors"]))} | {esc(series)} |')
    category_lines += ['']
(ROOT / 'CATEGORIES.md').write_text('\n'.join(category_lines))

readme_path = ROOT / 'README.md'
readme = readme_path.read_text()
start, end = '<!-- CATEGORY-SUMMARY:START -->', '<!-- CATEGORY-SUMMARY:END -->'
assert readme.count(start) == readme.count(end) == 1
before, remainder = readme.split(start)
_, after = remainder.split(end)
readme_path.write_text(before+start+'\n'+ '\n'.join(category_summary())+'\n'+end+after)
print(f'Rendered {len(books)} books across {len(keys)} series/subject groups and {len(category_names)} primary categories.')
