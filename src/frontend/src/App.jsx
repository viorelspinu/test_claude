import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import './App.css'

// Context providers
import { TodoProvider } from './context/TodoContext'

// Layout components
import Header from './components/layout/Header'
import Footer from './components/layout/Footer'

// Main pages
import TodoPage from './components/todo/TodoPage'

function App() {
  return (
    <TodoProvider>
      <Router>
        <div className="app">
          <Header />
          <main className="main-content">
            <Routes>
              <Route path="/" element={<TodoPage />} />
              <Route path="/todos" element={<TodoPage />} />
            </Routes>
          </main>
          <Footer />
        </div>
      </Router>
    </TodoProvider>
  )
}

export default App
