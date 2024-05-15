from gpt_utils import *

cb = Chatbot()
text = cb.make_stt('UserSpeech_3.wav')
print(text, len(text), type(text))
if text == "":
    print("no text")
if text == None:
    print("dodododo")