from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import chess
from ..services.chess_engine_service import ChessEngineService
from ..services.ai_service import AIService
import os, yaml

ROOT = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(ROOT, "..", "..", "config", "settings.yaml")
with open(CONFIG_PATH, "r") as f:
    CONFIG = yaml.safe_load(f)

router = APIRouter()
engine_service = ChessEngineService(CONFIG.get('engine', {}))
ai_service = AIService(engine_service, CONFIG.get('ai', {}))

class AnalyzeReq(BaseModel):
    fen: str
    last_move: str = None
