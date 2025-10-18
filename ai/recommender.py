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