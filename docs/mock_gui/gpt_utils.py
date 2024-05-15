import os
from openai import OpenAI
from pathlib import Path
import warnings
import tkinter as tk

from dotenv import load_dotenv
load_dotenv()

# Ignore DeprecationWarning
warnings.filterwarnings("ignore", category=DeprecationWarning)


class Chatbot:
    def __init__(self, root, text_box, max_length=1024):
        # API Key 호출
        self.client = OpenAI(
            api_key=os.getenv('API_KEY')
        )
        
        ## GUI 관련
        self.root = root
        self.text_box = text_box
        
        self.chat_history = ""
        self.max_length = max_length

        self.response = False
        self.order = 0
        
        
    def add_message(self, message):
        # 대화 추가 전에 최대 길이를 초과할지 확인하고 조정
        updated_history = self.chat_history + "\n" + message
        if len(updated_history) > self.max_length:
            # 토큰을 줄여 최대 길이에 맞춤
            updated_history = updated_history[-self.max_length:]
        self.chat_history = updated_history

    def generate_response(self, prompt):
        print("들어온 프롬프트:", prompt)
        if prompt == "":
            answer = "질문에 답변을 해주세요"
            return answer
            
        if self.response == False:
            user_prompt = "This is My Personal Statement.\n\n" + prompt + \
                "\n\nPlease generate one question based on the Personal Statement I wrote.\n" + \
                    "Please don't create any words other than answers.\n"
            prompt = user_prompt
            self.response = True
        else:
            user_prompt = self.chat_history + "\n\n" + prompt
                    
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful Mock Interviewer.\n\
                    You have to say one sentence at a time and answer in Korean"},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=150,
            n=1,
            temperature=1
        )
        answer = response.choices[0].message.content
        self.add_message("User: " + prompt + "\n")
        self.add_message("AI: " + answer+ "\n")
        return answer
    
    def generate_summary(self):
        if self.chat_history == "":
            self.text_box.insert(tk.END, "대화 내용이 없습니다. 먼저 Mock Interview를 진행해주세요.\n")
            return "대화 내용이 없습니다. 먼저 Mock Interview를 진행해주세요."
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful Mock Interviewer.\n\
                    Look at the following whole conversation and give me a summary."},
                {"role": "user", "content": self.chat_history},
            ],
            max_tokens=150,
            temperature=1
        )
        summary = response.choices[0].message.content
        return summary

    def make_tts(self, prompt):
        speech_file_path = 'AiSpeech_' + str(self.order) + '.mp3'
        response = self.client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=prompt
        )
        response.stream_to_file(speech_file_path)
        self.order += 1
        
        return speech_file_path
        
    def make_stt(self, path):
        with open(path, "rb") as audio_file:
            transcription = self.client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file,
                temperature=1,
                language='ko'
            )
        
        
        
        return transcription.text