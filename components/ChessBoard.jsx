import React, { useState } from "react";
import { Chessboard } from "react-chessboard";
import { Chess } from "chess.js";
import useChessEngine from "../hooks/useChessEngine";


export default function ChessBoard() {
  const [game] = useState(new Chess());
  const { handleMove, boardPosition } = useChessEngine(game);

  return (
    <div className="flex flex-col items-center">
      <Chessboard
        id="AIChessBoard"
        position={boardPosition}
        onPieceDrop={(source, target) => handleMove(source, target)}
        boardWidth={480}
      />
    </div>
  );
}
