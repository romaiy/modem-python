from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import wave
import requests
import json

app2 = FastAPI()
app2.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app2.post("/receiver")
async def convert_to_txt(data: str):

    response = requests.get(data)
    with open('Sound.wav', 'wb') as f:
        f.write(response.content)

    # Открываем звуковой файл для чтения
    with wave.open('Sound.wav', 'r') as file:
        # Получаем параметры звукового файла
        channels, _, framerate, _, _, _ = file.getparams()

    # Читаем данные из звукового файла
    binary = ''
    for i in range(file.getnframes()):
        frame = file.readframes(1)
        if frame[0] < 192:
            binary += '0'
        else:
            binary += '1'

    # Преобразуем бинарный код в текст
    text = ''
    for i in range(0, len(binary), 8):
        text += chr(int(binary[i:i+8], 2))

    # Записываем текст в новый файл
    with open('NewFile.txt', 'w', encoding='utf-8') as file:
        file.write(text)

    # Возвращаем содержимое файла в качестве ответа
    with open('NewFile.txt', 'r', encoding='utf-8') as file:
        content = file.read()

    return {"content": content}
