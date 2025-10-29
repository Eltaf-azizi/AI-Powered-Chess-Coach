# scripts/evaluate_model.py
import os
import joblib
import chess
from ai.evaluator import Evaluator
from backend.services.chess_engine_service import ChessEngineService


MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "models", "move_evaluator.pkl")


def quick_eval(fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
    engine = ChessEngineService({})
    ev = Evaluator(engine_service=engine)
    board = chess.Board(fen)
    print("Eval:", ev.evaluate_board(board))


if __name__ == "__main__":
    quick_eval()
