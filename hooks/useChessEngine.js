import { useState } from "react";
import axios from "axios";



export default function useChessEngine(game) {
  const [boardPosition, setBoardPosition] = useState(game.fen());
  const [moves, setMoves] = useState([]);
  const [feedback, setFeedback] = useState("");
  const [strategy, setStrategy] = useState("");


  const handleMove = async (source, target) => {
    const move = game.move({ from: source, to: target, promotion: "q" });

