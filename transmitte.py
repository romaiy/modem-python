import wave

# Открываем текстовый файл для чтения и считываем его содержимое
with open('File.txt', 'r') as file:
    text = file.read()

# Преобразуем текст в бинарный код
binary = ''.join(format(ord(i), '08b') for i in text)

# Создаем новый wave файл
with wave.open('sound_file.wav', 'w') as file:
    # Устанавливаем параметры звукового файла
    file.setparams((1, 1, 44100, 0, 'NONE', 'not compressed'))

    # Записываем данные в звуковой файл
    for bit in binary:
        if bit == '0':
            file.writeframes(bytes([128]))
        else:
            file.writeframes(bytes([255]))