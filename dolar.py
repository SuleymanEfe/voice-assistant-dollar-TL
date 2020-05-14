import speech_recognition as sr
from playsound import playsound
from gtts import gTTS
import random
import os
import requests
import re

r = sr.Recognizer()

api = requests.get('https://api.exchangeratesapi.io/latest?base=USD')
cektigim = api.json()
dolar = cektigim['rates']['TRY']


def record():
    with sr.Microphone() as source:
        speak('Dinliyorum')
        audio = r.listen(source)
        voice = ''
        try:
            voice = r.recognize_google(audio, language='tr-TR')
        except:
            pass
        speak('1 dakika lutfen')
        return voice


def speak(string):
    tts = gTTS(string, lang='tr')
    rand = random.randint(1, 10000)
    file = 'audio' + str(rand) + '.mp3'
    tts.save(file)
    playsound(file)
    os.remove(file)

voice = record()
print(voice)

sonuc = re.match(r'(\d+) (dolar|TL)', voice)



if sonuc:
    sayi = int(sonuc.group().split()[0])
    birim = sonuc.group().split()[1]
    if birim == 'dolar':
        sonuc = str(dolar * sayi)
    elif birim == 'TL':
        sonuc = str(sayi / dolar)
    else:
        sonuc = 'Anlayamadim'
    speak(sonuc)
else:
    sonuc = 'Sadece dolar ve tlyi cevirebiliyorum.'
    speak(sonuc)
