import React from "react";
import Cookies from "universal-cookie";
import './Home.css';
import send from '../../assets/send.jpg';
import secrets from '../../assets/secrets.png';
import receive from '../../assets/receive.png';
import decode from '../../assets/decode.png';

const Home = () => {
  
    const cookies = new Cookies();
    const accessToken = cookies.get('access_token')

    console.log(accessToken)

  return (
    <div className="grid-container" style={{marginTop: '20em', marginBottom: '2em'}}>

        <div className="grid-item">
            <div className="card w-96 bg-base-100 shadow-xl image-full">
                <figure className="img-container"><img src={secrets} alt="?" /></figure>
                <div className="card-body">
                <h2 className="card-title">Generate Secrets</h2>
                <p>Generate and download a secrets file to your local machine.</p>
                <div className="card-actions justify-end">
                    <button className="btn btn-primary">Generate</button>
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
                    <button className="btn btn-primary">Write Message</button>
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
                    <button className="btn btn-primary">View</button>
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
                    <button className="btn btn-primary">Decode</button>
                </div>
                </div>
            </div>
        </div>

    </div>
  );
};

export default Home;