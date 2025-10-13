"""
AI service that glues evaluator, recommender and feedback generator.
For Part 1 we provide a lightweight default evaluator and recommender inline,
so the backend works without waiting for deep ML code in Part 2.
"""
import chess
from .. import db as db_module  # not used here; kept for possible DB interaction
from .. import __name__ as pkgname
import os


# Import ai modules from top-level ai/ if present. Fall back to basic internal logic.
try:
    from ...ai.evaluator import Evaluator
    from ...ai.recommender import Recommender
    from ...ai.feedback_generator import FeedbackGenerator
    ai_available = True
except Exception:
    ai_available = False

# Minimal fallback evaluator/recommender/feedback if ai package isn't present
class SimpleEvaluator:
    PIECE_VALUES = {
        chess.PAWN: 100,
        chess.KNIGHT: 320,
        chess.BISHOP: 330,
        chess.ROOK: 500,
        chess.QUEEN: 900,
        chess.KING: 20000
    }