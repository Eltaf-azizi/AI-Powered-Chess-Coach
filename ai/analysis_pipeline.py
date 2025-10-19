# ai/analysis_pipeline.py
"""
High-level analysis pipeline that combines evaluator + recommender + feedback generator
and returns a single dict payload suitable for the backend API responses.
"""

from .evaluator import Evaluator
from .recommender import Recommender
from .feedback_generator import FeedbackGenerator



class AnalysisPipeline:
    def __init__(self, engine_service=None, ai_config: dict = None):
        self.evaluator = Evaluator(engine_service, ai_config or {})
        self.recommender = Recommender(self.evaluator, ai_config or {})
        self.feedback_gen = FeedbackGenerator()


    def analyze(self, board, last_move=None):
        eval_cp = self.evaluator.evaluate_board(board)
        suggestions = self.recommender.suggest_moves(board)
        feedback = self.feedback_gen.generate_feedback(board, last_move=last_move, eval_score=eval_cp, suggestions=suggestions)
        return {
            "eval": eval_cp,
            "suggestions": suggestions,
            "feedback": feedback
        }
        