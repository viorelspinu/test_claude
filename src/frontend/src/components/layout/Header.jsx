import React from 'react'
import { Link } from 'react-router-dom'

const Header = () => {
  return (
    <header className="app-header">
      <div className="header-content">
        <h1 className="app-title">
          <Link to="/">Todo App</Link>
        </h1>
        <nav className="app-nav">
          <Link to="/todos" className="nav-link">Todos</Link>
        </nav>
      </div>
    </header>
  )
}

export default Header