import React from "react";



export default function Footer() {
  return (
    <footer className="bg-gray-200 text-center text-sm text-gray-600 py-3">
      © {new Date().getFullYear()} AI-Powered Chess Coach. Built with ❤️ for learning.
    </footer>
  );
}
