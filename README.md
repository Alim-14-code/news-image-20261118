# news-image-20261118

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/Alim-14-code/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/Alim-14-code/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

A one-page newspaper front page summing up the world's news of Wednesday 18 November 2026 — 40 stories across 7 regions, one page. Three illustrated leads (Xi greets Trump on the tarmac in Shenzhen ahead of the first three-way summit with Putin; Kuwait and Bahrain intercept Iranian drones as the Gulf war widens; Voyager 1 becomes the first human-made object one light-day from Earth), ten more illustrated briefs (Ukraine's 141 drones, the Fed's minutes, Cyclone Akvan, the RSF's El Obeid killings, the EU's €45bn Ukraine loan, UK inflation at 3.6%, Gaza, Jeffries' Speaker nod, GTA VI's launch, Bangladesh's garment protests), a dotted world map with numbered pins, briefs 14–40, a day-in-numbers strip and a region count bar. A DATE CHECK box names what was deliberately left out because it was first reported on Tuesday 17 November. Rendered offline from researched, sourced reporting (Reuters, AP, AFP, BBC, Al Jazeera, ONS, IMD, NASA, Amnesty, WHO) as a deterministic 1024×1024 PNG; `render_r5.py` draws every illustration with Pillow (Noto fonts) and the map from Natural Earth land polygons shipped in this repo (`map_land.geojson`); `main.py` copies the finished image to `/output/entry.png` with the standard library only.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=e6d1qmmj&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards</sub>
