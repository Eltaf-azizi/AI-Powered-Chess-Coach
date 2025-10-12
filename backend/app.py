from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os, yaml, uvicorn
from .routes import game_routes, ai_routes, user_routes
from .database import models as db_models

ROOT = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(ROOT, "..", "config", "settings.yaml")
with open(CONFIG_PATH, "r") as f:
    CONFIG = yaml.safe_load(f)

app = FastAPI(title="AI-Powered Chess Coach API", version="1.0")

# allow local frontend for development; lock down in prod
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)


# include routers
app.include_router(game_routes.router, prefix="/game", tags=["game"])
app.include_router(ai_routes.router, prefix="/ai", tags=["ai"])
app.include_router(user_routes.router, prefix="/user", tags=["user"])

# ensure DB file exists / create tables
db_models.init_db()

@app.get("/")
def root():
    return {"ok": True, "service": "AI-Powered Chess Coach Backend"}

if __name__ == "__main__":
    uvicorn.run("backend.app:app", host=CONFIG['server']['host'], port=CONFIG['server']['port'], reload=CONFIG['server'].get('debug', True))