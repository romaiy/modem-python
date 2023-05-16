import wave

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

