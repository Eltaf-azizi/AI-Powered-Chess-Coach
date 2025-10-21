import React from "react";
import { Link } from "react-router-dom";



export default function Header() {
  return (
    <header className="bg-indigo-600 text-white p-4 flex justify-between items-center shadow">
      <h1 className="text-xl font-semibold">AI-Powered Chess Coach</h1>
      <nav className="space-x-4">
        <Link to="/" className="hover:text-gray-200">Home</Link>
        <Link to="/game" className="hover:text-gray-200">Play</Link>
        <Link to="/dashboard" className="hover:text-gray-200">Dashboard</Link>
        <Link to="/settings" className="hover:text-gray-200">Settings</Link>
      </nav>
    </header>
  );
}
