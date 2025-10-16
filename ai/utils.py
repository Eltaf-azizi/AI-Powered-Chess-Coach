# ai/utils.py
"""
Helper utilities for feature extraction and simple heuristics.

Functions:
- encode_board_features(board): returns numpy vector representing features for ML.
- move_type_label(board, move): returns string label: 'capture','develop','center','castle','other'
- label_to_int / int_to_label: helpers for classifier mapping
"""

import chess
import numpy as np

LABELS = ["capture", "develop", "center", "castle", "other"]

# basic piece-square tables (simplified) for small positional signal
# Using tiny PSTs for pawns and knights to include positional info
PST = {
    
}
