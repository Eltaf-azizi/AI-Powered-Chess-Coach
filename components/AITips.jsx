import React from "react";


export default function AITips({ feedback }) {
  if (!feedback) return null;

  return (
    <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 my-4">
      <h3 className="text-lg font-semibold mb-2">AI Coaching Tips</h3>
      <p className="text-gray-700">{feedback}</p>
    </div>
  );
}
