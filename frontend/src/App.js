import './App.css';
import React, {useState} from "react";
//import axios from "axios"
import { BlobServiceClient } from "@azure/storage-blob";

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
    if (!file) {
      alert('Please select a file first!');
      return;
    }

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

  return (
    <div className = "App">
      <header className = "App-header">
        <h1>Simplifile</h1>
        <div className="Content"> </div>
          <h3>File Upload</h3>
          <input type="file" accept="application/pdf" onChange={handleFileChange} />
          <button onClick={uploadFile}>Upload PDF</button>          
      </header>
      <p>{uploadStatus}</p>
    </div>
  );
};

export default UploadPDFToBlob;
