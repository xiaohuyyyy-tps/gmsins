import os
import json
from pathlib import Path

PICS_DIR = Path(__file__).parent / "pics"
OUTPUT_FILE = Path(__file__).parent / "gallery-data.json"

SUPPORTED_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}


def scan():
    gallery = []

    if not PICS_DIR.exists():
        print(f"[warn] pics/ directory not found at {PICS_DIR}")
        return

    date_dirs = sorted(
        [d for d in PICS_DIR.iterdir() if d.is_dir()],
        reverse=True,
    )

    for date_dir in date_dirs:
        date_label = date_dir.name
        images = sorted(
            [
                f.name
                for f in date_dir.iterdir()
                if f.is_file() and f.suffix.lower() in SUPPORTED_EXTS
            ]
        )

        if images:
            gallery.append(
                {
                    "date": date_label,
                    "images": [f"pics/{date_label}/{img}" for img in images],
                }
            )

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(gallery, f, ensure_ascii=False, indent=2)

    total = sum(len(d["images"]) for d in gallery)
    print(f"[ok] Scanned {len(gallery)} date(s), {total} image(s) -> gallery-data.json")


if __name__ == "__main__":
    scan()
