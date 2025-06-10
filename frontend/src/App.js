import React, { useState, useEffect } from 'react';
import './App.css';

// Import core components (will be created next)
// import TaskList from './components/Task/TaskList';
// import TaskForm from './components/Task/TaskForm';

const App = () => {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Mock data for initial development
  const mockTasks = [
    {
      id: 1,
      title: "Complete project setup",
      description: "Set up React app structure and basic components",
      priority: "High",
      completed: false,
      created_at: "2024-12-06T10:00:00Z",
      updated_at: "2024-12-06T10:00:00Z",
      completed_at: null
    },
    {
      id: 2,
      title: "Implement API integration",
      description: "Connect frontend with Flask backend API",
      priority: "Medium",
      completed: false,
      created_at: "2024-12-06T11:00:00Z",
      updated_at: "2024-12-06T11:00:00Z",
      completed_at: null
    }
  ];

  useEffect(() => {
    // Initialize with mock data for now
    setTasks(mockTasks);
  }, []);

  return (
    <div className="app">
      <header className="app-header">
        <h1>Todo List Application</h1>
        <div className="task-stats">
          <span>Total: {tasks.length}</span>
          <span>Completed: {tasks.filter(task => task.completed).length}</span>
          <span>Remaining: {tasks.filter(task => !task.completed).length}</span>
        </div>
      </header>

      <main className="app-main">
        <div className="app-content">
          {/* Task creation form will go here */}
          <section className="task-form-section">
            <h2>Add New Task</h2>
            {/* <TaskForm onTaskCreate={handleTaskCreate} /> */}
            <div className="placeholder">TaskForm component will be implemented next</div>
          </section>

          {/* Task list will go here */}
          <section className="task-list-section">
            <h2>Tasks</h2>
            {loading && <div className="loading">Loading tasks...</div>}
            {error && <div className="error">Error: {error}</div>}
            {/* <TaskList tasks={tasks} onTaskUpdate={handleTaskUpdate} onTaskDelete={handleTaskDelete} /> */}
            <div className="placeholder">TaskList component will be implemented next</div>
            
            {/* Mock task display for now */}
            <div className="mock-task-list">
              {tasks.map(task => (
                <div key={task.id} className={`mock-task-item ${task.completed ? 'completed' : ''}`}>
                  <h3>{task.title}</h3>
                  <p>{task.description}</p>
                  <span className={`priority ${task.priority.toLowerCase()}`}>{task.priority}</span>
                  <span className="status">{task.completed ? 'Completed' : 'Pending'}</span>
                </div>
              ))}
            </div>
          </section>
        </div>
      </main>

      <footer className="app-footer">
        <p>Todo List App - React + Flask</p>
      </footer>
    </div>
  );
};

export default App;