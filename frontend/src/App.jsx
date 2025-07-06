import React from 'react'
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Files from './pages/Files.jsx'

function App() {
  return (
      <Router>
        <Routes>
          <Route path="/" element={<Files />} />
        </Routes>
      </Router>
  )
}

export default App
