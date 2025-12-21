import React, { useState, useEffect } from 'react';
import './TaskForm.css';

const TaskForm = ({ task, onSubmit, onCancel }) => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    is_completed: false
  });

  useEffect(() => {
    if (task) {
      setFormData({
        title: task.title || '',
        description: task.description || '',
        is_completed: task.is_completed || false
      });
    }
  }, [task]);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (formData.title.trim()) {
      onSubmit(formData);
      if (!task) {
        setFormData({ title: '', description: '', is_completed: false });
      }
    }
  };

  return (
    <div className="task-form-overlay">
      <div className="task-form-card">
        <div className="form-header">
          <h3>{task ? 'Редактировать задачу' : 'Новая задача'}</h3>
          <button onClick={onCancel} className="close-btn">×</button>
        </div>
        
        <form onSubmit={handleSubmit} className="task-form">
          <div className="form-group">
            <label htmlFor="title">Название задачи *</label>
            <input
              type="text"
              id="title"
              name="title"
              value={formData.title}
              onChange={handleChange}
              placeholder="Введите название задачи"
              required
              autoFocus
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="description">Описание (необязательно)</label>
            <textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              placeholder="Добавьте описание задачи"
              rows="4"
            />
          </div>
          
          <div className="form-group checkbox-group">
            <input
              type="checkbox"
              id="is_completed"
              name="is_completed"
              checked={formData.is_completed}
              onChange={handleChange}
            />
            <label htmlFor="is_completed">
              Задача выполнена
            </label>
          </div>
          
          <div className="form-actions">
            <button type="button" onClick={onCancel} className="cancel-btn">
              Отмена
            </button>
            <button type="submit" className="submit-btn">
              {task ? 'Сохранить изменения' : 'Создать задачу'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default TaskForm;