import React, { useState } from 'react';
import Cookies from 'universal-cookie';
import logo from '../../assets/logo.png';
import { useNavigate } from 'react-router-dom';

const Login = () => {
  const [user, setUser] = useState('');
  const [pass, setPass]  =useState('');
  const cookies = new Cookies();
  const navigate = useNavigate();


  const handleSubmit = async e => {
    e.preventDefault();

    // Check if any of the inputs are empty
    if (!user || !pass) {
      alert('Username and Password Required');
      return;
    }

    const url = 'http://localhost:5000/login';

    // const formData = new FormData();
    // formData.append('username', user);
    // formData.append('password', pass);
    const user_credentials = { username: user, password: pass};

    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(user_credentials),
    })
      .then(response => response.json())
      .then(data => {
        if (data.access_token) {
          console.log(`Successfully logged in. Access Token: ${data.access_token}\n`);

          // Set the access token as a cookie
          cookies.set('access_token', data.access_token, {
            path: '/',
          });
          console.log(`access_token value: ${cookies.get('access_token')}`);

          alert("Successfully logged in")
          navigate('/home')
        } else {
          console.log(`Login failed. ${JSON.stringify(data)}\n`);
          alert(`Login failed. ${data['message']}\n`);
        }
      })
      .catch(error => {
        console.error('Error during login:', error);
        alert(`Error: ${error}`);
      });

  };


  return (
    <form onSubmit={handleSubmit}>
      <div className="card w-96 glass" >
        <figure style={{padding: '5%'}}><img src={logo} alt='Logo Missing'/></figure>
        <div 
          className="card-body"
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}  
        >
          <h2 className="card-title" style={{marginBottom: '0.5em'}}>Login</h2>
          
          <label className="input input-bordered flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor" className="w-4 h-4 opacity-70"><path d="M8 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6ZM12.735 14c.618 0 1.093-.561.872-1.139a6.002 6.002 0 0 0-11.215 0c-.22.578.254 1.139.872 1.139h9.47Z" /></svg>
            <input type="text" value={user} onChange={e => setUser(e.target.value)} className="grow" placeholder="Username" />
          </label>
          <label className="input input-bordered flex items-center gap-2">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor" className="w-4 h-4 opacity-70"><path fillRule="evenodd" d="M14 6a4 4 0 0 1-4.899 3.899l-1.955 1.955a.5.5 0 0 1-.353.146H5v1.5a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1-.5-.5v-2.293a.5.5 0 0 1 .146-.353l3.955-3.955A4 4 0 1 1 14 6Zm-4-2a.75.75 0 0 0 0 1.5.5.5 0 0 1 .5.5.75.75 0 0 0 1.5 0 2 2 0 0 0-2-2Z" clipRule="evenodd" /></svg>
            <input type="password" value={pass} onChange={e => setPass(e.target.value)} className="grow" placeholder="Password" />
          </label>
          
          <div className="card-actions justify-end" style={{marginTop: '0.5em'}}>
            <button className="btn btn-primary" type='submit'>Access</button>
          </div>

        </div>
      </div>
    </form>
  );
};

export default Login;