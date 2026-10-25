# quran-waqf-ibtida-index

> **Experimental.** This index was read with AI from page images that are publicly
> accessible online. It has been checked carefully, but it is **not guaranteed to be 100%
> correct**. Before relying on any mark, check it against a printed mushaf. Corrections are
> welcome as issues.

Waqf and ibtida marks (HENTI / MULAI) for all 604 pages of the Madinah 15-line mushaf,
indexed by word as `surah:ayah:word`. The index joins onto any Quran text that uses the
quran.com / Tanzil Uthmani word segmentation; you do not need our pages or fonts.

- 2,213 marks across 76 surahs
- 2,202 `repeat` marks: an underline runs from MULAI to HENTI. You may stop at `stop`; if
  you do, resume from `restart`, which comes at or before `stop`.
- 11 `stop` marks: HENTI and MULAI stand side by side with no underline. You may stop at
  `stop` and carry on from the next word, `restart`.

## Source

The marks were read off the page images published at **[quran.tampang.com](https://quran.tampang.com/)**
(retrieved 2026-10-23). All credit for the placement of the waqf-ibtida marks goes to that
source. The site names no publisher and states no licence, so this repository adds no
licence of its own.

## Files

| File | What it is |
|---|---|
| `data/waqf-ibtida.json` | All marks, with the source, method and accuracy notes |
| `data/waqf-ibtida.csv` | The same marks as a table, one per row |
| `provenance/decisions.json` | Every mark settled by eye, with the reason for each |
| `provenance/stops.json` | The 11 no-underline stop marks |

## One mark

```json
{"id": 2, "kind": "repeat", "restart": "2:6:6", "stop": "2:6:9", "page": 3,
 "restart_line": 1, "stop_line": 1, "restart_text": "ءَأَنذَرْتَهُمْ", "stop_text": "تُنذِرْهُمْ",
 "text": "ءَأَنذَرْتَهُمْ أَمْ لَمْ تُنذِرْهُمْ", "basis": "readings agree"}
```

- Words are `surah:ayah:word`: 1-based, ayah numbers not counted, quran.com / Tanzil Uthmani
  segmentation. Riwayah Hafs 'an 'Asim.
- `page` is the 604-page Madinah mushaf. Line numbers are the printed lines of that page,
  with surah title and basmala lines counted.
- `basis` says why a mark stands:
  - `readings agree` (2,102): two independent readings name it.
  - `decided by eye` (105): the readings disagreed or a reader was unsure, so the mark was
    settled on an enlarged scan. The reason is in `provenance/decisions.json`.
  - `blind reading, tag positions checked` (6): no-underline stop marks seen by one reader,
    with the tag positions then checked on the scan.

## How it was made

1. **Line breaks fitted.** On many pages the scans break their lines 1 to 3 words
   differently from quran.com's layout, so every page's line breaks were first fitted to its
   own scan.
2. **Two independent readings of every page.** One was a script: the underline and tags are
   found by colour, and each tag goes to the word whose edge it is flush with. The other was
   by eye: readers saw each scan line with the same line typeset and numbered beneath it, and
   never saw the script's answer.
3. **Disagreements settled by hand.** A mark stands when two readings name it. Every mark
   only one reading named, and every reading marked unsure, was settled on an enlarged scan
   using the printing rule: MULAI is flush with the right end of the restart word, HENTI with
   the left end of the stop word. That came to about 170 decisions, each recorded with its
   reason.
4. **Earlier sample re-checked.** All 243 pairs that had been hand-checked earlier match
   this index.

Known limit: where a tag sits exactly between two words, it is assigned by the printing rule
above. Those cases are noted in `provenance/decisions.json`.

---

## Bahasa Indonesia

> **Eksperimen.** Data ini dibaca dengan bantuan AI dari gambar halaman yang bisa diakses
> publik. Sudah diperiksa dengan teliti, tetapi **belum tentu 100% benar**. Cocokkan dulu
> dengan mushaf cetak sebelum dipakai. Koreksi bisa dikirim lewat issue.

Indeks tanda waqaf ibtida (HENTI / MULAI) untuk 604 halaman mushaf Madinah 15 baris. Setiap
tanda dirujuk per kata dengan format `surat:ayat:kata`. Isinya 2.213 tanda: 2.202 tanda
**ulang** (bergaris, berhenti lalu mengulang dari MULAI) dan 11 tanda **berhenti** (tanpa
garis, lanjut ke kata berikutnya).

Setiap halaman dibaca dua kali secara terpisah, dan semua beda pendapat dicek dengan scan yang
diperbesar. Sumber: scan halaman di [quran.tampang.com](https://quran.tampang.com/).
