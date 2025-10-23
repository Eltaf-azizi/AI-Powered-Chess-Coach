import React from "react";



export default function StrategyPanel({ strategy }) {
  return (
    <div className="bg-indigo-50 border border-indigo-200 rounded-lg p-4 shadow">
      <h3 className="text-lg font-semibold mb-2">Strategy Suggestion</h3>
      <p className="text-gray-700">{strategy || "No suggestion yet"}</p>
    </div>
  );
}
