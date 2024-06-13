import os
from openai import OpenAI
from gui_utils import *
from gpt_utils import *
from fine_tuning import *
from connect_db import *
import pygame
import tkinter as tk

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
        
        self.text_box = tk.Text(self.root, height=32, width=85, bg="lightyellow")
        self.text_box.pack()
        self.text_box.insert("1.10", "[면접 내용은 여기에 기록됩니다]\n")
        
        self.intro_box = tk.Text(self.root, height=12, width=40, bg="#FFB6C1")
        self.intro_box.place(x=50, y=520)
        self.intro_box.insert("1.0", "[사용법]\n")
        self.intro_box.tag_configure("center", justify='center')
        self.intro_box.tag_add("center", "1.0", "2.0")
        
        self.intro_box.tag_configure("left", justify='center')
        self.intro_box.tag_add("left", "2.0", "5.0")
        self.intro_box.insert(tk.END, "1. 자기소개서 추가\n2. 면접 시작\n3. 면접 종료 후 요약 및 평가 확인\n\n")
        
        self.intro_box.insert(tk.END, "[맞춤형 면접관 생성 및 사용 방법]\n")
        self.intro_box.tag_configure("center", justify='center')
        self.intro_box.tag_add("center", "6.0", "7.0")
        
        self.intro_box.tag_configure("left", justify='center')
        self.intro_box.tag_add("left", "7.0", "end")
        self.intro_box.insert(tk.END, "1. 면접 내용 수집 동의 후 면접 진행\n2. 맞춤형 면접관 생성 클릭\n3. 맞춤형 면접관 사용 체크\n")
        self.intro_box.config(state="disabled")

        # 버튼을 배치할 프레임 생성
        frame_color = "#DDA0DD"
        self.whole_frame = tk.Frame(self.root, bg=frame_color)
        self.whole_frame.pack(side=tk.RIGHT, padx=80, pady=10)
        
        self.button_frame = tk.Frame(self.whole_frame, bg=frame_color)
        self.button_frame.pack(side=tk.BOTTOM, padx=10, pady=10)

        self.button_frame3 = tk.Frame(self.whole_frame, bg=frame_color)
        self.button_frame3.pack(side=tk.TOP, padx=10, pady=10)
        
        # 디버깅용 프레임
        self.button_frame2 = tk.Frame(self.root, bg='gray')
        self.button_frame2.pack(side=tk.BOTTOM, fill=tk.BOTH, padx=10, pady=10)    
        
        # 체크박스 생성
        self.var1 = tk.IntVar()
        self.checkbox1 = tk.Checkbutton(self.button_frame3, text="면접 내용 수집에 동의", variable=self.var1, bg="#FFDAB9")
        self.checkbox1.grid(row=0, padx=5, pady=5, sticky="nsew")
        
        # 제거할것
        # self.var2 = tk.IntVar()
        # self.checkbox2 = tk.Checkbutton(self.button_frame3, text="사용자 맞춤형 면접관 사용", variable=self.var2, bg="#FFDAB9")
        # self.checkbox2.grid(row=1, padx=5, pady=5)
        
        self.gt = Chatbot(root, self.text_box)
        self.db = ConnectDB()
        self.ft = FineTuning(self.gt.client)
        self.ut = Gui_utils(root, self.text_box, self.var1, self.gt, self.db, self.ft)
        # self.ut = Gui_utils(root, self.text_box, self.var1, self.var2, self.gt, self.db)
        
        # 버튼 생성 및 그리드 배치
        self.button_start = tk.Button(self.button_frame, text="면접 시작", 
                                      command=self.ut.start_interview, bg="#FF6666", width=12, height=2)
        self.button_start.grid(row=2, column=0, padx=5, pady=5)

        self.button_s = tk.Button(self.button_frame, text="자소서 추가", 
                                  command=self.ut.add_PersonalStatement, bg="#E6E6FA", width=12, height=2)
        self.button_s.grid(row=2, column=1, padx=5, pady=5)
        
        # self.button_make_mock = tk.Button(self.button_frame, text="맞춤형 면접관 사용", 
        #                                   command=self.ut.make_customized_mock_interviewer, bg="#FFDAB9", width=14, height=2)
        # self.button_make_mock.grid(row=3, column=0, padx=5, pady=5)
        self.button_make_mock = tk.Button(self.button_frame, text="맞춤형 면접관", 
                                          command=self.ut.select_fine_tuning, bg="#FFDAB9", width=14, height=2)
        self.button_make_mock.grid(row=3, column=0, padx=5, pady=5)        
        
        self.button_interview_history = tk.Button(self.button_frame, text="면접 내용 확인", 
                                                  command=lambda: self.ut.show_chat_history(self.gt.real_history), bg="lightgreen", width=12, height=2)
        self.button_interview_history.grid(row=3, column=1, padx=5, pady=5)
        
        self.button_interview_summary = tk.Button(self.button_frame, text="면접 요약 확인", 
                                                  command=self.ut.show_summary, bg="lightgreen", width=12, height=2)
        self.button_interview_summary.grid(row=4, column=0, padx=5, pady=5)
        
        self.button_interview_evaluate = tk.Button(self.button_frame, text="면접 내용 평가", 
                                                   command=self.ut.show_evaluation, bg="lightgreen", width=12, height=2)
        self.button_interview_evaluate.grid(row=4, column=1, padx=5, pady=5)
        
        self.button_t = tk.Button(self.button_frame2, text="chat_history 확인", 
                                  command=lambda: print("chat_history:",self.gt.chat_history))
        self.button_t.pack(pady=2)
        
        self.button_t2 = tk.Button(self.button_frame2, text="questions 확인", 
                                   command=lambda: print("question_list:",self.ut.question_list))
        self.button_t2.pack(pady=2)
        
        self.testb = tk.Button(self.button_frame2, text="DB에 데이터 넣기 버튼", 
                               command=self.ut.save_chat_history)
        self.testb.pack(pady=2)
        
        self.testb2 = tk.Button(self.button_frame2, text="DB에서 데이터 읽기 버튼", 
                                command=self.db.select_interview_data)
        self.testb2.pack(pady=2)
        
        # self.button_frame.columnconfigure(0, weight=1)
        # self.button_frame.columnconfigure(1, weight=0)
        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)
        self.button_frame.rowconfigure(0, weight=1)
        self.button_frame.rowconfigure(1, weight=1)
        self.button_frame.rowconfigure(2, weight=1)
        
    def test(self):
        print("yesgogo!!!!!!!!")
        
# 메인 윈도우 생성
root = tk.Tk()
label = tk.Label(root, text="Mock Interviewer", bg="lightblue", fg="black", font=("Helvetica", 16, "bold"))
label.pack(pady=10)

root.configure(bg='lightblue')
root.title("Mock Interviewer")
root.geometry("800x800")
app = Gui_app(root)
# GUI 실행
root.mainloop()
