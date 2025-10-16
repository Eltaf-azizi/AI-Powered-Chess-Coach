# ai/__init__.py
"""
AI package for AI-Powered Chess Coach.

Exports:
- Evaluator: hybrid evaluator that uses Stockfish if available, else ML model fallback.
- Recommender: suggests moves + strategy comments (uses ML model when available).
- FeedbackGenerator: produces human-friendly textual tips.
- utils: feature extraction helpers.
- AnalysisPipeline: convenient wrapper for full analysis (eval + suggestions + feedback).
"""
from .evaluator import Evaluator
from .recommender import Recommender
from .feedback_generator import FeedbackGenerator
from .utils import encode_board_features, move_type_label
from .analysis_pipeline import AnalysisPipeline

__all__ = ["Evaluator", "Recommender", "FeedbackGenerator", "encode_board_features", "AnalysisPipeline", "move_type_label"]
