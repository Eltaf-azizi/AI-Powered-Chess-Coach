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

class Evaluator:
    def __init__(self, engine_service=None, ai_config: dict = None, model_path: str = None):
        """
        engine_service: instance of ChessEngineService (may be None)
        ai_config: config dict with keys 'fallback_search_depth', 'engine_time' etc.
        model_path: path to saved move_evaluator.pkl
        """
        self.engine_service = engine_service
        self.config = ai_config or {}
        self.model_path = model_path or MODEL_PATH_DEFAULT
        self.model = None
        self._load_model()

    def _load_model(self):
        if os.path.exists(self.model_path):
            try:
                self.model = joblib.load(self.model_path)
            except Exception as e:
                print(f"[Evaluator] Could not load model at {self.model_path}: {e}")
                self.model = None
