import os
from openai import OpenAI
from gui_utils import *
from gpt_utils import *
import pygame

pygame.mixer.init()

class Gui_app:
    def __init__(self, root):
        self.root = root
        
        self.text_box = tk.Text(self.root, height=35, width=80)
        self.text_box.pack(pady=20)  # 상하 여백 추가
        self.text_box.insert(tk.END, "안녕하세요. 모의 면접 프로그램입니다. 자소서를 추가한 후 면접을 시작해 주세요.\n")
        # self.temp_box = tk.Text(self.root)
        
        self.gt = Chatbot(root, self.text_box)
        self.ut = Gui_utils(root, self.text_box, self.gt)
        
        self.button_start = tk.Button(self.root, text="면접 시작", 
                                      command = self.ut.start_interview)
        self.button_start.pack(pady=10)  # 상하 여백 추가

        self.button_s = tk.Button(self.root, text="자소서 추가", 
                                  command = self.ut.open_custom_dialog)
        self.button_s.pack(pady=10)  # 상하 여백 추가

        self.button_t = tk.Button(self.root, text="전체 면접 내용 확인", 
                                  command = self.ut.open_custom_dialog2)
                                #   command = lambda: print("Ai_text_check:",self.ut.ai_answer))
        self.button_t.pack(pady=10)  # 상하 여백 추가

        self.button_interview_summary = tk.Button(self.root, text="면접 요약", 
                                        command = lambda: print("Ai_interview_summary:\n", self.gt.generate_summary()))
        self.button_interview_summary.pack(pady=10)  # 상하 여백 추가
        
        self.button_interview_history = tk.Button(self.root, text="면접 분석", 
                                  command = lambda: print("Ai_interview_history:\n", self.gt.chat_history))
        self.button_interview_history.pack(pady=10)  # 상하 여백 추가
        
        
        self.button_interview_history = tk.Button(self.root, text="표정 분석", 
                                  command = lambda: print("Ai_interview_history:\n", self.gt.chat_history))
        self.button_interview_history.pack(pady=20)  # 상하 여백 추가
        
        self.button_interview_history = tk.Button(self.root, text="말투 분석", 
                                  command = lambda: print("Ai_interview_history:\n", self.gt.chat_history))
        self.button_interview_history.pack(pady=10)  # 상하 여백 추가                

                        
    def test(self):
        print("yesgogo!!!!!!!!")
        
# 메인 윈도우 생성
root = tk.Tk()
root.title("Mock Interviewer")
root.geometry("700x900")
app = Gui_app(root)
# GUI 실행
root.mainloop()