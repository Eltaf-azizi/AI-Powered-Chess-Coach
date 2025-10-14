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

    def material(self, board: chess.Board):
        score = 0
        for ptype,val in self.PIECE_VALUES.items():
            score += len(board.pieces(ptype, chess.WHITE)) * val
            score -= len(board.pieces(ptype, chess.BLACK)) * val
        score += int(0.1 * len(list(board.legal_moves)))
        return float(score)

class SimpleRecommender:
    def __init__(self, evaluator, suggestion_count=3):
        self.evaluator = evaluator
        self.count = suggestion_count

    def suggestions(self, board: chess.Board):
        # shallow score of legal moves: push, evaluate material, pop
        moves = []
        for mv in list(board.legal_moves):
            board.push(mv)
            score = self.evaluator.material(board)
            board.pop()
            moves.append((mv.uci(), score))
        moves.sort(key=lambda x: x[1], reverse=(board.turn==chess.WHITE))
        top = moves[:self.count]
        out = []
        for uci, score in top:
            try:
                san = board.san(chess.Move.from_uci(uci))
            except Exception:
                san = uci
            out.append({"uci": uci, "san": san, "score": score, "comment": "Fallback suggestion"})
        return out
