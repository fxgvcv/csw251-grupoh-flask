import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { registerUser, authenticateUser } from '../services/api';

function Login({ onLoginSuccess }) {
  const [isRegistering, setIsRegistering] = useState(false);
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState(''); // Only for registration
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();
    setIsLoading(true);
    setError(null);

    try {
      if (isRegistering) {
        // Register new user
        const userData = { username, email, password };
        await registerUser(userData);
        alert('Registration successful! Please log in.');
        setIsRegistering(false); 
      } else {
        const credentials = { username, password };
        const response = await authenticateUser(credentials);
        
        console.log('Login successful:', response.data); 
        localStorage.setItem('userToken', response.data.token);
        localStorage.setItem('username', username);

        onLoginSuccess();
        navigate('/buildings');
      }
    } catch (err) {
      console.error('Authentication/Registration error:', err);
      setError(err.response?.data?.message || 'Authentication failed. Please check your credentials or try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <article className="login-container">
      <header>
        <h2>{isRegistering ? 'Register' : 'Login'} to SARC</h2>
      </header>
      {error && <p role="alert" className="error-message">{error}</p>}
      <form onSubmit={handleSubmit}>
        <label htmlFor="username">
          Username:
          <input
            type="text"
            id="username"
            name="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            aria-busy={isLoading}
          />
        </label>

        {isRegistering && (
          <label htmlFor="email">
            Email:
            <input
              type="email"
              id="email"
              name="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              aria-busy={isLoading}
            />
          </label>
        )}

        <label htmlFor="password">
          Password:
          <input
            type="password"
            id="password"
            name="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            aria-busy={isLoading}
          />
        </label>

        <button type="submit" aria-busy={isLoading} disabled={isLoading}>
          {isLoading ? 'Loading...' : (isRegistering ? 'Register' : 'Login')}
        </button>
      </form>

      <small>
        {isRegistering ? (
          <>
            Already have an account?{' '}
            <a href="#" onClick={() => setIsRegistering(false)}>Login here</a>
          </>
        ) : (
          <>
            Don't have an account?{' '}
            <a href="#" onClick={() => setIsRegistering(true)}>Register here</a>
          </>
        )}
      </small>
    </article>
  );
}

export default Login;