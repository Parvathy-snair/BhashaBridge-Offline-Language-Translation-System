import pyttsx3

engine = pyttsx3.init()
engine.setProperty("voice", "ml")  # try "mal" or "english" if silent
engine.say("സുഖമാണോ")
engine.runAndWait()
