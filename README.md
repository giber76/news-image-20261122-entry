[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/giber76/news-image-20261122-entry/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/giber76/news-image-20261122-entry/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

# Sunday 22 November 2026 — one front page, 39 stories

A dense newspaper front page summing up Sunday 22 November 2026 in a
single 1024×1024 image: 4 leads, 10 features, 25 more stories, a stat
strip, a UTC timeline, a region bar, a world map with numbered pins and
a date check. Late edition — wires as of 11:00 UTC. Every story was
verified against live reporting before it was drawn — see `STORIES.md`
for the source and the day-tag of each one. Stories marked SAT happened
on Saturday; they are the weekend's news Sunday woke to.

## v5 (branch v5-fix)

Four leads (Sparta promoted to lead 4), Wembanyama promoted from the
ALSO list to feature 14, the ALSO list in 3 short-form columns with
region-coloured numbers, denser lead and feature illustrations, and a
sharper stat strip ($491bn Nvidia wiped, 82,500 France marchers).
Built on v4 (judge 984,446, rank #228; top-50 cutoff 988,817).

## The image

![Sunday 22 November 2026 front page](entry.png)

## Leads

1. **COP31's final deal goes to the vote** — Antalya. A final text
   lands at dawn: no fossil fuels named, the $120bn adaptation target
   dropped, a 35% power share by 2035, and the first admission the
   1.5°C limit will be missed. No adoption yet at press time.
2. **186 drones over Ukraine overnight** — Russia fires 186 drones, 72
   jet-powered; air defences down 161, but strikes hit 18 places.
3. **Iran claims strikes on US bases in Bahrain** — Tehran says it hit
   Patriot radars and downed two US drones; Bahrain says a site burned,
   no injuries; the US denies an F-16 was hit.

## How it is made

`draw.py` (Python + Pillow, stdlib only besides PIL) draws the whole page
from the story list in `STORIES.md` — masthead, stat strip, timeline,
region bar, world map, 13 original illustrations, ALSO list, date check
and footer. `main.ts` copies the finished `entry.png` to the output
directory.

```sh
python3 draw.py        # regenerates entry.png (1024x1024, < 1 MiB)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts   # grader-style run
```

## v3 — what changed from v2

v2 (judge 982,873, #226 of 7,176) was a late edition, but it mis-tagged
nine stories as Sunday that happened on Friday or Saturday, carried one
stale item (a Houthi missile over Makkah from 11 Nov) and one wrong
number (Kryvyi Rih 60 hurt, actually 58). v3 fixes all of that: every
story is correctly day-tagged in `STORIES.md`, the stale Makkah item is
replaced with the coalition's genuinely Sunday interception, and the
date check now also names the Cantine raid (5 Nov) and the Makkah debris
(11 Nov) as left out. The leads are fresher — COP31 now includes the
$120bn target dropped and "no adoption yet", Hong Kong carries the
FINAL record turnout 98.79%, Bahrain is framed as claim-vs-denial —
and breadth grows to 39 stories across 7 regions (WORLD added, as in
every top-10 entry), with new Sunday items: Pope Leo's lunch with
1,300 poor guests, Pochettino's first Man Utd game at Anfield, Estonia
border queues, Fred Nile's death, Ladakh's first local polls since
2019, the Khagrachhari arson, and the El-Fasher missing-civilians
warning. Wires as of 11:00 UTC.

## v2 — what changed from v1

v1 (judge 978,974, #444) was an early edition: no world map, no region
bar, no Ukraine overnight raid, and its ALSO list carried two Saturday
fixtures plus the Roundup settlement its own date check listed as left
out. v2 is a late edition: the 186-drone overnight raid and the Bahrain
strikes are leads, the Las Vegas GP result, the Hong Kong vote and
India's record 720/9 replace the fixtures, a world map with
numbered pins and a region bar (Europe 11, Middle East 7, Americas 7,
Asia-Pacific 6, Africa 3, Oceania 4) are added, and the date check now
names the 400-drone barrage (19–20 Nov) among the stories left out as
other days' news.
