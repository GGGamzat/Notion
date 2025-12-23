import React, { useState, useEffect } from 'react';
import './Dashboard.css';
import TaskList from './TaskList';
import TaskForm from './TaskForm';

const Dashboard = ({ user, onLogout }) => {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingTask, setEditingTask] = useState(null);

  // const API_BASE_URL = process.env.NODE_ENV === 'development' 
  //     ? 'http://127.0.0.1:8000'  // Для локальной разработки
  //     : '';  // В продакшене - тот же домен

  const API_BASE_URL = process.env.REACT_APP_API_URL || '';

  // const API_BASE_URL = 'http://127.0.0.1:8000';


  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_BASE_URL}/tasks/`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        setTasks(data);
      }
    } catch (error) {
      console.error('Ошибка при загрузке задач:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTask = async (taskData) => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_BASE_URL}/tasks/`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(taskData),
      });

      if (response.ok) {
        const newTask = await response.json();
        setTasks([newTask, ...tasks]);
        setShowForm(false);
      }
    } catch (error) {
      console.error('Ошибка при создании задачи:', error);
    }
  };

  const handleUpdateTask = async (taskId, taskData) => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_BASE_URL}/tasks/${taskId}`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(taskData),
      });

      if (response.ok) {
        const updatedTask = await response.json();
        setTasks(tasks.map(task => 
          task.id === taskId ? updatedTask : task
        ));
        setEditingTask(null);
      }
    } catch (error) {
      console.error('Ошибка при обновлении задачи:', error);
    }
  };

  const handleDeleteTask = async (taskId) => {
    if (!window.confirm('Вы уверены, что хотите удалить эту задачу?')) {
      return;
    }

    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_BASE_URL}/tasks/${taskId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        setTasks(tasks.filter(task => task.id !== taskId));
      }
    } catch (error) {
      console.error('Ошибка при удалении задачи:', error);
    }
  };

  const handleToggleTask = async (taskId) => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_BASE_URL}/tasks/${taskId}/completed`, {
        method: 'PATCH',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const updatedTask = await response.json();
        setTasks(tasks.map(task => 
          task.id === taskId ? updatedTask : task
        ));
      }
    } catch (error) {
      console.error('Ошибка при изменении статуса задачи:', error);
    }
  };

  const handleEditTask = (task) => {
    setEditingTask(task);
    setShowForm(true);
  };

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <div className="welcome-section">
          <h2>Мои задачи</h2>
          <p>{user?.username}, у вас {tasks.length} задач</p>
        </div>
        
        <div className="dashboard-actions">
          <button 
            onClick={() => {
              setEditingTask(null);
              setShowForm(true);
            }}
            className="action-btn primary"
          >
            + Новая задача
          </button>
          <button onClick={onLogout} className="action-btn logout">
            Выйти
          </button>
        </div>
      </div>

      {showForm && (
        <TaskForm
          task={editingTask}
          onSubmit={editingTask ? 
            (data) => handleUpdateTask(editingTask.id, data) : 
            handleCreateTask
          }
          onCancel={() => {
            setShowForm(false);
            setEditingTask(null);
          }}
        />
      )}

      {loading ? (
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Загрузка задач...</p>
        </div>
      ) : (
        <TaskList
          tasks={tasks}
          onToggle={handleToggleTask}
          onEdit={handleEditTask}
          onDelete={handleDeleteTask}
        />
      )}

      {tasks.length === 0 && !loading && (
        <div className="empty-state">
          <div className="empty-icon">📝</div>
          <h3>Задач пока нет</h3>
          <p>Создайте свою первую задачу</p>
          <button 
            onClick={() => setShowForm(true)}
            className="action-btn primary"
          >
            Создать задачу
          </button>
        </div>
      )}
    </div>
  );
};

export default Dashboard;