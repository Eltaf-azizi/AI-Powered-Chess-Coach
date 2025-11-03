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

### 5. Train AI Models (if you haven’t yet)
```
python models/train_model.py
```

This creates move_evaluator.pkl and strategy_recommender.pkl in the models/ folder.

### 6. Start the Backend
```
uvicorn backend.app:app --reload
```

Backend runs at http://127.0.0.1:8000

### 7. Start the Frontend
```
cd frontend
npm install
npm run dev
```

Frontend runs at http://localhost:5173
 (or as printed in terminal)


## 🧩 API Reference

|Endpoint |	Method |	Description |
|--------|--------|--------------|
|/	GET |	Health | check |
|/game/start |	POST |	Start a new game|
|/game/move |	POST |	Submit a move and get AI analysis|
|/game/state/{id} |	GET |	Get current game state|
|/ai/analyze |	POST |	Analyze arbitrary FEN position|

See docs/api_reference.md
 for complete payloads.

## 💻 Tech Stack
### Backend

 - FastAPI – RESTful API framework

 - python-chess – Chess rules and move validation

 - SQLite – Lightweight game storage

 - Scikit-learn – ML models for move evaluation

### Frontend

 - React + Vite – Fast modern web app

 - react-chessboard – Chess UI component

 - Axios – API communication

### AI / ML

 - RandomForest models for evaluation and strategy classification

 - Custom feature extraction from chessboard positions

 - Optional integration with Stockfish for hybrid analysis


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


## 📈 Example Output

When a player moves:
```
{
  "analysis": {
    "eval": 0.54,
    "suggestions": ["Nf3", "Bc4", "d3"],
    "feedback": "Good central control. Develop your kingside bishop next."
  }
}
```

## 🧪 Testing

Run all backend tests:
```
pytest -q
```

Frontend (if using Jest/Vitest):
```
npm test
```

## 📄 Documentation

 - docs/architecture.md : system design overview
 - docs/api_reference.md : endpoints and usage
 - docs/model_notes.md : AI and ML details
 - docs/ui_wireframes/ : mockups and visual references


## 🌍 Future Improvements

 - Add user authentication and game history
 - Train deeper models using large PGN datasets
 - Integrate reinforcement learning for adaptive coaching
 - Real-time multiplayer with socket-based updates
 - Personalized learning plans based on user patterns


## 🧑‍💻 Contributing

Contributions are welcome!
If you find a bug or have an idea for improvement:

 1. Fork the repository
 2. Create a new branch
 3. Commit your changes
 4. Submit a pull request

Please make sure your code follows the existing structure and includes tests when possible.

## 💬 Author

Developer: Eltaf Azizi

AI & Full-Stack Developer passionate about combining game design and machine learning.
