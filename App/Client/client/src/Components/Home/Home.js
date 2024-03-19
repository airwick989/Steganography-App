import React from "react";
import Cookies from "universal-cookie";
import './Home.css';
import send from '../../assets/send.jpg';
import secrets from '../../assets/secrets.png';
import receive from '../../assets/receive.png';
import decode from '../../assets/decode.png';
import { useNavigate } from 'react-router-dom';
import { checkRefresh } from "../AuthHelper/AuthHelper";

const Home = () => {
  
    const cookies = new Cookies();
    var accessToken = cookies.get('access_token')
    const refreshToken = cookies.get('refresh_token')
    const navigate = useNavigate();


    async function getSecrets(){
        const secrets_url = 'http://localhost:5000/getsecrets'

        const newTokenPromise = checkRefresh(accessToken, refreshToken);
        //console.log(`OLD: ${accessToken}`);
        const newToken = await newTokenPromise;
        //console.log(`NEWTOKEN: ${newToken}`);
        if (newToken != null){
            accessToken = newToken;
            cookies.set('access_token', accessToken, { path: '/' });
        };

        //console.log(`NEW: ${accessToken}`);
        
        const headers = {
            Authorization: `Bearer ${accessToken}`
        };

        fetch(secrets_url, { headers })
        .then(response => {
            if (!response.ok) {
            throw new Error(`Failed to download secrets`);
            }
            return response.blob();
        })
        .then(blob => {
            // Create a URL for the blob
            const url = window.URL.createObjectURL(new Blob([blob]));
            // Create a link element
            const link = document.createElement('a');
            link.href = url;
            // Specify the filename
            link.setAttribute('download', 'secrets.txt');
            // Simulate click on the link to trigger download
            document.body.appendChild(link);
            link.click();
            // Remove the link element
            link.parentNode.removeChild(link);
        })
        .catch(error => {
            alert(error.message);
        });

    };


    async function getMessages(){
        const download_url = 'http://localhost:5000/download'

        const newTokenPromise = checkRefresh(accessToken, refreshToken);
        const newToken = await newTokenPromise;
        if (newToken != null){
            accessToken = newToken;
            cookies.set('access_token', accessToken, { path: '/' });
        };

        const headers = {
            Authorization: `Bearer ${accessToken}`
        };

        fetch(download_url, { headers })
        .then(response => {
            if (!response.ok) {
                throw new Error("Currently there have been no messages left for you");
            }
            return response.blob();
        })
        .then(blob => {
            // Create a URL for the blob
            const url = window.URL.createObjectURL(new Blob([blob]));
            // Create a link element
            const link = document.createElement('a');
            link.href = url;
            // Specify the filename
            link.setAttribute('download', 'messages.zip');
            // Simulate click on the link to trigger download
            document.body.appendChild(link);
            link.click();
            // Remove the link element
            link.parentNode.removeChild(link);
        })
        .catch(error => {
            alert(error.message);
        });
    };


  return (
    <div className="grid-container" style={{marginTop: '20em', marginBottom: '2em'}}>

        <div className="grid-item">
            <div className="card w-96 bg-base-100 shadow-xl image-full">
                <figure className="img-container"><img src={secrets} alt="?" /></figure>
                <div className="card-body">
                <h2 className="card-title">Generate Secrets</h2>
                <p>Generate and download a secrets file to your local machine.</p>
                <div className="card-actions justify-end">
                    <button className="btn btn-primary" onClick={getSecrets}>Generate</button>
                </div>
                </div>
            </div>
        </div>

        <div className="grid-item">
            <div className="card w-96 bg-base-100 shadow-xl image-full">
                <figure className="img-container"><img src={send} alt="?" /></figure>
                <div className="card-body">
                <h2 className="card-title">Send Message</h2>
                <p>Encrypt and send a message to a specified user.</p>
                <div className="card-actions justify-end">
                    <button className="btn btn-primary" onClick={() => navigate('/upload')}>Write Message</button>
                </div>
                </div>
            </div>
        </div>
        
        <div className="grid-item">
            <div className="card w-96 bg-base-100 shadow-xl image-full">
                <figure className="img-container"><img src={receive} alt="?" /></figure>
                <div className="card-body">
                <h2 className="card-title">Inbox</h2>
                <p>Check if any encrypted messages have been left for you.</p>
                <div className="card-actions justify-end">
                    <button className="btn btn-primary" onClick={getMessages}>View</button>
                </div>
                </div>
            </div>
        </div>

        <div className="grid-item">
            <div className="card w-96 bg-base-100 shadow-xl image-full">
                <figure className="img-container"><img src={decode} alt="?" /></figure>
                <div className="card-body">
                <h2 className="card-title">Decode</h2>
                <p>Decode an image to view the embedded message.</p>
                <div className="card-actions justify-end">
                    <button className="btn btn-primary" onClick={() => navigate('/decode')}>Decode</button>
                </div>
                </div>
            </div>
        </div>

    </div>
  );
};

export default Home;