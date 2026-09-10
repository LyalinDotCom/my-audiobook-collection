# My Audiobook Collection

A catalog of **238 audiobook library titles**, extracted from an Audible screen recording and organized by series.

## [Browse the complete collection →](BOOKS.md)

The catalog includes:

- **54 series and named collections**, with book numbers and omnibus ranges.
- **53 titles without a cataloged series**, organized into eight subject groups.
- Clickable cover thumbnails, full cover art links, and direct Audible product links for every title.
- Source-video timestamps and notes for edition differences.

All 238 titles shown by the library counter are accounted for. A box set counts as one library title. Missing installments have not been added to the collection.

### Files

| File | Contents |
|---|---|
| [BOOKS.md](BOOKS.md) | Complete illustrated catalog and series index |
| [data/library.json](data/library.json) | Structured records, Audible ASINs, cover URLs, and source timestamps |
| [VERIFICATION.md](VERIFICATION.md) | Extraction method, checks, and edition caveats |
| [scripts/render_catalog.py](scripts/render_catalog.py) | Rebuilds the Markdown catalog from JSON |

### Edition notes

*The Iliad* and *Team of Rivals* are matched to the abridged editions visible in the recording. *Start with Why* and *Getting Things Done* link to current editions that may differ from the owned recordings. The exact edition of *Intelligence in War* remains unconfirmed. These exceptions are marked beside the books.

### Update the catalog

Edit `data/library.json`, then run:

```sh
python3 scripts/render_catalog.py
```

The generator uses Python's standard library. Its count assertion reflects this 238-title snapshot; update the source counts and assertion deliberately when adding future books.

Catalog snapshot: **September 10, 2026**. The source video, extracted frames, and temporary working files are excluded from the repository. Cover images are linked from Audible/Amazon and remain the property of their respective rights holders.
