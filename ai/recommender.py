# ai/recommender.py
"""
Recommender: produce a list of suggested moves with short comments.

Behavior:
- Tries to use engine for best move(s) via engine_service.bestmove
- If ML strategy_recommender exists (models/strategy_recommender.pkl), it will predict move-type
  for candidate moves to give higher-level strategy tags.
- Fallback: use a simple shallow search (material heuristic) and rule-based comments.
"""

import os
import chess
import joblib
from .utils import encode_board_features, move_type_label, label_to_int, int_to_label

MODEL_PATH_DEFAULT = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "models", "strategy_recommender.pkl")

class Recommender:
    def __init__(self, evaluator, ai_config: dict = None, model_path: str = None):
        """
        evaluator: instance of Evaluator (used for scoring candidate moves)
        ai_config: may contain 'suggestion_count'
        """
        self.evaluator = evaluator
        self.config = ai_config or {}
        self.count = int(self.config.get("suggestion_count", 3))
        self.model_path = model_path or MODEL_PATH_DEFAULT
        self.model = None
        self._load_model()

    def _load_model(self):
        if os.path.exists(self.model_path):
            try:
                self.model = joblib.load(self.model_path)
            except Exception as e:
                print(f"[Recommender] Could not load model at {self.model_path}: {e}")
                self.model = None

    def suggest_moves(self, board: chess.Board):
        """
        Return list of suggestions (ordered) of form:
        { uci, san, score (centipawn), strategy_label, comment }
        """