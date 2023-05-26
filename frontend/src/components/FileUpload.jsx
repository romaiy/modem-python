import axios from "axios";
import { useEffect, useState } from "react";

const FileUpload = () => {
    const [text, setText] = useState('');
    const [isLoading, setLoading] = useState(false);
    
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
                }
            })
            setText(response.data.content)
            console.log(response.data)
        } catch (error) {
            console.error(error);
        } finally {
            setLoading(false)
        }
    };

    return (
        <div className="container">
            <div className="audio">
                <h1 className="audio__heading">Приложение модем</h1>
                <div className="audio__row">
                    <input 
                        type="file" 
                        onChange={(e) => handleChange(e)}
                        className="custom-file-input"
                    />
                    <button
                        onClick={() => setText('')}
                        className="custom-file-button"
                    >
                    </button>
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