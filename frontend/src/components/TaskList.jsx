import React from 'react';
import './TaskList.css';

const TaskList = ({ tasks, onToggle, onEdit, onDelete }) => {
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('ru-RU', {
      day: 'numeric',
      month: 'short',
      year: 'numeric'
    });
  };

  return (
    <div className="task-list">
      {tasks.map(task => (
        <div key={task.id} className={`task-card ${task.is_completed ? 'completed' : ''}`}>
          <div className="task-main">
            <div className="task-checkbox">
              <input
                type="checkbox"
                checked={task.is_completed}
                onChange={() => onToggle(task.id)}
                id={`task-${task.id}`}
              />
              <label 
                htmlFor={`task-${task.id}`}
                className="custom-checkbox"
              ></label>
            </div>
            
            <div className="task-content">
              <div className="task-header">
                <h3 className="task-title">{task.title}</h3>
                <span className="task-date">
                  {formatDate(task.created_at)}
                </span>
              </div>
              
              {task.description && (
                <p className="task-description">{task.description}</p>
              )}
            </div>
          </div>
          
          <div className="task-actions">
            <button 
              onClick={() => onEdit(task)}
              className="action-btn edit-btn"
            >
              Редактировать
            </button>
            <button 
              onClick={() => onDelete(task.id)}
              className="action-btn delete-btn"
            >
              Удалить
            </button>
          </div>
        </div>
      ))}
    </div>
  );
};

export default TaskList;