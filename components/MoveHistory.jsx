import React from "react";



export default function MoveHistory({ moves }) {
  return (
    <div className="bg-white border rounded-lg p-4 shadow">
      <h3 className="font-semibold mb-2">Move History</h3>
      <ol className="list-decimal ml-5 text-gray-700">
        {moves.map((move, i) => (
          <li key={i}>{move}</li>
        ))}
      </ol>
    </div>
  );
}
