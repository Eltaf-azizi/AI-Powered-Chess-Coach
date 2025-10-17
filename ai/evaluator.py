# ai/evaluator.py
"""
Evaluator: provides evaluate_board() that returns centipawn evaluation (float).
Behavior:
- If Stockfish (engine_service) is provided and available, prefers engine analysis.
- Otherwise uses a trained ML model (models/move_evaluator.pkl) if present.
- If no model, uses a fallback material evaluator.
"""

import os
import numpy as np
import joblib
import chess
from .utils import encode_board_features

MODEL_PATH_DEFAULT = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "models", "move_evaluator.pkl")
