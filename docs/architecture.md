# Architecture

## Overview
The system has three layers:
1. **Frontend (React)** — UI for gameplay and display of AI tips.
2. **Backend (FastAPI)** — game state, validation, persistence, and AI service glue.
3. **AI (Python)** — evaluator, recommender, and feedback generator. Models live in `models/`.

## Flow
- Player performs action in frontend -> sends FEN or move UCI to backend.
- Backend validates and persists move -> calls AI service.
- AI service uses Stockfish (if installed) or ML models for evaluation, recommends moves, and generates feedback.
- Backend returns JSON analysis -> frontend displays it.

## Storage
- SQLite for MVP (`backend/database/db.sqlite3`). Models persisted via `joblib` in `models/`.
