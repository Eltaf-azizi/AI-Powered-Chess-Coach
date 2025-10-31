<h1 align="center">♟️ AI-Powered Chess Coach</h1>

**AI-Powered Chess Coach** is a full-stack application that allows users to play chess online while receiving real-time feedback and strategy suggestions from an AI system.

- **Frontend (React):** Interactive online chessboard and analysis dashboard.  
- **Backend (FastAPI):** Game logic, user sessions, and communication between frontend and AI.  
- **AI Engine (Python + ML):** Evaluates moves, recommends strategies, and generates coaching tips.


## 🚀 Overview

**AI-Powered Chess Coach** is a full-stack application that allows users to play chess online while receiving real-time feedback and strategy suggestions from an AI system.

- **Frontend (React):** Interactive online chessboard and analysis dashboard.  
- **Backend (FastAPI):** Game logic, user sessions, and communication between frontend and AI.  
- **AI Engine (Python + ML):** Evaluates moves, recommends strategies, and generates coaching tips.



## 🎯 Goal

> **Goal:** Expand game AI logic with tips & ML  
> **Output:** Online chess game → AI analyzes moves and suggests strategies

The app doesn’t just show good or bad moves. It explains *why* a move is effective and what strategy it supports (e.g., development, control of center, defense, or attack).


## 🧠 Core Features

| Feature | Description |
|----------|--------------|
| ♟️ **Interactive Chessboard** | Play against a friend or AI directly in your browser |
| 🔍 **AI Move Analysis** | Each move is evaluated using ML and Stockfish |
| 💡 **Strategy Suggestions** | The AI explains patterns and proposes improvements |
| 📊 **Performance Feedback** | Tracks your game patterns and gives learning insights |
| 🧩 **Openings Recognition** | Detects known openings and explains their principles |
| 🧪 **Modular Architecture** | Backend, AI, and frontend work independently but communicate through APIs |


## ⚙️ Installation and Setup

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/ai-powered-chess-coach.git
cd ai-powered-chess-coach
```


### 2. Create and Activate Virtual Environment
```
python -m venv venv
source venv/bin/activate    # on macOS / Linux
venv\Scripts\activate       # on Windows
```

### 3. Install Backend Dependencies
```
pip install -r requirements.txt
```

### 4. Run Database Setup (Optional)
```
python scripts/setup_db.py
```

## 🧠 How the AI Works
### 1. Feature Extraction
  Each position is turned into numerical features: material, mobility, king safety, etc.

### 2. Evaluation Model
  A trained RandomForestRegressor predicts the strength of a position.

### 3. Strategy Recommender
  A classifier predicts the “type” of move (development, capture, defense, etc.)

### 4. Feedback Generator
  Converts AI evaluations into natural-language advice like:

   “Consider developing your minor pieces before pushing pawns further.”
