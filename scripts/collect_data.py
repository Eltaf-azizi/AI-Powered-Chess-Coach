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