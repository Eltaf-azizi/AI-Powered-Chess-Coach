import chess
import chess.engine
import os, shutil

class ChessEngineService:
    def __init__(self, engine_config: dict=None):
        self.engine_path = ""
        if engine_config:
            self.engine_path = engine_config.get('stockfish_path', "") or ""
        # also allow env var
        if not self.engine_path:
            self.engine_path = os.environ.get("STOCKFISH_PATH", "")
        self.engine = None