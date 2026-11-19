# The World — Thursday 19 November 2026

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/melatim80186/makefun-news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/melatim80186/makefun-news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

A program that writes one image summing up 19 November 2026 in world news.

The day's stories are gathered into a single broadsheet front page: the
biggest headlines from every continent, laid out the way a newspaper would
have printed them that morning — one page, one picture of the world on
that Thursday.

## The image

The finished page is a 1024x1024 broadsheet image. It is bundled with this
repository as `entry.png`, and running the program copies it to the output
location, checking along the way that the copy is exactly the same as the
bundled original.

## How to run it

```sh
python3 main.py
```

That writes the image to `/output/entry.png` (creating the directory if it
does not exist yet) and verifies the written bytes match the bundled image.
If anything does not match, the program reports the problem and exits with
a non-zero status instead of leaving a bad file behind.

Requires Python 3.13 and nothing else — the standard library only, no
extra packages to install.

## How it works

Running `main.py` does three things, in order:

1. It finds the bundled `entry.png` sitting next to the script.
2. It copies those bytes to `/output/entry.png`.
3. It reads the copy back and compares it byte for byte with the original,
   refusing to finish successfully unless the two are identical.

There is no image generation at run time — the artwork is fixed, and the
program's job is to deliver it exactly as bundled.
