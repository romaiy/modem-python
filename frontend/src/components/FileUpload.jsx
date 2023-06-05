import axios from "axios";
import React from 'react';
import { useState } from "react";

const FileUpload = () => {
    const [text, setText] = useState('');
    const [isLoading, setLoading] = useState(false);
    const [audioUrl, setAudioUrl] = useState();
    
    const handleChange = e => {
        setLoading(true)
        const fileInput = e.target;
        const file = fileInput.files[0];
        if (file) {
            handleSubmit(file);
        }
    };

    const handleSubmit = async file => {
        const formData = new FormData();
        formData.append('file', file);
    
        try {
            const response = await axios.post('http://127.0.0.1:8000/transmitte', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                },
                responseType: 'blob'
            });
            const url = window.URL.createObjectURL(new Blob([response.data]));
            console.log(url)
            setAudioUrl(url);
        } catch (error) {
            console.error(error);
        } finally {
            setLoading(false)
        }
    };

    const handleDownload = () => {
        const link = document.createElement('a');
        link.href = audioUrl;
        link.setAttribute('download', 'Sound.wav');
        document.body.appendChild(link);
        link.click();
    };

    const handleClear = () => {
        setAudioUrl();
        setText();
    };

    const handleUpload = async () => {
        const formData = new FormData();
        formData.append('file', audioUrl);
        try {
            const response = await axios.post('http://127.0.0.1:8000/receiver', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            console.log(response.data);
            setText(response.data.text);
            handleDownload();
        } catch (error) {
            console.error(error);
        } finally {
        }
    };

    return (
        <div className="container">
            <div className="audio">
                <h1 className="audio__heading">Приложение модем</h1>
                <div className="audio__row" style={{marginTop: '30px', height: '54px'}}>
                    <input
                        aria-label="Выберите файл"
                        type="file" 
                        onChange={(e) => handleChange(e)}
                        className="custom-file-input"
                    />
                    <button
                        aria-label="Очистить"
                        style={{marginRight: '35px'}}
                        onClick={handleClear}
                        className="custom-file-button"
                    >
                    </button>
                    {audioUrl &&
                    <audio
                        onEnded={() => handleUpload()}
                        controls
                        src={audioUrl}
                    >
                    </audio>
                }
                    <div className="audio__state">{isLoading ? 'Обработка' : 'Ожидание загрузки'}</div>
                </div>
                <p className="audio__text">
                    {text && <>{text}</>}
                </p>
            </div>
        </div>
    );
};

export default FileUpload;