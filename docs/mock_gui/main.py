import os
from openai import OpenAI
from gui_utils import *
from gpt_utils import *
from connect_db import *
import pygame

pygame.mixer.init()
# 색상 설정
colors = {
    "Pale Pink": "#FFB6C1",
    "Mint Green": "#98FF98",
    "Lavender": "#E6E6FA",
    "Peach": "#FFDAB9",
    "Soft Yellow": "#FFFACD",
    "Coral": "#F08080",
    "Powder Blue": "#B0E0E6",
    "Blush Pink": "#F4C2C2",
    "Pastel Purple": "#DDA0DD",
    "Soft Beige": "#F5F5DC"
}

class Gui_app:
    def __init__(self, root):
        self.root = root
        
        self.text_box = tk.Text(self.root, height=35, width=90, bg="lightyellow")
        self.text_box.pack()  # 상하 여백 추가
        # self.temp_box = tk.Text(self.root)

        # 체크박스 생성
        self.var1 = tk.IntVar()
        self.checkbox1 = tk.Checkbutton(root, text="면접 내용 수집에 동의(맞춤형 면접 제공)", variable=self.var1, bg="#FFDAB9")
        self.checkbox1.place(x=455, y=519)
        # 체크박스 체크햇는지 확인은 .get() 으로 확인, 0(체크해제) 1(체크)
        
        self.var2 = tk.IntVar()
        self.checkbox2 = tk.Checkbutton(root, text="사용자 맞춤형 면접관 사용", variable=self.var2, bg="#FFDAB9")
        self.checkbox2.place(x=180, y=519)
                
        self.gt = Chatbot(root, self.text_box)
        self.db = ConnectDB()
        self.ut = Gui_utils(root, self.text_box, self.var1, self.var2, self.gt, self.db)

        # self.button_temp = tk.Button(self.root, text="Test input", 
        #                               command = lambda: print("hihi"))
        # self.button_temp.pack(pady=10)  # 상하 여백 추가
        
        """
        1. 자소서 입력(자소서 항목 당 질문 생성 + 첫 질문(자기소개 요청))
        2. 면접 시작
        """
        self.button_start = tk.Button(self.root, text="Start", 
                                      command = self.ut.start_interview, bg="#FFB6C1")
        self.button_start.pack(pady=10)  # 상하 여백 추가

        self.button_s = tk.Button(self.root, text="자소서 추가", 
                                  command = self.ut.add_PersonalStatement, bg="#E6E6FA")
        self.button_s.pack(pady=10)  # 상하 여백 추가
        
        self.button_make_mock = tk.Button(self.root, text="맞춤형 면접관 생성", 
                                  command = self.ut.make_customized_mock_interviewer, bg="#FFDAB9")
        self.button_make_mock.place(x=465, y=565)  # 상하 여백 추가
        
        self.button_interview_history = tk.Button(self.root, text="면접 전체 내용 확인", 
                                  command = lambda: self.ut.show_chat_history(self.gt.real_history), bg="lightgreen")
        self.button_interview_history.place(x=210, y=611)  # 상하 여백 추가

        self.button_interview_summary = tk.Button(self.root, text="면접 요약 확인", 
                                        command = self.ut.show_summary, bg="lightgreen")
        self.button_interview_summary.pack(pady=10)  # 상하 여백 추가
        
        self.button_interview_evaluate = tk.Button(self.root, text="면접 내용 평가", 
                                        command = self.ut.show_evaluation, bg="lightgreen")
        self.button_interview_evaluate.place(x=470, y=611)  # 상하 여백 추가
        
        self.button_t = tk.Button(self.root, text="chat_history 확인", 
                                  command = lambda: print("chat_history:",self.gt.chat_history))
        self.button_t.pack(pady=10)  # 상하 여백 추가
        
        self.button_t2 = tk.Button(self.root, text="questions 확인", 
                                  command = lambda: print("question_list:",self.ut.question_list))
        self.button_t2.pack(pady=10)  # 상하 여백 추가
        
        self.testb = tk.Button(self.root, text="DB에 데이터 넣기 버튼", 
                                  command = self.ut.save_chat_history)
        self.testb.pack()
        
        self.testb2 = tk.Button(self.root, text="DB에서 데이터 읽기 버튼", 
                                  command = self.db.select_interview_data)
        self.testb2.pack()        

                        
    def test(self):
        print("yesgogo!!!!!!!!")
        
# 메인 윈도우 생성
root = tk.Tk()
label = tk.Label(root, text="Mock Interviewer", bg="lightblue", fg="black", font=("Helvetica", 16, "bold"))

label.pack(pady=10)

# frame = tk.Frame(root, bg="yellow", bd=5)
# frame.pack(padx=10, pady=10)
root.configure(bg='lightblue')
root.title("Mock Interviewer")
root.geometry("800x800")
app = Gui_app(root)
# GUI 실행
root.mainloop()