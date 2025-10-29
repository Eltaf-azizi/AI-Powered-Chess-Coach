# scripts/collect_data.py
import os
import requests
from pathlib import Path


OUT = Path(__file__).resolve().parents[1] / "data" / "games"
OUT.mkdir(parents=True, exist_ok=True)


# small sample PGN URL (public sample). You can replace with real datasets.
SAMPLES = {
    "sample1.pgn": "https://raw.githubusercontent.com/niklasf/python-chess/master/tests/data/games/wc2000.pgn"
}


def download():
    for name, url in SAMPLES.items():
        out = OUT / name
        if out.exists():
            print(name, "already exists")
            continue
        try:
            print("Downloading", url)
            r = requests.get(url, timeout=30)
            r.raise_for_status()
            out.write_bytes(r.content)
            print("Saved to", out)
        except Exception as e:
            print("Failed to download", url, e)



if __name__ == "__main__":
    download()
