# API Reference

Base URL: `http://127.0.0.1:8000`

## `GET /`
Health check.

## `POST /game/start`
Start new game.
**Body**
```json
{ "mode": "local", "white_player": "human", "black_player": "ai" }
