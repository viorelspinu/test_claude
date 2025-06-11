import React from 'react';
import './TodoFilter.css';

const TodoFilter = ({ currentFilter, onFilterChange, todoCounts }) => {
  const filters = [
    { key: 'all', label: 'All', count: todoCounts.total },
    { key: 'active', label: 'Active', count: todoCounts.active },
    { key: 'completed', label: 'Completed', count: todoCounts.completed }
  ];

  return (
    <div className="todo-filter">
      <h3>Filter Todos</h3>
      <div className="filter-buttons">
        {filters.map(filter => (
          <button
            key={filter.key}
            className={`filter-btn ${currentFilter === filter.key ? 'active' : ''}`}
            onClick={() => onFilterChange(filter.key)}
          >
            {filter.label}
            <span className="count">({filter.count})</span>
          </button>
        ))}
      </div>
    </div>
  );
};

export default TodoFilter;