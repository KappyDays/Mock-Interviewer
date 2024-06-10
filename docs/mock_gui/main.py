import os
from openai import OpenAI
from gui_utils import *
from gpt_utils import *
import pygame

pygame.mixer.init()

class Gui_app:
    def __init__(self, root):
        self.root = root
        
        self.text_box = tk.Text(self.root, height=40, width=90)
        self.text_box.pack(pady=20)  # 상하 여백 추가
        # self.temp_box = tk.Text(self.root)
        
        self.gt = Chatbot(root, self.text_box)
        self.ut = Gui_utils(root, self.text_box, self.gt)

        # self.button_temp = tk.Button(self.root, text="Test input", 
        #                               command = lambda: print("hihi"))
        # self.button_temp.pack(pady=10)  # 상하 여백 추가
        
        """
        1. 자소서 입력(자소서 항목 당 질문 생성 + 첫 질문(자기소개 요청))
        2. 면접 시작
        """
        self.button_start = tk.Button(self.root, text="Start", 
                                      command = self.ut.start_interview)
        self.button_start.pack(pady=10)  # 상하 여백 추가

        self.button_s = tk.Button(self.root, text="자소서 추가", 
                                  command = self.ut.add_PersonalStatement)
        self.button_s.pack(pady=10)  # 상하 여백 추가

        self.button_t = tk.Button(self.root, text="chat_history 확인", 
                                  command = lambda: print("chat_history:",self.gt.chat_history))
        self.button_t.pack(pady=10)  # 상하 여백 추가
        
        self.button_t2 = tk.Button(self.root, text="questions 확인", 
                                  command = lambda: print("question_list:",self.ut.question_list))
        self.button_t2.pack(pady=10)  # 상하 여백 추가        

        self.button_interview_history = tk.Button(self.root, text="면접 전체 내용 확인", 
                                  command = lambda: self.ut.show_chat_history(self.gt.real_history))
        self.button_interview_history.pack(pady=10)  # 상하 여백 추가

        self.button_interview_summary = tk.Button(self.root, text="면접 요약 확인", 
                                        command = lambda: print("Ai_interview_summary:\n", self.gt.generate_summary()))
        self.button_interview_summary.pack(pady=10)  # 상하 여백 추가
        
        self.button_interview_evaluate = tk.Button(self.root, text="면접 내용 평가", 
                                        command = lambda: self.ut.show_evaluation(self.gt.chat_history))
        self.button_interview_evaluate.pack(pady=10)  # 상하 여백 추가
                        
    def test(self):
        print("yesgogo!!!!!!!!")
        
# 메인 윈도우 생성
root = tk.Tk()
root.title("Mock Interviewer")
root.geometry("800x900")
app = Gui_app(root)
# GUI 실행
root.mainloop()