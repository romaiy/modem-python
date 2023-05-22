from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import wave


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/transmitte")
async def convert_to_wav(file: UploadFile = File(...)):
    # Открываем файл и считываем его содержимое
    contents = await file.read()

    # Преобразуем текст в бинарный код
    binary = ''.join(format(byte, '08b') for byte in contents)

    # Создаем новый wave файл
    with wave.open('Sound.wav', 'w') as f:
        # Устанавливаем параметры звукового файла
        f.setparams((1, 1, 44100, 0, 'NONE', 'not compressed'))

        # Записываем данные в звуковой файл
        for bit in binary:
            if bit == '0':
                f.writeframes(bytes([128]))
            else:
                f.writeframes(bytes([255]))

    # Возвращаем wav файл в качестве ответа на запрос
    return FileResponse(path='Sound.wav', filename='123', media_type='audio/wav')