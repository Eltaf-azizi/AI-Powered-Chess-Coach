import React from "react";
import ChessBoard from "../components/ChessBoard";
import AITips from "../components/AITips";
import MoveHistory from "../components/MoveHistory";
import StrategyPanel from "../components/StrategyPanel";
import useChessEngine from "../hooks/useChessEngine";
import { Chess } from "chess.js";


export default function Game() {
  const [game] = React.useState(new Chess());
  const { boardPosition, moves, feedback, strategy, handleMove } = useChessEngine(game);

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      <ChessBoard />
      <div>
        <MoveHistory moves={moves} />
        <AITips feedback={feedback} />
        <StrategyPanel strategy={strategy} />
      </div>
    </div>
  );
}
