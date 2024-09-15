import './App.css';
import React, {useState} from "react";
import Particles from "react-tsparticles";
import { loadFull } from "tsparticles";
import { useCallback } from "react";
import { BlobServiceClient } from "@azure/storage-blob";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faFile } from "@fortawesome/free-solid-svg-icons";

const UploadPDFToBlob = () => {
  const [file, setFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState('');

  const sasToken = 'sp=raw&st=2024-09-15T03:32:10Z&se=2024-09-15T11:32:10Z&spr=https&sv=2022-11-02&sr=c&sig=oOAQsLb4C4N%2FhQrc5zc7ftPTtXL8xFlx8ShWoUprrVA%3D'; // Replace with your Azure SAS Token
  const containerName = 'pdfcontainer'; // Replace with your Blob Storage container name
  const storageAccountName = 'vtpdfstorage'; // Replace with your storage account name

  //create blobServiceClient from connection string
  const blobServiceClient = new BlobServiceClient(`https://${storageAccountName}.blob.core.windows.net?${sasToken}`);
  
  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const uploadFile = async () => {

    try {
      setUploadStatus('Uploading...');
      
      const containerClient = blobServiceClient.getContainerClient(containerName);
      const blobClient = containerClient.getBlockBlobClient(file.name);
      
      const arrayBuffer = await file.arrayBuffer();

      // Upload the ArrayBuffer using uploadData
      await blobClient.uploadData(arrayBuffer);
      
      setUploadStatus('Upload successful!');
    } catch (error) {
      console.error('Error uploading file:', error);
      setUploadStatus('Upload failed.');
    }
  };

  /* Particle configuration for icon */
  const particlesInit = useCallback(async (engine) => {
    await loadFull(engine);
  }, []);

  const particlesOptions = {
    particles: {
      number: { value: 30 },
      shape: {
        type: "char",
        character: {
          value: ['\uf15b'], // FontAwesome Unicode for "file" icon
          font: "FontAwesome", // FontAwesome is recognized by tsparticles
          style: "",
          weight: "400",
        },
      },
      size: { value: 20 },
      move: {
        enable: true,
        speed: 3,
        direction: "none",
        random: true,
        straight: false,
        out_mode: "out",
      },
      opacity: { value: 0.8 },
    },
    interactivity: {
      events: {
        onhover: { enable: true, mode: "repulse" },
      },
      modes: {
        repulse: { distance: 100 },
      },
    },
    retina_detect: true,
  };

  return (
    <div className = "App">

      <Particles id="tsparticles" init={particlesInit} options={particlesOptions}> 
      style={{position: "absolute", top: 0, left: 0, width: "100%",height: "100%", zIndex: 0}}
      </Particles>

      <header className = "App-header">
        <h1 className="Title">Simplifile</h1>
        <p className="Description">Simplifile simplifies the process of reading your files by reducing the content and reading it aloud for your users.</p>
        <br></br>
        <div>
          {/* One big button for both selecting and submitting the PDF */}
          <label className="upload-btn">
            <input 
              type="file" 
              accept="application/pdf" 
              onChange={handleFileChange} 
              style={{ display: 'none' }} 
              onClick={uploadFile}
            />
            <h3>Upload PDF File</h3>
          </label> 
        </div>    
      </header>
      <p>{uploadStatus}</p>
    </div>
  );
};

export default UploadPDFToBlob;
