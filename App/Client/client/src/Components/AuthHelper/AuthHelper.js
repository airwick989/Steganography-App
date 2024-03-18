export function checkRefresh(access_token, refresh_token){
    if (access_token) {
        const decodedToken = decodeToken(access_token);
        console.log('Access Token:', access_token); // Log decoded token
        console.log('Decoded Token:', decodedToken); // Log decoded token
        if (decodedToken.exp * 1000 > Date.now()) {
            // Token is not expired
            return null;
        } else {
            // Token is expired, attempt refresh
            return refreshTokens(refresh_token);
        }
    }
};


const decodeToken = token => {
    try {
        return JSON.parse(atob(token.split('.')[1]));
    } catch (error) {
        return null;
    }
};


const refreshTokens = refresh_token => {
    if (refresh_token) {
      return fetch('http://localhost:5000/refreshtoken', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${refresh_token}`,
        },
        body: JSON.stringify({ refresh_token }),
      })
        .then(response => response.json())
        .then(data => {
          if (data.access_token) {
            console.log(`Successfully refreshed access token: ${data.access_token}`);
            // Update access token and return it
            return data.access_token;
          } else {
            console.log('Failed to refresh access token:', data.message);
            return null; // Return null if access token refresh fails
          }
        })
        .catch(error => {
          console.error('Error refreshing access token:', error);
          return null; // Return null if there's an error during token refresh
        });
    } else {
      console.log('Refresh token not found.');
      return null; // Return null if refresh token is not found
    }
};