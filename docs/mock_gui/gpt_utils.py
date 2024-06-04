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
        self.ps = self.get_PersonalStatement("ps.txt")
        
        self.max_length = max_length
        self.max_tokens = 150
        self.n = 1
        self.temperature = 1

        self.response = False
        self.order = 0
        self.model = "gpt-3.5-turbo"
        self.fine_tuned_model = "ft:gpt-3.5-turbo-0125:personal:60mock:9W2XDE5J"
        
        
    def add_message(self, message):
        # 대화 추가 전에 최대 길이를 초과할지 확인하고 조정
        updated_history = self.chat_history + "\n" + message
        if len(updated_history) > self.max_length:
            # 토큰을 줄여 최대 길이에 맞춤
            updated_history = updated_history[-self.max_length:]
        self.chat_history = updated_history

    def generate_ps_questions(self, user_input, reply=False, new_dialog=False):
        print("자소서 기반 질문 생성! 들어온 프롬프트:", user_input)
        # 자소서 입력이 안된 경우
        if user_input == "":
            ai_answer = "질문에 답변을 해주세요"
            return ai_answer
        
        # 자소서 입력이 된 경우, 질문 생성
        # 자소서 기반 유저 프롬프트 생성
        user_prompt = "This is My Personal Statement.\n\n" + user_input + \
            "\n\nPlease create 2 questions for each item in Korean based on the contents written in the Personal Statement.\n\
            Please separate it by \n, and don't number it."
        response = self.client.chat.completions.create(
            model = self.model,
            messages=[
                {"role": "system", "content": "You are a helpful Mock Interviewer.\n\
                    Please create a question in Korean related to the user's answer"},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=self.max_tokens,
            n=self.n,
            temperature=self.temperature
        )
        # 질문 생성
        question_list = response.choices[0].message.content
        question_list = question_list.split("\n")
        print("질문 개수: ", len(question_list))
        return question_list

    # 응답 생성
    def generate_response(self, user_input, reply=False, new_dialog=False): #follow question
        print("들어온 프롬프트:", user_input)
        # 인터뷰 도중 유저의 입력이 없을 경우
        if user_input == "":
            ai_answer = "질문에 답변을 해주세요"
            return ai_answer
        
        # 첫 응답일 경우 자소서에 대한 질문 생성
        if new_dialog:
            user_prompt = "This is My Personal Statement.\n\n" + user_input + \
                "\n\nPlease create 2 questions for each item in Korean based on the contents written in the Personal Statement.\n\
                    Please separate it by \n, and don't number it."
            response = self.client.chat.completions.create(
                model = self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful Mock Interviewer.\n\
                        Please create a question in Korean related to the user's answer"},
                    {"role": "user", "content": user_prompt},
                ],
                max_tokens=150,
                n=1,
                temperature=1
            )
            ai_answer = response.choices[0].message.content                      
        else:
            user_prompt = self.chat_history + "\n\n" + user_input
        
        # 꼬리 질문일 경우 사용자 답변을 기반으로 질문을 생성
        if reply:
            ai_answer = "꼬리질문이다이"
            
            # response = self.client.chat.completions.create(
            #     model = self.model,
            #     messages=[
            #         {"role": "system", "content": "You are a helpful Mock Interviewer.\n\
            #             Please create a question in Korean related to the user's answer"},
            #         {"role": "user", "content": user_prompt},
            #     ],
            #     max_tokens=150,
            #     n=1,
            #     temperature=1
            # )
            # ai_answer = response.choices[0].message.content               
        # 꼬리 질문이 아닐 경우 질문 리스트에서 가져온 질문 사용
        else:
            ai_answer = reply
         
        
        # 채팅 히스토리 기록
        self.add_message("User: " + user_input + "\n")
        self.add_message("AI: " + ai_answer+ "\n")
        return ai_answer
    
    def generate_summary(self):
        if not self.is_interviewed(): return
        
        response = self.client.chat.completions.create(
            model = self.model,
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
    
    def evaluate_interview(self):
        if not self.is_interviewed(): return
        
        response = self.client.chat.completions.create(
            model = self.model,
            messages=[
                {"role": "system", "content": "You are a helpful Mock Interviewer.\n\
                    Look at the following whole conversation and give me an evaluation.\n\
                    Give a maximum of 5 score according to each evaluation criteria and explain why in korean.\n\
                    Here are five evaluation criteria.\n\n\
                    1. Is the answer based on the cover letter?\n\
                    2. Is the clarity and logic of the answers to the given questions appropriate?\n\
                    3. Is the interviewer's ability to understand the point of the question appropriate?\n\
                    4. Is your major knowledge (technical) utilization ability, related work experience, and skill level sufficient?\n\
                    5. Is creativity, willpower and developability (self-improvement needs), vision, and future plans well described?"},
                {"role": "user", "content": self.chat_history},
            ],
            max_tokens=150,
            temperature=1
        )
        evaluation = response.choices[0].message.content
        return evaluation

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
    
    def is_interviewed(self):
        if self.chat_history == "":
            self.text_box.insert(tk.END, "대화 내용이 없습니다. 먼저 Mock Interview를 진행해주세요.\n")
            return False
        else:
            True
        
    def get_PersonalStatement(self, txt_path):
        personal_statement = ""
        with open(txt_path, 'r', encoding='utf-8') as fp:
            lines = fp.readlines()
            for line in lines:
                personal_statement += line
        return personal_statement