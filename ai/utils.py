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
    chess.PAWN: [
        0,0,0,0,0,0,0,0,
        5,5,5,5,5,5,5,5,
        1,1,2,3,3,2,1,1,
        0.5,0.5,1,2.5,2.5,1,0.5,0.5,
        0,0,0,2,2,0,0,0,
        0.5,-0.5,-1,0,0,-1,-0.5,0.5,
        0.5,1,1,-2,-2,1,1,0.5,
        0,0,0,0,0,0,0,0
    ],
    chess.KNIGHT: [
        -5,-4,-3,-3,-3,-3,-4,-5,
        -4,-2,0,0,0,0,-2,-4,
        -3,0,1.5,2,2,1.5,0,-3,
        -3,0.5,2,2.5,2.5,2,0.5,-3,
        -3,0,2.5,2.5,2.5,2,0,-3,
        -3,0.5,1.5,2,2,1.5,0.5,-3,
        -4,-2,0,0.5,0.5,0,-2,-4,
        -5,-4,-3,-3,-3,-3,-4,-5
    ]
}


def encode_board_features(board: chess.Board):
    """
    Encode board into numeric feature vector:
    - material counts (6 values white - black)
    - mobility (legal moves count)
    - king safety (is in check flag)
    - castling rights (4 flags)
    - piece-square sums for pawns and knights for both colors
    """
    # material counts per piece type (order: P,N,B,R,Q,K)
    piece_types = [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING]
    material = []