# 17 November 2026 — World News in One Image

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/joyrichh/makefun-news-image-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/joyrichh/makefun-news-image-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

Competition: [`news-image-20261117`](https://make.fun/bounty/news-image-20261117).

A 1024×1024 PNG summarizing the supplied verified news for Tuesday,
17 November 2026, using six story cards and an “Also today” strip.

## The six stories

1. **MIDDLE EAST:** U.S. strikes Iran; Tehran hits back in Gulf
2. **UKRAINE:** Crimea Bridge partly collapses after Ukrainian strike
3. **DIPLOMACY:** Xi, Trump and Putin set for first three-way summit
4. **TECH:** U.S. tightens AI chip export rules on China
5. **MARKETS:** Nvidia posts $116B quarter as Huang offers return
6. **ISRAEL:** Eisenkot bloc ousts Netanyahu ally as Knesset speaker

Also today:

- UK sanctions eight Israeli firms over West Bank settlements; Israel calls it a hostile act.
- Japan scrambles jets as Russian aircraft enter its airspace.
- Houthis advance in Yemen; government forces pull back to defend Aden.

The supplied news was verified on 18 November 2026 against Reuters, AP, NPR,
AFP and Standard Topic. `news.json` preserves the full headlines, summaries,
tags, colors, source list and verification note. The image credits Reuters,
AP, NPR and AFP.

## How the program works

`main.ts` uses only the Node.js 22 standard library. It reads `entry.png.b64`,
decodes the PNG, checks its signature, and writes `/output/entry.png`.
`MAKEFUN_OUTPUT_DIR` overrides the output directory for local verification:

```sh
mkdir -p out
MAKEFUN_OUTPUT_DIR=out node main.ts
cmp entry.png out/entry.png
```

`build_image.py` is an authoring tool that reads `news.json` and renders
`entry.png` with Pillow and system DejaVu fonts, preserving the original
two-column, six-card layout, typography and 1024×1024 dimensions.
To rebuild the embedded image:

```sh
python3 build_image.py
base64 -w0 entry.png > entry.png.b64
```

The generated binary `entry.png` stays locally available and is git-ignored;
`entry.png.b64` is the committed text representation.

## Deterministic and offline

The entry uses no network, randomness, timestamps or external packages at
runtime. Every run decodes the same embedded bytes. Rebuilding with the same
Pillow version, fonts and news data also produces identical PNG bytes.

## Verification

Two consecutive `python3 build_image.py` builds produced identical SHA-256
hashes: `246e9cbd5f991ec1ced3672db2cc5c7c1e2f5938726367b64a32537701631289`.
The resulting RGB PNG is **1024×1024 pixels**, **137,265 bytes**.
After regenerating `entry.png.b64` with `base64 -w0 entry.png`, running
`MAKEFUN_OUTPUT_DIR=out node main.ts` and `cmp entry.png out/entry.png`
confirmed that the runtime output is byte-identical to the rendered image.

The longest “Also today” item measures 852.34 pixels including its bullet,
within the 932-pixel text area. The renderer now applies width-aware
ellipsis truncation to each strip item and bounded wrapping to story text;
current headlines and summaries fit without truncation.

## License and prompt

`LICENSE` contains the MIT license and its SPDX identifier. `prompt.txt`
preserves Jese's original words.
