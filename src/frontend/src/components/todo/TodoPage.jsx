import React from 'react'
import TodoForm from './TodoForm'
import TodoList from './TodoList'
import TodoStats from './TodoStats'

const TodoPage = () => {
  const handleFormSubmit = (newTodo) => {
    console.log('New todo created:', newTodo)
  }

  const handleFormCancel = () => {
    console.log('Form cancelled')
  }

  return (
    <div className="todo-page">
      <div className="page-header">
        <h2>My Todos</h2>
        <p>Manage your tasks efficiently</p>
      </div>
      
      <div className="todo-container">
        <div className="todo-form-section">
          <TodoForm 
            onSubmit={handleFormSubmit}
            onCancel={handleFormCancel}
          />
        </div>
        
        <div className="todo-stats-section">
          <TodoStats />
        </div>
        
        <div className="todo-list-section">
          <TodoList />
        </div>
      </div>
    </div>
  )
}

export default TodoPage