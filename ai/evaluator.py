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

    def evaluate_board(self, board: chess.Board) -> float:
        """
        Returns centipawn score from White's perspective (positive = White advantage).
        Priority:
         1) Use engine if available.
         2) Use ML model if loaded.
         3) Fallback material heuristic.
        """
        # 1) engine
        if self.engine_service:
            try:
                info = self.engine_service.analyze(board, limit=self.config.get("engine_time", 0.05))
                if info and "score" in info:
                    score = info["score"]
                    # convert to centipawns
                    if score.is_mate():
                        mate = score.white().mate()
                        return 100000.0 if mate and mate > 0 else -100000.0
                    cp = score.white().cp
                    return float(cp) if cp is not None else 0.0
            except Exception:
                pass
                
        # 2) ML model
        if self.model is not None:
            try:
                feat = encode_board_features(board).reshape(1, -1)
                pred = self.model.predict(feat)
                # model returns rough centipawn value
                return float(pred[0])
            except Exception as e:
                print("[Evaluator] model prediction failed:", e)

        # 3) fallback material eval
        return float(self._material_eval(board))

    def _material_eval(self, board: chess.Board) -> int:
        # simple piece-value sum (centipawn style)
        values = {
            chess.PAWN: 100,
            chess.KNIGHT: 320,
            chess.BISHOP: 330,
            chess.ROOK: 500,
            chess.QUEEN: 900,
            chess.KING: 20000
        }
        score = 0
        for ptype, val in values.items():
            score += len(board.pieces(ptype, chess.WHITE)) * val
            score -= len(board.pieces(ptype, chess.BLACK)) * val
        # small mobility factor
        score += int(0.1 * len(list(board.legal_moves)))
        return score
