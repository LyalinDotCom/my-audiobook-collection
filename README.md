# My Audiobook Collection

A catalog of **238 audiobook library titles**, extracted from an Audible screen recording and organized by series.

## [Browse the complete collection →](BOOKS.md)

The catalog includes:

- **54 series and named collections**, with book numbers and omnibus ranges.
- **53 titles without a cataloged series**, organized into eight subject groups.
- Clickable cover thumbnails, full cover art links, and direct Audible product links for every title.
- Source-video timestamps and notes for edition differences.

All 238 titles shown by the library counter are accounted for. A box set counts as one library title. Missing installments have not been added to the collection.

<!-- CATEGORY-SUMMARY:START -->
## Books by category

Each library title is assigned one primary genre or subject. These are editorial classifications; overlapping genres are counted once, and each box set counts as one title.

| Category | Titles | Share |
|---|---:|---:|
| [Science fiction](CATEGORIES.md#category-01) | 128 | 53.8% |
| [Thrillers, espionage & mystery](CATEGORIES.md#category-02) | 37 | 15.5% |
| [History, military & politics](CATEGORIES.md#category-03) | 19 | 8.0% |
| [Business, leadership & productivity](CATEGORIES.md#category-04) | 15 | 6.3% |
| [Fantasy](CATEGORIES.md#category-05) | 11 | 4.6% |
| [Biography, memoir & personal essays](CATEGORIES.md#category-06) | 9 | 3.8% |
| [Educational — science, data & learning](CATEGORIES.md#category-07) | 4 | 1.7% |
| [Society & culture](CATEGORIES.md#category-08) | 4 | 1.7% |
| [Literary classics & mythology](CATEGORIES.md#category-09) | 3 | 1.3% |
| [Parenting & relationships](CATEGORIES.md#category-10) | 3 | 1.3% |
| [Health, nutrition & fitness](CATEGORIES.md#category-11) | 2 | 0.8% |
| [Personal development & psychology](CATEGORIES.md#category-12) | 2 | 0.8% |
| [Personal finance & investing](CATEGORIES.md#category-13) | 1 | 0.4% |
| **Total** | **238** | **100%** |

**Fiction: 179 · Nonfiction: 59.** Percentages are rounded.

“Educational” here covers science, data, and learning. History, business, health, and self-help are counted separately. See [the category index](CATEGORIES.md) for definitions, individual titles, and crossover notes.
<!-- CATEGORY-SUMMARY:END -->

### Files

| File | Contents |
|---|---|
| [BOOKS.md](BOOKS.md) | Complete illustrated catalog and series index |
| [CATEGORIES.md](CATEGORIES.md) | Genre and subject counts, definitions, and every title grouped by category |
| [data/library.json](data/library.json) | Structured records, Audible ASINs, cover URLs, and source timestamps |
| [VERIFICATION.md](VERIFICATION.md) | Extraction method, checks, and edition caveats |
| [scripts/render_catalog.py](scripts/render_catalog.py) | Rebuilds both indexes and this page's category summary from JSON |

### Edition notes

*The Iliad* and *Team of Rivals* are matched to the abridged editions visible in the recording. *Start with Why* and *Getting Things Done* link to current editions that may differ from the owned recordings. The exact edition of *Intelligence in War* remains unconfirmed. These exceptions are marked beside the books.

### Update the catalog

Edit `data/library.json`, including each title's `primary_category` and `fiction_or_nonfiction`, then run:

```sh
python3 scripts/render_catalog.py
```

The generator uses Python's standard library. Its count assertion reflects this 238-title snapshot; update the source counts and assertion deliberately when adding future books.

Catalog snapshot: **September 10, 2026**. The source video, extracted frames, and temporary working files are excluded from the repository. Cover images are linked from Audible/Amazon and remain the property of their respective rights holders.
