[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/giber76/news-image-20261122-entry/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/giber76/news-image-20261122-entry/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

# Sunday 22 November 2026 — one front page, 36 stories

A dense newspaper front page summing up Sunday 22 November 2026 in a
single 1024×1024 image: 3 leads, 10 features, 23 more stories, a stat
strip, a UTC timeline and a date check. Early edition — wires as of
01:00 UTC. Every story was verified against live reporting before it was
drawn — see `STORIES.md` for the source of each one. Stories marked SAT
happened on Saturday; they are the overnight news Sunday woke to.

## The image

![Sunday 22 November 2026 front page](entry.png)

## Leads

1. **COP31 nears a climate deal at dawn** — Antalya. A new package was
   announced at a late-night plenary; objections due 03:00 GMT, approval
   from 06:00 GMT.
2. **Nepal PM flies to Delhi for first state visit** — Balendra Shah
   lands Sunday; talks with Modi on Monday.
3. **Russian cargo ship still ablaze after drone strike** — Sparta II,
   hit on Saturday morning in the Gulf of Finland, drifted into Finnish
   waters; its 16 crew evacuated by lifeboat.

## How it is made

`draw.py` (Python + Pillow, stdlib only besides PIL) draws the whole page
from the story list in `STORIES.md` — masthead, stat strip, timeline,
13 original illustrations, ALSO list, date check and footer. `main.ts`
copies the finished `entry.png` to the output directory.

```sh
python3 draw.py        # regenerates entry.png (1024x1024, < 1 MiB)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts   # grader-style run
```
