import os
from openai import OpenAI
from pathlib import Path
import warnings
import tkinter as tk
import re

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
        
        self.chat_history = []
        self.real_history = ""
        # self.ps = self.get_PersonalStatement("ps.txt")
        
        self.max_length = max_length
        self.max_tokens = 4000
        self.n = 1
        self.temperature = 1

        self.response = False
        self.order = 0
        self.model = "gpt-3.5-turbo"
        self.fine_tuned_model = "ft:gpt-3.5-turbo-0125:personal:60mock:9W2XDE5J"
        
        
    # def add_message(self, message):
    #     # 대화 추가 전에 최대 길이를 초과할지 확인하고 조정
    #     updated_history = self.chat_history + "\n" + message
    #     if len(updated_history) > self.max_length:
    #         # 토큰을 줄여 최대 길이에 맞춤
    #         updated_history = updated_history[-self.max_length:]
    #     self.chat_history = updated_history

    def history_update(self, role, content):
        # 대화 추가 전에 최대 길이를 초과할지 확인하고 조정
        # updated_history = self.chat_history + "\n" + message
        # if len(updated_history) > self.max_length:
        #     # 토큰을 줄여 최대 길이에 맞춤
        #     updated_history = updated_history[-self.max_length:]
        self.chat_history.append({"role": role, "content": content})
        
    def real_history_update(self, role, content):
        self.real_history += role + ": " + content + "\n"
        if role == "A":
            self.real_history += "\n"
        
    def generate_ps_questions(self, user_input, reply=False, new_dialog=False):
        def process_answer(ai_answer):
            q_list = []
            # 질문을 나눠서 질문 리스트 생성
            question_list = ai_answer.split("\n")
            # 질문 사이사이 빈 문자열 제거
            filtered_question_list = [question for question in question_list if question != ""]
            
            for question in filtered_question_list:
                q_list.append(re.sub(r'^[\d-]+\.\s*|^-+\s*', '', question))
                
            return q_list[::-1]
        
        # print("자소서 기반 질문 생성! 들어온 프롬프트:", user_input)
        # # 자소서 입력이 안된 경우
        # if user_input == "":
        #     ai_answer = "질문에 답변을 해주세요"
        #     return ai_answer
        
        # GPT용 시스템 입력 생성 후 히스토리 업데이트
        system_input =  "You are a helpful Mock Interviewer.\n" + \
            "Your task is to generate thoughtful and relevant interview questions in Korean based on the provided Personal Statement.\n" + \
            "Each paragraph should have exactly 2 questions, Do not provide any additional commentary or text. Just provide the questions."
        self.history_update("system", system_input)
                
        # 자소서 입력이 된 경우, 자소서 기반 질문 생성
        user_prompt = f"This is My Personal Statement:\n{user_input}\n\n" + \
                "For each paragraph above, generate exactly 2 interview questions in Korean." + \
                "Provide only the questions without any additional text."
            #   "Do not provide any additional commentary or text. Just provide the questions."

        # user_prompt = "This is My Personal Statement.\n" + \
        #     "Please create 2 questions for each paragraph in the Personal Statement in Korean.\n" + \
        #     "Don't say anything other than a question sentence.\n\n" + user_input
        self.history_update("user", user_prompt) # 히스토리 업데이트
        
        # GPT 응답 생성
        response = self.client.chat.completions.create(
            model = self.model,
            messages=self.chat_history,
            # max_tokens=self.max_tokens,
            # n=self.n,
            temperature=self.temperature
        )
        
        # 응답 history에 추가
        ai_answer = response.choices[0].message.content
        self.history_update("assistant", ai_answer)
        # 질문을 나눠서 질문 리스트 생성
        print("\n질문 생성됨 ==== \n", ai_answer)
        question_list = process_answer(ai_answer)
        # question_list = ai_answer.split("\n")
        print("\n처리된 질문\n", question_list)
        print("질문 개수: ", len(question_list))
        return question_list

    # 응답 생성
    def generate_response(self, user_input, question=False): #follow question
        self.history_update("user", user_input)
        self.real_history_update("A", user_input)
        # 인터뷰 도중 유저의 입력이 없을 경우
        if user_input == "":
            ai_answer = "질문에 답변을 해주세요"
            return ai_answer
        
        # 꼬리 질문일 경우 사용자 답변을 기반으로 질문을 생성
        if not question:
            system_input = "You are a helpful Mock Interviewer. Your task is to generate thoughtful and relevant one interview question in Korean based on the provided User Input."
            self.history_update("system", system_input)            
            # ai_answer = "꼬리질문이다이"
            
            response = self.client.chat.completions.create(
                model = self.model,
                messages=self.chat_history,
                max_tokens=self.max_tokens,
                # n=1,
                temperature=self.temperature
            )
            ai_answer = response.choices[0].message.content
            self.history_update("assistant", ai_answer)
            self.real_history_update("Q", ai_answer)
        # 꼬리 질문이 아닐 경우 질문 리스트에서 가져온 질문 사용
        else:
            ai_answer = question
            self.history_update("assistant", ai_answer)
            self.real_history_update("Q", ai_answer)
        return ai_answer
    
    def generate_summary(self):
        # 디버깅용 
        self.real_history = """
Q: 안녕하세요, 자기소개 해주세요.
A: 안녕하세요, 이번에 금융결제원에 지원한 홍길동입니다.

Q. 어떤 기술이나 지식을 통해 금융결제원에서 제공하는 서비스를 개선하고자 하는 것으로 귀결되었나요? 어떤 기술적 도전에 직면하여 어떻게 극복했나요?
A: 제가 공부한 Java programming을 통해 금융결제원에서 제공하는 UI 서비스를 개선하고자 합니다.

Q. 금융결제원의 서비스를 통해 안전성과 편리함을 느낀 부분에 대해 좀 더 구체적으로 설명해 주실 수 있을까요? 실제 사용자 입장에서 어떤 점이 특히 강조되는가요?
A. 실제 사용자 입장에서 금융결제원의 보안에 안전성을 느낀 적 있습니다. 또한 UI가 체계적이라 편리함을 느꼈습니다."""
        if not self.is_interviewed(): return
        response = self.client.chat.completions.create(
            model = self.model,
            messages=[
                {"role": "system", "content": "You are a helpful Mock Interviewer.\n\
                    Look at the following whole conversation and give me a summary in korean.\n\
                    Number the summary and write it in sentences.\n\
                    Put a line between each sentence."},
                {"role": "user", "content": self.real_history},
            ],
            max_tokens=self.max_tokens,
            temperature=self.temperature
        )
        summary = response.choices[0].message.content
        print("서머리리: ", summary)
        return summary
    
    def evaluate_interview(self):
        # 디버깅용 
        self.real_history = """
Q: 안녕하세요, 자기소개 해주세요.
A: 안녕하세요, 이번에 금융결제원에 지원한 홍길동입니다.

Q. 어떤 기술이나 지식을 통해 금융결제원에서 제공하는 서비스를 개선하고자 하는 것으로 귀결되었나요? 어떤 기술적 도전에 직면하여 어떻게 극복했나요?
A: 제가 공부한 Java programming을 통해 금융결제원에서 제공하는 UI 서비스를 개선하고자 합니다.

Q. 금융결제원의 서비스를 통해 안전성과 편리함을 느낀 부분에 대해 좀 더 구체적으로 설명해 주실 수 있을까요? 실제 사용자 입장에서 어떤 점이 특히 강조되는가요?
A. 실제 사용자 입장에서 금융결제원의 보안에 안전성을 느낀 적 있습니다. 또한 UI가 체계적이라 편리함을 느꼈습니다."""
        if not self.is_interviewed(): return
        response = self.client.chat.completions.create(
            model = self.model,
            messages=[
                {"role": "system", "content": "You are a helpful Mock Interviewer.\n\
                    Look at the following whole conversation and give me an evaluation.\n\
                    Give a maximum of 5 score according to each evaluation criteria and explain why in korean.\n\
                    Here are five evaluation criteria.\n\n\
                    1. Is the answer based on the cover letter? ([your_score]/5)\n\
                    2. Is the clarity and logic of the answers to the given questions appropriate? ([your_score]/5)\n\
                    3. Is the interviewer's ability to understand the point of the question appropriate? ([your_score]/5)\n\
                    4. Is your major knowledge (technical) utilization ability, related work experience, and skill level sufficient? ([your_score]/5)\n\
                    5. Is creativity, willpower and developability (self-improvement needs), vision, and future plans well described? ([your_score]/5)\n\n\
                    After evaluation, generate the overall evaluation and calculate the average score"},
                {"role": "user", "content": self.real_history},
            ],
            max_tokens=self.max_tokens,
            temperature=self.temperature
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
        if self.real_history == "":
            self.text_box.insert(tk.END, "대화 내용이 없습니다. 먼저 Mock Interview를 진행해주세요.\n")
            return False
        else:
            print("인터뷰 내용 있음!!")
            print(self.real_history)
            return True
        
    # def get_PersonalStatement(self, txt_path):
    #     personal_statement = ""
    #     with open(txt_path, 'r', encoding='utf-8') as fp:
    #         lines = fp.readlines()
    #         for line in lines:
    #             personal_statement += line
    #     return personal_statement