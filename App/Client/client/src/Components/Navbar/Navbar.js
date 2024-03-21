import React from 'react';
import './Navbar.css';
import { useNavigate } from 'react-router-dom';
import Cookies from 'universal-cookie';
import LogoutIcon from './LogoutIcon';

const Navbar = () => {
  const navigate = useNavigate();
  const cookies = new Cookies();
  const username = cookies.get('username');

    const logout = () => {
        const allCookies = cookies.getAll();
        Object.keys(allCookies).forEach(cookieName => {
            cookies.remove(cookieName);
        });

        navigate('/', { replace: true });
    };

  return (
    <ul className="menu menu-horizontal bg-base-200 rounded-box" style={{ marginBottom: '50px', marginTop: '70px', display: 'flex', justifyContent: 'center' }}>
      <li>
        <button onClick={() => navigate('/home')}>
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
          </svg>
        </button>
      </li>
      <li>
        <button className="tooltip-button">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span className="tooltip-text">{username}</span>
        </button>
      </li>
      <li>
        <button onClick={logout}>
          <LogoutIcon fill="#a6adbb" width="24" height="24" />
        </button>
      </li>
    </ul>
  );
};

export default Navbar;