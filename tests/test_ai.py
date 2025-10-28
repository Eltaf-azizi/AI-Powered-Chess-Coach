# tests/test_ai.py
import chess
from ai.utils import encode_board_features, move_type_label
from ai.evaluator import Evaluator


def test_encode_features():
    board = chess.Board()
    feats = encode_board_features(board)
    assert feats.shape[0] > 0
    assert all([isinstance(x, float) for x in feats])


def test_move_type_label_opening():
    board = chess.Board()
    mv = chess.Move.from_uci("g1f3")
    label = move_type_label(board, mv)
    assert label in ("develop", "other", "center", "capture", "castle")


def test_evaluator_fallback():
    ev = Evaluator(engine_service=None, ai_config={})
    board = chess.Board()
    val = ev.evaluate_board(board)
    assert isinstance(val, float)
