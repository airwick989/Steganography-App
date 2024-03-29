import React, { useState, useEffect } from 'react';
import Cookies from "universal-cookie";
import './Decoder.css';
import { checkRefresh } from '../AuthHelper/AuthHelper';
import { useNavigate } from 'react-router-dom';
import Navbar from '../Navbar/Navbar';

const Decoder = () => {
  const [photo, setPhoto] = useState(null);
  const [secretsFile, setSecretsFile] = useState(null);
  
  const cookies = new Cookies();
  var accessToken = cookies.get('access_token')
  const refreshToken = cookies.get('refresh_token')
  const navigate = useNavigate();

  useEffect(() => {
      if (accessToken === undefined){
          navigate('/', { replace: true });
      }
  }, [accessToken, navigate]);


  const handleSubmit = async e => {
    e.preventDefault();

    // Check if any of the inputs are empty
    if (!photo || !secretsFile) {
      alert('All form inputs are required.');
      return;
    }

    // Check if photo is a png or jpeg
    if (photo && !['image/png'].includes(photo.type)) {
      alert('Invalid photo format. Please upload a PNG image file.');
      return;
    }

    // Check if secretsFile is a txt file
    if (secretsFile && secretsFile.type !== 'text/plain') {
      alert('Invalid secrets file format. Please upload a TXT file.');
      return;
    }

    const decode_url = 'http://localhost:5000/decode';

    const formData = new FormData();
    formData.append('photo', photo);
    formData.append('secretsFile', secretsFile);

    const newTokenPromise = checkRefresh(accessToken, refreshToken);
    const newToken = await newTokenPromise;
    if (newToken != null){
        accessToken = newToken;
        cookies.set('access_token', accessToken, { path: '/' });
    };

    try {
      const response = await fetch(decode_url, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
        body: formData,
      });

      const result = await response.json();
      alert(`HIDDEN MESSAGE:\n${result.message}`);
    } catch (error) {
      alert('Error during upload:', error);
    }
  };

  return (
    <div>
      <Navbar />
      <form onSubmit={handleSubmit}>

        <h1 className="text-5xl font-bold" style={{marginBottom: '1em'}}>Decode an Embedded Image</h1>
        <label className="form-control w-full max-w-xs">
          <div className="label">
            <span className="label-text">Upload Image</span>
            <span className="label-text-alt">png</span>
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

        <button className="btn btn-xs sm:btn-sm md:btn-md lg:btn-lg" type='submit'>Submit</button>
      </form>
    </div>
  );
};

export default Decoder;