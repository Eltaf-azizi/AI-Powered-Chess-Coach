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
