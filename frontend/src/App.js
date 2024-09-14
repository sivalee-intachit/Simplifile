import logo from './logo.svg';
import './App.css';
import {useState} from "react";
import axios from "axios"

function App() {

  const [ file, setFile ] = useState(null)

  function handleUpload() {
    if (!file) {
      console.log("No file selected");
      return;
    }
    const fd = new FormData();
    fd.append('file', file);

    axios.post('http://httpbin.org/post', fd, {
      onUploadProgress: (progressEvent) => ( console.log(progressEvent.progress*100) ),
      headers : {
        "Customer-Header": "value",
      }
    })
    .then(res => console.log(res.data))
    .catch(err => console.error(err))
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>Simplifile</h1>
        <div className="Content">
          <h3>File Upload</h3>
          
          <input onChange={ (e) => { setFile(e.target.files[0])}} type="file"/>
          
          <button onClick={ handleUpload } >Upload</button>
        </div>
      </header>
    </div>
  );
}

export default App;
