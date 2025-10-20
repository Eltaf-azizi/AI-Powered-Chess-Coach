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


def find_stockfish(config_path=None):
    """
    Try to find stockfish binary from env or config file. Return path or None.
    """
    if STOCKFISH_ENV and os.path.exists(STOCKFISH_ENV):
        return STOCKFISH_ENV
    # check common paths
    for p in ["/usr/bin/stockfish", "/usr/local/bin/stockfish", "C:\\Program Files\\stockfish\\stockfish.exe"]:
        if os.path.exists(p):
            return p
    # try reading config file if provided
    if config_path and os.path.exists(config_path):
        try:
            import yaml
            with open(config_path, "r") as f:
                cfg = yaml.safe_load(f)
            engine_cfg = cfg.get("engine", {})
            path = engine_cfg.get("stockfish_path", "")
            if path and os.path.exists(path):
                return path
        except Exception:
            pass
    return None

def sample_positions_from_pgns(games_dir, max_positions=2000, per_game_limit=50):
    """
    Iterate through PGN files and sample positions.
    Yields (fen, last_move_uci) where fen is board AFTER the move.
    """
    out = []
    if not os.path.exists(games_dir):
        return out
    for pgn_file in Path(games_dir).glob("*.pgn"):
        try:
            with open(pgn_file, "r", encoding="utf-8", errors="ignore") as f:
                while True:
                    game = chess.pgn.read_game(f)
                    if game is None:
                        break
                    board = game.board()
                    count = 0
                    for move in game.mainline_moves():
                        board.push(move)
                        # sample some positions to avoid too many per game
                        if random.random() < 0.25 and count < per_game_limit:
                            out.append((board.fen(), move.uci()))
                            count += 1
                        if len(out) >= max_positions:
                            return out
        except Exception as e:
            print("Failed reading PGN", pgn_file, e)
    return out

def label_positions_with_stockfish(positions, stockfish_path, time_limit=0.05):
    """
    For each fen, run Stockfish to get evaluation (cp) and best move.
    Returns list of tuples (fen, last_move_uci, eval_cp, best_move_uci)
    """
    engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
    labeled = []
    try:
        for fen, last_move in tqdm(positions):
            board = chess.Board(fen)
            try:
                info = engine.analyse(board, chess.engine.Limit(time=time_limit))
                score = info.get("score")
                if score is None:
                    eval_cp = 0.0
                else:
                    if score.is_mate():
                        mate = score.white().mate()
                        eval_cp = 100000.0 if mate and mate > 0 else -100000.0
                    else:
                        eval_cp = float(score.white().cp)
                # best move
                try:
                    mv = engine.play(board, chess.engine.Limit(depth=12))
                    best = mv.move.uci() if mv and mv.move else None
                except Exception:
                    best = None
            except Exception:
                eval_cp = 0.0
                best = None
            labeled.append((fen, last_move, eval_cp, best))
    finally:
        engine.quit()
    return labeled


def generate_synthetic_dataset(n=500):
    """
    Generates simple random legal positions using random playouts
    and uses a cheap heuristic evaluation as labels.
    """
    data = []
    for _ in range(n):
        board = chess.Board()
        # play random small number of moves
        for _ in range(random.randint(0, 20)):
            if board.is_game_over():
                break
            moves = list(board.legal_moves)
            board.push(random.choice(moves))
        # pick one legal move and apply it to create a sample (post-move fen)
        if list(board.legal_moves):
            mv = random.choice(list(board.legal_moves))
            board.push(mv)
            fen = board.fen()
            # heuristic eval via simple material
            values = {
                chess.PAWN: 100, chess.KNIGHT: 320, chess.BISHOP: 330,
                chess.ROOK: 500, chess.QUEEN: 900, chess.KING: 20000
            }
            sc = 0
            for ptype,val in values.items():
                sc += len(board.pieces(ptype, chess.WHITE)) * val
                sc -= len(board.pieces(ptype, chess.BLACK)) * val
            best = mv.uci()
            data.append((fen, mv.uci(), float(sc), best))
    return data