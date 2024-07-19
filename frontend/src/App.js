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

    try {
      const response = await axios.post('http://localhost:5000/stylize', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      const result = response.data.stylized_image;
      setStylizedImage(`data:image/jpeg;base64,${result}`);
    } catch (error) {
      console.error('Error uploading images:', error);
    }
  };

  return (
    <div className="container">
      <h1>Image Stylizer</h1>
      <input
        type="file"
        id="content-image"
        onChange={(e) => handleImageChange(e, setContentImage)}
      />
      {contentImage && <img src={contentImage} alt="Content" className="image-preview" />}
      <input
        type="file"
        id="style-image"
        onChange={(e) => handleImageChange(e, setStyleImage)}
      />
      {styleImage && <img src={styleImage} alt="Style" className="image-preview" />}
      <button onClick={handleSubmit}>Stylize Image</button>
      <div className="stylized-box">
        {stylizedImage && <img src={stylizedImage} alt="Stylized" />}
      </div>
    </div>
  );
}

export default App;
