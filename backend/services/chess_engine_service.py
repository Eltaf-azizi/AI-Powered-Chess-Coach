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
        if self.engine_path and os.path.exists(self.engine_path):
            try:
                self.engine = chess.engine.SimpleEngine.popen_uci(self.engine_path)
            except Exception as e:
                print(f"[ChessEngineService] Could not start engine at {self.engine_path}: {e}")
                self.engine = None
        else:
            # no engine available; remain None -> fallbacks used
            pass

    def analyze(self, board: chess.Board, limit=0.1):
        """
        Return engine analysis info or None if no engine present.
        `limit` is seconds (float).
        """
        if not self.engine:
            return None

