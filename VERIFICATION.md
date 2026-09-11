# Verification and edition notes

## Coverage

The supplied Audible library recording is 88.433 seconds long and displays **238 titles**. Text recognition was performed on **354 sampled frames**, at four frames per second. Repeated views of the same book were merged, clipped title fragments were discarded, and spelling and punctuation were checked against Audible's catalog.

The resulting catalog contains **238 distinct title records and 238 distinct Audible ASINs**. Titles with identical names but different authors remain separate, such as *Into the Fire* by Gregg Hurwitz and by Craig A. Falconer. *Paradise*, *Not Alone*, and *Infinite* remain separate from the longer titles that contain those words.

Each record in [data/library.json](data/library.json) retains a first-observed timestamp. These times refer to the supplied recording, not an audiobook playback position. The source video's SHA-256 digest is retained for identification; the video and its iCloud sharing URL are not published.

## Catalog matching

Titles and authors were matched against Audible's US catalog on September 10, 2026. The catalog provides product ASINs, contributors, series metadata, runtimes, and Amazon-hosted cover images. Exact-title alternatives were reviewed using visible contributors, covers, and full durations where the video exposed them.

The source video is a library list, so it does not expose a unique product identifier for every entry. A catalog match establishes the book identity; it cannot guarantee the same historical edition in every case. Cover designs and availability can change.

| Title | Resolution |
|---|---|
| The Iliad | Matched to the abridged Robert Fagles translation with Bernard Knox introduction, narrated by Derek Jacobi and Maria Tucci. The video shows 8h 44m, matching ASIN `B002UZMV1Y`. |
| Team of Rivals | Matched to the abridged Richard Thomas narration. The video shows 9h 28m, matching ASIN `B002V8MOTE`. |
| Beneath the Dark Ice | The visible cover matches the older Sean Mangan edition, ASIN `B0065717C2`, rather than the newer catalog entry. |
| Intelligence in War | The title and cover match, but the recording shows remaining time rather than a full duration. The unabridged Richard Matthews edition is linked; the exact owned edition remains unconfirmed. |
| Start with Why | The library shows the original title without an anniversary label. The currently listed 15th Anniversary Edition supplies the product and cover links. This is an explicitly marked substitute, not an exact edition match. |
| Getting Things Done | The library shows a 7h 9m edition. The currently listed edition is 10h 17m. The current product and cover links are supplied with an explicit edition-difference note. |

## Organization

The 238 library titles are divided into **185 titles in 54 series or named collections** and **53 titles in eight subject groups**. Series numbering follows Audible's catalog and is not necessarily chronological or publication order. Each library entry appears once.

- *A History of the English-Speaking Peoples*: the four Audible subtitles identify volumes I–IV, even though the API omits series metadata. The [Audible publisher description](https://www.audible.com/pd/The-Great-Democracies-Audiobook/B002V1OIRW) also lists the four volumes.
- *The World Crisis*: volume 1 is identified by the title itself.
- *Uplift Saga*: the main six-book sequence is used. The later three volumes also belong to the Uplift Trilogy.
- *Revelation Space*: the Prefect Dreyfus books appear in their own subseries; the JSON retains secondary series associations supplied by Audible.
- *Good to Great*: Audible groups *Built to Last* in this named collection. *Good to Great* is grouped alongside it without inventing a sequence number for its individual listing.
- *Start with Why*: grouped using [Audible's series index](https://www.audible.com/series/Start-with-Why-Series-Audiobooks/B0F79MT9ZX).
- “Without a cataloged series” means the matched listing supplies no series and no separately verified series assignment was made. It does not establish that a book can never have a sequel or a related work.

## Reading order and trilogy grouping

Updated September 11, 2026. Both Markdown indexes now group titles by **series/universe → trilogy or subseries → numeric book position**, instead of alphabetizing individual books within a genre. Series names sort alphabetically while ignoring leading “The,” “A,” and “An.” Standalone titles follow series and remain alphabetical.

The original `group`, `sequence`, and `catalog_series` fields are preserved. The `reading_family`, `reading_section`, `reading_section_order`, and `reading_position` fields control presentation. Section positions are local numbers, not replacements for Audible's overall series numbers. Missing installments are not added or silently renumbered in ordinary series.

- **Black Fleet Saga:** Black Fleet Trilogy → Expansion Wars Trilogy → Unification War Trilogy, following the [author's series index](https://joshuadalzelle.com/series/black-fleet-saga).
- **Commonwealth universe:** Commonwealth Saga → Void Trilogy. The [publisher identifies the Void Trilogy as part of Commonwealth](https://www.penguinrandomhouse.com/series/TVT/commonwealth-the-void-trilogy/).
- **Uplift:** the original three novels are followed by the Uplift Trilogy: *Brightness Reef*, *Infinity's Shore*, *Heaven's Reach*. [David Brin identifies that second trilogy explicitly](https://www.davidbrin.com/fiction/upliftwar1.html).
- **Red Rising:** *Red Rising*, *Golden Son*, and *Morning Star* form the [original trilogy](https://penguinrandomhouselibrary.com/book/?isbn=9780593724460). The owned later books have a separate “Sequel saga” section; owning three of them does not make that saga a trilogy.
- **Revelation Space:** *Revelation Space* → *Redemption Ark* → *Absolution Gap*, following [Alastair Reynolds' own suggested sequence](https://www.alastairreynolds.com/novels/). *Inhibitor Phase*, companion works, and the Prefect Dreyfus subseries have separate sections. Companion placement is a browsing choice, not a required chronology.
- **Expeditionary Force:** the main series and Mavericks spinoff sit together, each retaining its own sequence. They are not interleaved into a universal reading timeline.

Other established trilogies retain their existing book numbers. Longer series such as the Expanse, Bobiverse, and Lightbringer are not arbitrarily split into three-book chunks. These presentation changes preserve all 238 titles and all category totals.

## Reproducibility

The curated JSON is the source of truth for the Markdown catalog. `python3 scripts/render_catalog.py` checks the expected record count, unique record IDs, unique ASINs, link formats, category membership, and fiction/nonfiction consistency before rendering `BOOKS.md`, `CATEGORIES.md`, and the category summary in `README.md`.

The category overview is separate from the series organization above. Each of the 238 titles has one editorial primary genre or subject, producing **13 categories: 179 fiction titles and 59 nonfiction titles**. The category definitions and crossover decisions are documented in [CATEGORIES.md](CATEGORIES.md) and in the JSON's `category_scheme`. Counts in every Markdown overview are generated from the same per-book category fields.

Live checks on September 10, 2026 returned **HTTP 200 for all 238 Audible product records and all 238 cover images**. Each product response returned the expected ASIN. No failed links were found in those checks. Audible storefront access and purchasing availability can still vary by region.

The repository contains catalog metadata and links. It does not contain audiobook audio, source video, extracted screenshots, access tokens, or copies of publisher cover files.
