import React from 'react';
import TodoItem from './TodoItem';
import './TodoList.css';

const TodoList = ({ todos, filter, onToggle, onDelete, onEdit }) => {
  // Filter todos based on current filter
  const filteredTodos = todos.filter(todo => {
    switch (filter) {
      case 'active':
        return !todo.completed;
      case 'completed':
        return todo.completed;
      default:
        return true;
    }
  });

  if (filteredTodos.length === 0) {
    return (
      <div className="todo-list empty">
        <div className="empty-state">
          <h3>No todos found</h3>
          <p>
            {filter === 'active' && 'No active todos. Great job!'}
            {filter === 'completed' && 'No completed todos yet.'}
            {filter === 'all' && 'No todos yet. Add your first todo above!'}
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="todo-list">
      <div className="list-header">
        <h3>
          {filter === 'active' && 'Active Todos'}
          {filter === 'completed' && 'Completed Todos'}
          {filter === 'all' && 'All Todos'}
          <span className="count">({filteredTodos.length})</span>
        </h3>
      </div>
      
      <div className="todos-container">
        {filteredTodos.map(todo => (
          <TodoItem
            key={todo.id}
            todo={todo}
            onToggle={onToggle}
            onDelete={onDelete}
            onEdit={onEdit}
          />
        ))}
      </div>
    </div>
  );
};

export default TodoList;