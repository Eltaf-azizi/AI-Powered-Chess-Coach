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
