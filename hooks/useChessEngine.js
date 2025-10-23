import { useState } from "react";
import axios from "axios";



export default function useChessEngine(game) {
  const [boardPosition, setBoardPosition] = useState(game.fen());
  const [moves, setMoves] = useState([]);
  const [feedback, setFeedback] = useState("");
  const [strategy, setStrategy] = useState("");


  const handleMove = async (source, target) => {
    const move = game.move({ from: source, to: target, promotion: "q" });


    if (move === null) return false;
    setBoardPosition(game.fen());
    setMoves([...moves, move.san]);



    // Call backend for analysis
    try {
      const res = await axios.post("http://localhost:5000/api/ai/analyze", {
        fen: game.fen(),
      });
      setFeedback(res.data.feedback);
      setStrategy(res.data.strategy);
    } catch (err) {
      console.error(err);
    }


    return true;
  };
  

  return { boardPosition, moves, feedback, strategy, handleMove };
}
