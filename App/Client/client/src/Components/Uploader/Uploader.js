import React, { useState } from 'react';
import Cookies from "universal-cookie";
import './Uploader.css';

const Uploader = () => {
  const [photo, setPhoto] = useState(null);
  const [secretsFile, setSecretsFile] = useState(null);
  const [recipient, setRecipient] = useState('');
  const [message, setMessage] = useState('');
  
  const cookies = new Cookies();
  const accessToken = cookies.get('access_token')

  // useEffect(() => {
  //   const login_url = 'http://localhost:5000/login';
  //   const user_credentials = { username: 'user1', password: 'password1' };

  //   fetch(login_url, {
  //     method: 'POST',
  //     headers: {
  //       'Content-Type': 'application/json',
  //     },
  //     body: JSON.stringify(user_credentials),
  //   })
  //     .then(response => response.json())
  //     .then(data => {
  //       if (data.access_token) {
  //         setAccessToken(data.access_token);
  //         console.log(`Successfully logged in. Access Token: ${data.access_token}\n`);
  //       } else {
  //         console.log(`Login failed. ${JSON.stringify(data)}\n`);
  //       }
  //     })
  //     .catch(error => {
  //       console.error('Error during login:', error);
  //     });
  // }, []); // Empty dependency array to mimic componentDidMount

  const handleSubmit = async e => {
    e.preventDefault();

    // Check if any of the inputs are empty
    if (!photo || !secretsFile || !recipient || !message) {
      alert('All form inputs are required.');
      return;
    }

    // Check if photo is a png or jpeg
    if (photo && !['image/png', 'image/jpeg'].includes(photo.type)) {
      alert('Invalid photo format. Please upload a PNG or JPEG file.');
      return;
    }

    // Check if secretsFile is a txt file
    if (secretsFile && secretsFile.type !== 'text/plain') {
      alert('Invalid secrets file format. Please upload a TXT file.');
      return;
    }

    const upload_url = 'http://localhost:5000/upload';

    const formData = new FormData();
    formData.append('photo', photo);
    formData.append('secretsFile', secretsFile);
    formData.append('recipient', recipient);
    formData.append('message', message);

    // console.log(formData.get('photo'));
    // console.log(formData.get('secretsFile'));
    // console.log(formData.get('recipient'));
    // console.log(formData.get('message'));

    try {
      const response = await fetch(upload_url, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
        body: formData,
      });

      const result = await response.json();
      alert(result.message);
    } catch (error) {
      alert('Error during upload:', error);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>

        <h1 className="text-5xl font-bold" style={{marginBottom: '1em'}}>Send Encrypted Message</h1>
        <label className="form-control w-full max-w-xs">
          <div className="label">
            <span className="label-text">Upload Image</span>
            <span className="label-text-alt">png or jpeg</span>
          </div>
          <input type="file" onChange={e => setPhoto(e.target.files[0])} className="file-input file-input-bordered w-full max-w-xs" />
        </label>

        <label className="form-control w-full max-w-xs">
          <div className="label">
            <span className="label-text">Upload Secrets File</span>
            <span className="label-text-alt">txt</span>
          </div>
          <input type="file" onChange={e => setSecretsFile(e.target.files[0])} className="file-input file-input-bordered w-full max-w-xs" />
        </label>

        <label className="input input-bordered flex items-center gap-2">
          Recipient:
          <input type="text" className="grow" placeholder="enter recipient's username here" value={recipient} onChange={e => setRecipient(e.target.value)} />
        </label>

        <label className="form-control">
          <div className="label">
            <span className="label-text">Enter you covert message here</span>
          </div>
          <textarea className="textarea textarea-bordered h-24" placeholder="Type here" value={message} onChange={e => setMessage(e.target.value)}></textarea>
        </label>

        <button className="btn btn-xs sm:btn-sm md:btn-md lg:btn-lg" type='submit'>Submit</button>
      </form>
    </div>
  );
};

export default Uploader;