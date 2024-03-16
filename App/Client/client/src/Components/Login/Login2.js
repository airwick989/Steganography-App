import React, { useState } from 'react';
import { useAuth } from '../Auth/AuthContext';

const Login = () => {
  const { login } = useAuth();
  const [token, setToken] = useState('');

  const handleLogin = () => {
    // Here you would typically make an API call to authenticate the user
    // and obtain the access token
    login(token);
  };

  return (
    <div>
        <h1>HELLO</h1>
        <input type="text" value={token} onChange={(e) => setToken(e.target.value)} />
        <button onClick={handleLogin}>Login</button>
    </div>
  );
};

export default Login;