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


class SimpleFeedback:
    def generate(self, board: chess.Board, last_move=None, eval_score=None):
        notes = []
        if last_move:
            mv = None
            try:
                mv = chess.Move.from_uci(last_move)
            except:
                mv = None
            if mv and board.is_capture(mv):
                notes.append("You captured a piece. Check for recaptures.")
        if eval_score is not None:
            if eval_score > 300:
                notes.append("You're ahead — trade pieces and consolidate.")
            elif eval_score < -300:
                notes.append("You're behind — look for defense and simplifications.")
            else:
                notes.append("Balanced position — improve piece activity.")
        if not notes:
            notes.append("Think about center control and piece development.")
        return " ".join(notes)


class AIService:
    def __init__(self, engine_service, ai_config: dict=None):
        self.engine_service = engine_service
        self.ai_config = ai_config or {}
        # if ai/ package exists use it
        if ai_available:
            # Evaluator takes engine_service, config
            self.evaluator = Evaluator(engine_service, self.ai_config)
            self.recommender = Recommender(self.evaluator, self.ai_config)
            self.feedback = FeedbackGenerator()
        else:
            self.evaluator = SimpleEvaluator()
            self.recommender = SimpleRecommender(self.evaluator, suggestion_count=self.ai_config.get('suggestion_count', 3))
            self.feedback = SimpleFeedback()


    def analyze_position(self, board: chess.Board, last_move: str = None):
        # Try engine first
        engine_info = self.engine_service.analyze(board, limit=self.ai_config.get('engine_time', 0.05))
        eval_cp = None
        engine_best = None
        if engine_info:
            score = engine_info.get("score")
            if score:
                try:
                    if score.is_mate():
                        eval_cp = 100000.0 if score.white().mate() > 0 else -100000.0
                    else:
                        eval_cp = float(score.white().cp)
                except Exception:
                    eval_cp = None
            try:
                mv = self.engine_service.bestmove(board, depth=self.ai_config.get('engine_depth', 12))
                if mv:
                    engine_best = mv.uci()
            except Exception:
                engine_best = None


        # If top-level ai module exists use it, else fallback
        if ai_available:
            eval_cp = self.evaluator.evaluate_board(board) if eval_cp is None else eval_cp
            suggestions = self.recommender.suggest_moves(board)
            feedback = self.feedback.generate_feedback(board, last_move=last_move, eval_score=eval_cp)
        else:
            if eval_cp is None:
                eval_cp = self.evaluator.material(board)
            suggestions = self.recommender.suggestions(board)
            # include engine_best if present
            if engine_best and not any(s['uci'] == engine_best for s in suggestions):
                suggestions.insert(0, {"uci": engine_best, "san": engine_best, "score": None, "comment": "Engine best move"})
                suggestions = suggestions[:self.ai_config.get('suggestion_count', 3)]
            feedback = self.feedback.generate(board, last_move=last_move, eval_score=eval_cp)

        return {
            "eval": eval_cp,
            "suggestions": suggestions,
            "feedback": feedback
        }