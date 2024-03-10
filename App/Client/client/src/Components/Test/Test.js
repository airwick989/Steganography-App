import React, { useEffect } from 'react';

const TestServer = () => {
  const base_url = 'http://localhost:5000';

  useEffect(() => {
    const login_url = `${base_url}/login`;

    // Login request
    const user_credentials = { username: 'user1', password: 'password1' };

    fetch(login_url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(user_credentials),
    })
      .then(response => response.json())
      .then(data => {
        if (data.access_token) {
          const access_token = data.access_token;
          console.log(`Successfully logged in. Access Token: ${access_token}\n`);

          // Continue with additional logic or API calls here
        } else {
          console.log(`Login failed. ${JSON.stringify(data)}\n`);
        }
      })
      .catch(error => {
        console.error('Error during login:', error);
      });
  }, []); // Empty dependency array to mimic componentDidMount

  return (
    <div>
      {/* Your React component JSX */}
    </div>
  );
};

export default TestServer;