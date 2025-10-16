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
    for pt in piece_types:
        material.append(len(board.pieces(pt, chess.WHITE)))
    for pt in piece_types:
        material.append(len(board.pieces(pt, chess.BLACK)))

    mobility = [len(list(board.legal_moves))]

    king_in_check = [1 if board.is_check() else 0]

    castling = [
        1 if board.has_kingside_castling_rights(chess.WHITE) else 0,
        1 if board.has_queenside_castling_rights(chess.WHITE) else 0,
        1 if board.has_kingside_castling_rights(chess.BLACK) else 0,
        1 if board.has_queenside_castling_rights(chess.BLACK) else 0
    ]

    # piece-square sums (pawn and knight) for each color
    def pst_sum(pt, color):
        arr = PST.get(pt)
        if arr is None:
            return 0.0
        s = 0.0
        for sq in board.pieces(pt, color):
            # pst is indexed from white's perspective; if black, mirror
            idx = sq if color == chess.WHITE else chess.square_mirror(sq)
            s += arr[idx]
        return s

    pawn_pst = [pst_sum(chess.PAWN, chess.WHITE), pst_sum(chess.PAWN, chess.BLACK)]
    knight_pst = [pst_sum(chess.KNIGHT, chess.WHITE), pst_sum(chess.KNIGHT, chess.BLACK)]

    features = material + mobility + king_in_check + castling + pawn_pst + knight_pst
    return np.array(features, dtype=float)


def move_type_label(board: chess.Board, move: chess.Move) -> str:
    """
    Simple heuristic to label a move:
    - capture: if move captures
    - castle: castling move
    - develop: moving knight or bishop from home rank in opening phase
    - center: move to d4,e4,d5,e5
    - other: fallback
    """
    try:
        if board.is_capture(move):
            return "capture"
    except Exception:
        pass

    # castle
    if board.is_castling(move):
        return "castle"

    # center
    center = [chess.E4, chess.D4, chess.E5, chess.D5]
    if move.to_square in center:
        return "center"

    # develop: moving N/B from back rank within first 12 fullmoves
    from_piece = board.piece_at(move.from_square)
    if board.fullmove_number <= 12 and from_piece and from_piece.piece_type in (chess.KNIGHT, chess.BISHOP):
        # if it's on rank 1 or 8 (back rank) and moves off back rank it's development
        rank = chess.square_rank(move.from_square)
        if rank in (0, 7):
            return "develop"

    return "other"

def label_to_int(label: str) -> int:
    return LABELS.index(label) if label in LABELS else LABELS.index("other")

def int_to_label(i: int) -> str:
    if 0 <= i < len(LABELS):
        return LABELS[i]
    return "other"