import React from 'react'
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Files from './pages/Files.jsx'
import {MenuProvider} from "./contexts/MenuContext.jsx";

function App() {
  return (
      <MenuProvider>
          <Router>
            <Routes>
                    <Route path="/" element={<Files />} />
            </Routes>
          </Router>
      </MenuProvider>
  )
}

export default App
