# ai/feedback_generator.py
"""
Generates human-friendly feedback paragraphs for players based on:
- last move
- evaluation score
- suggestions

This component is intentionally simple and rule-driven to produce actionable hints.
"""

import chess


class FeedbackGenerator:
    def __init__(self, style: str = "friendly"):
        self.style = style

    def generate_feedback(self, board: chess.Board, last_move: str = None, eval_score: float = None, suggestions: list = None):
        """
        Returns a short paragraph of feedback.
        - board: current board AFTER last_move
        - last_move: UCI string of the last move (optional)
        - eval_score: centipawn evaluation (optional)
        - suggestions: list of suggestions from recommender (optional)
        """
        parts = []

        # Comment on last move
        if last_move:
            try:
                mv = chess.Move.from_uci(last_move)
            except Exception:
                mv = None
