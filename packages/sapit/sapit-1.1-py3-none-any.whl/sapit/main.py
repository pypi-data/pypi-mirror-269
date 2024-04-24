import pyttsx3 as pt

engine = pt.init('sapi5')
voices = engine.getProperty('voices')

engine.setProperty ('voice', voices[0].id)

def say(audio):
    engine.say(audio)
    engine.runAndWait()