import React, { useState, useEffect } from 'react';
import './App.css';
import Auth from './components/Auth';
import Dashboard from './components/Dashboard';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      setIsAuthenticated(true);
      const userData = localStorage.getItem('user');
      if (userData) {
        setUser(JSON.parse(userData));
      }
    }
  }, []);

  const handleLogin = (token, userData) => {
    localStorage.setItem('token', token);
    localStorage.setItem('user', JSON.stringify(userData));
    setIsAuthenticated(true);
    setUser(userData);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setIsAuthenticated(false);
    setUser(null);
  };

  return (
    <div className="App">
      <header className="header">
        <div className="container">
          <h1>Notion</h1>
          {isAuthenticated && (
            <div className="user-info">
              <span>{user?.username || 'Пользователь'}</span>
              <button onClick={handleLogout} className="logout-btn">
                Выйти
              </button>
            </div>
          )}
        </div>
      </header>
      
      <main className="main-content">
        <div className="container">
          {isAuthenticated ? (
            <Dashboard user={user} onLogout={handleLogout} />
          ) : (
            <Auth onLogin={handleLogin} />
          )}
        </div>
      </main>
      
      <footer className="footer">
        <div className="container">
          <p>© 2025 Abdullaev Gamzat</p>
        </div>
      </footer>
    </div>
  );
}

export default App;