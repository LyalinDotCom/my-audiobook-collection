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
    match = re.match(r'\d+(?:\.\d+)?', b['reading_position'])
    return (float(match[0]) if match else 10000, b['title'].casefold())

def name_order(name):
    return re.sub(r'^(the|a|an) ', '', name.casefold())

def sections(items):
    result = collections.defaultdict(list)
    for b in items:
        result[(b['reading_section_order'], b['reading_section'])].append(b)
    return [(name, sorted(result[(rank,name)], key=order)) for rank,name in sorted(result)]

def timestamp(seconds):
    return f'{int(seconds)//60}:{int(seconds)%60:02d}'

groups = collections.defaultdict(list)
for book in books:
    groups[(book['group_kind'], book['reading_family'])].append(book)
keys = sorted(groups, key=lambda k: (0 if k[0] == 'series' else 1, name_order(k[1])))
anchors = {key:f'group-{i+1:02d}' for i,key in enumerate(keys)}
series_count = len({b['group'] for b in books if b['group_kind'] == 'series'})
standalone_count = sum(b['group_kind'] == 'standalone' for b in books)
lines = [
    '# My Audiobook Collection', '',
    f'**238 library titles · {series_count} series or named collections · {standalone_count} titles without a cataloged series**', '',
    'Cataloged from the supplied Audible library recording on **September 10, 2026**. The extracted total matches the **238 titles** displayed in the video. Box sets count as one library title.', '',
    'Click any cover or **Audible** link to open the product page. **Cover art** opens the full image. **Video** is the first observed timestamp in the source recording, rounded down to a whole second.', '',
    'Browse by **series/universe → trilogy or subseries → book number**. Related trilogies stay together. Order numbers are local to each subsection; the original Audible sequence is retained in the JSON. Longer series are not artificially divided into trilogies. This catalog contains only the books shown, and does not imply every series is complete. See [verification and reading-order notes](VERIFICATION.md).', '',
    '**Edition exceptions:** *Start with Why* and *Getting Things Done* link to current editions that may differ from the recordings owned. The edition of *Intelligence in War* remains unconfirmed. *The Iliad* and *Team of Rivals* are matched to the abridged editions shown.', '',
    *category_summary(), '',
    '## Series and trilogy index', '', '| Series / universe / category | Trilogies and subseries | Titles |', '|---|---|---:|'
]
for key in keys:
    names = [name for name,items in sections(groups[key])]
    detail = ' → '.join(names) if names != [key[1]] else '—'
    lines.append(f'| [{key[1]}](#{anchors[key]}) | {detail} | {len(groups[key])} |')
for key in keys:
    kind,name = key
    lines += ['', f'<a id="{anchors[key]}"></a>', '', f'## {name}', '', f'{len(groups[key])} title'+('s' if len(groups[key]) != 1 else '')+'.', '']
    if name == 'Good to Great':
        lines += ['Audible’s named collection. Its numbering is not publication order; *Good to Great* has no sequence in its individual listing.', '']
    if name == 'Revelation Space universe':
        lines += ['The core sequence follows the author’s stated order. Companion works and the Prefect Dreyfus subseries have their own sections; their placement is not a required universe-wide chronology.', '']
    if name == 'Uplift Saga':
        lines += ['The original three novels are followed by the separate Uplift Trilogy, with numbering restarted at 1 for *Brightness Reef*.', '']
    if name == 'Red Rising':
        lines += ['The original trilogy is separate from the sequel saga. The three sequel books owned here do not imply the sequel saga is a trilogy or complete.', '']
    if name == 'Expeditionary Force':
        lines += ['Main-series books and the Mavericks spinoff each retain their own sequence. Spinoffs are kept together rather than interleaved with the main-series timeline.', '']
    for section, section_books in sections(groups[key]):
      if section != name:
        lines += [f'### {section}', '']
      lines += ['| Cover | Order | Book and author | Links | Video |', '|---|---:|---|---|---|']
      for b in section_books:
        cover=f'<a href="{esc(b["audible_url"])}"><img src="{esc(b["cover_url"])}" alt="{esc(b["title"])} cover" width="80" height="80"></a>'
        description=f'**{esc(b["title"])}**<br>{esc("; ".join(b["authors"]))}<br><small>{esc(b["primary_category"])}</small>'
        if b['notes']:
            description += '<br><em>'+esc(b['notes'])+'</em>'
        links=f'[Audible]({b["audible_url"]}) · [Cover art]({b["cover_url"]})'
        lines.append(f'| {cover} | {esc(b["reading_position"] or "—")} | {description} | {links} | {timestamp(b["evidence_seconds"])} |')
      lines += ['']
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
        'Grouped by series/universe, then trilogy or subseries, then book number. Standalone titles follow the series.', '']
    families = collections.defaultdict(list)
    for b in books:
        if b['primary_category'] == name:
            families[b['reading_family'] if b['group_kind'] == 'series' else 'Standalone titles'].append(b)
    for family in sorted(families,key=lambda f:(f == 'Standalone titles',name_order(f))):
        category_lines += [f'### {family}', '']
        for section, section_books in sections(families[family]):
            if section != family:
                category_lines += [f'#### {section}', '']
            category_lines += ['| Order | Title | Author |', '|---:|---|---|']
            for b in section_books:
                category_lines.append(f'| {esc(b["reading_position"] or "—")} | [{esc(b["title"])}]({b["audible_url"]}) | {esc("; ".join(b["authors"]))} |')
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
