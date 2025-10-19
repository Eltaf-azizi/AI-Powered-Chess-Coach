# models/train_model.py
"""
Training script for:
- move_evaluator.pkl : RandomForestRegressor predicting a position evaluation (centipawns)
- strategy_recommender.pkl : RandomForestClassifier predicting move-type labels

Behavior:
- If STOCKFISH_PATH env var is set (or config/settings.yaml contains engine path),
  the script will use Stockfish to label positions (eval + best move -> label).
- Otherwise falls back to generating a small synthetic dataset.

Usage:
    python models/train_model.py --games_dir ../data/games --out_dir ../models

Notes:
- For real training, populate data/games with PGN files containing many games.
- This script is intentionally simple to make it easy to run and extend.
"""

import os
import argparse
import chess.pgn
import chess
import random
import numpy as np
import joblib
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from tqdm import tqdm
from pathlib import Path
from ai.utils import encode_board_features, move_type_label, label_to_int
import subprocess
import chess.engine
import multiprocessing

DEFAULT_OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "models")
DEFAULT_GAMES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "games")
STOCKFISH_ENV = os.environ.get("STOCKFISH_PATH", "")
