from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import wave
import requests

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

    text = convert()
    return {"content": text}

def convert():
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
    return text