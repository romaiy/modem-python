from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import wave

app = FastAPI()

@app.post("/convert")
async def convert_to_wav(file: UploadFile = File(...)):
    # Открываем файл и считываем его содержимое
    contents = await file.read()

    # Преобразуем текст в бинарный код
    binary = ''.join(format(byte, '08b') for byte in contents)

    # Создаем новый wave файл
    with wave.open('temp.wav', 'w') as f:
        # Устанавливаем параметры звукового файла
        f.setparams((1, 1, 44100, 0, 'NONE', 'not compressed'))

        # Записываем данные в звуковой файл
        for bit in binary:
            if bit == '0':
                f.writeframes(bytes([128]))
            else:
                f.writeframes(bytes([255]))

    # Возвращаем wav файл в качестве ответа на запрос
    return FileResponse('temp.wav', media_type='audio/wav')