"""Entry point for the 22 November 2026 front page.

The picture is drawn ahead of time by render.py (Pillow) and stored in
this repository as news_image.png. This program only moves that finished
PNG into place as /output/entry.png, using the standard library alone,
so the sandbox run needs no network and no third-party package.
"""

import shutil
from pathlib import Path

IMAGE_NAME = "news_image.png"
OUTPUT_DIR = Path("/output")
OUTPUT_NAME = "entry.png"


def main():
    here = Path(__file__).resolve().parent
    picture = here / IMAGE_NAME
    if not picture.is_file():
        raise SystemExit(f"missing {IMAGE_NAME} next to main.py")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    destination = OUTPUT_DIR / OUTPUT_NAME
    shutil.copyfile(picture, destination)
    size = destination.stat().st_size
    print(f"wrote {destination} ({size} bytes)")


if __name__ == "__main__":
    main()
