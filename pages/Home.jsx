
import React from "react";
import { Link } from "react-router-dom";


export default function Home() {
  return (
    <div className="text-center py-20">
      <h2 className="text-3xl font-bold mb-4">Welcome to AI-Powered Chess Coach</h2>
      <p className="text-gray-700 mb-8">
        Play chess, improve your strategy, and get real-time coaching from AI.
      </p>
      <Link to="/game" className="bg-indigo-600 text-white px-6 py-3 rounded hover:bg-indigo-700">
        Start Playing
      </Link>
    </div>
  );
}

