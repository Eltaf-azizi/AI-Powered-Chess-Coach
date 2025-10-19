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
            if mv:
                if board.is_capture(mv):
                    parts.append("Nice capture — always check if the opponent has a strong reply.")
                else:
                    parts.append("Consider whether this move improves piece activity or king safety.")

        # Evaluation perspective
        if eval_score is not None:
            # convert to pawn units for readability
            pawns = round(eval_score / 100.0, 2)
            if eval_score > 300:
                parts.append(f"You are ahead by about {pawns} pawns. Simplify and trade pieces when safe.")
            elif eval_score < -300:
                parts.append(f"You are down by about {abs(pawns)} pawns. Look for defensive resources and tactical chances.")
            else:
                parts.append("The position is roughly balanced. Focus on improving piece placement and controlling the center.")

        # Suggest next focus
        if suggestions and len(suggestions) > 0:
            top = suggestions[0]
            parts.append(f"Try the move {top.get('san','(move)')} — {top.get('comment','it improves the position')}.")

        # King safety & tactics reminder
        if board.is_check():
            parts.append("You're in check — prioritize dealing with the check safely.")
        # Length guard
        feedback = " ".join(parts).strip()
        if not feedback:
            feedback = "Try to improve piece activity and look for tactical chances before making a move."
        return feedback
