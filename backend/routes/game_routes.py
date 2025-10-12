from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import chess, uuid
from ..services.database_service import DatabaseService
from ..services.chess_engine_service import ChessEngineService
from ..services.ai_service import AIService
import os, yaml

ROOT = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(ROOT, "..", "..", "config", "settings.yaml")
with open(CONFIG_PATH, "r") as f:
    CONFIG = yaml.safe_load(f)

router = APIRouter()

db = DatabaseService()
engine_service = ChessEngineService(CONFIG.get('engine', {}))
ai_service = AIService(engine_service, CONFIG.get('ai', {}))

class StartGameReq(BaseModel):
    mode: str = "local"     # local | ai
    white_player: str = "human"
    black_player: str = "ai"

class MoveReq(BaseModel):
    game_id: str
    uci: str

@router.post("/start")
def start_game(req: StartGameReq):
    game_id = str(uuid.uuid4())
    board = chess.Board()
    db.create_game(game_id=game_id, fen=board.fen(), mode=req.mode, white=req.white_player, black=req.black_player)
    return {"game_id": game_id, "fen": board.fen()}

@router.post("/move")
def make_move(req: MoveReq):
    game = db.get_game(req.game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    board = chess.Board(game['fen'])
    try:
        move = chess.Move.from_uci(req.uci)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid UCI: {e}")
    if move not in board.legal_moves:
        raise HTTPException(status_code=400, detail="Illegal move")
    board.push(move)
    db.add_move(req.game_id, req.uci, board.fen())
    # Run AI analysis: returns evaluation, suggestions, feedback
    analysis = ai_service.analyze_position(board, last_move=req.uci)

    return {
        "fen": board.fen(),
        "moves": db.get_moves(req.game_id),
        "analysis": analysis
    }



@router.get("/state/{game_id}")
def get_state(game_id: str):
    game = db.get_game(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    board = chess.Board(game['fen'])
    analysis = ai_service.analyze_position(board)
    return {
        "game_id": game_id,
        "fen": game['fen'],
        "moves": db.get_moves(game_id),
        "analysis": analysis
    }