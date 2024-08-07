import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [contentImage, setContentImage] = useState(null);
  const [styleImage, setStyleImage] = useState(null);
  const [stylizedImage, setStylizedImage] = useState(null);

  const handleImageChange = (e, setImage) => {
    const file = e.target.files[0];
    setImage(URL.createObjectURL(file));
  };

  const handleSubmit = async () => {
    const contentFile = document.getElementById('content-image').files[0];
    const styleFile = document.getElementById('style-image').files[0];
    const formData = new FormData();
    formData.append('content_image', contentFile);
    formData.append('style_image', styleFile);

    // try {
    //   const response = await axios.post('https://ai-generative-works.onrender.com/stylize', formData, {
    //     headers: { 'Content-Type': 'multipart/form-data' },
    //   });
    //   const result = response.data.stylized_image;
    //   setStylizedImage(`data:image/jpeg;base64,${result}`);
    // } catch (error) {
    //   console.error('Error uploading images:', error);
    // }
    try {
      const response = await fetch('https://ai-generative-works.onrender.com/stylize', {
        method: 'POST',
        body: formData,
        headers: {
          'Accept': 'application/json',
        }
      });
      const result = await response.json();
      setStylizedImage(`data:image/jpeg;base64,${result.stylized_image}`);
    } catch (error) {
      console.error('Error uploading images:', error);
    }
  };

  return (
    <div className="container">
      <h1>Image Stylizer</h1>
      <div className="image-container">
        <div className="preview-box">
          {contentImage && <img src={contentImage} alt="Content" />}
          <div className="upload-button-container">
            <input
              type="file"
              id="content-image"
              onChange={(e) => handleImageChange(e, setContentImage)}
            />
          </div>
        </div>
        <div className="preview-box">
          {styleImage && <img src={styleImage} alt="Style" />}
          <div className="upload-button-container">
            <input
              type="file"
              id="style-image"
              onChange={(e) => handleImageChange(e, setStyleImage)}
            />
          </div>
        </div>
        <div className="stylized-box">
          {stylizedImage && <img src={stylizedImage} alt="Stylized" />}
          <button onClick={handleSubmit}>Stylize Image</button>
        </div>
      </div>
    </div>
  );
}

export default App;
