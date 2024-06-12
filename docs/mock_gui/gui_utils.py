import tkinter as tk
from tkinter import Toplevel, Label, Entry, Button, Text, messagebox, filedialog
from gpt_utils import *
from connect_db import *
import pdb
import pygame
import time
import soundfile as sf
import threading
import sounddevice as sd
import numpy as np
import queue

class Gui_utils:
    def __init__(self, root, text_box, var1, var2, chatbot:Chatbot, db:ConnectDB):
        self.root = root
        self.question_queue = queue.Queue()
        self.text_box = text_box
        
        self.record_order = 0
        self.ai_answer_order = 0
        
        self.ai_reply = "" #디버깅, None
        self.question_list = []
        self.question_count = 0
        self.all_qc = 1
        
        self.cb = chatbot
        self.db = db
        self.requestion = False
        
        self.var1 = var1
        self.var2 = var2
        
    def show_temporary_alert(self, window, message, delay=2000):
        # 메시지를 보여주는 팝업 창 생성
        popup = tk.Toplevel(window)
        popup.title("Alert")
        popup.geometry("200x100")  # 창 크기 설정

        # 메시지 라벨 추가
        message_label = tk.Label(popup, text=message)
        message_label.pack(pady=20, padx=20)

        # 지정된 시간(delay) 후에 팝업 창 닫기
        return popup

    def add_hello(self, text_widget, alignment):
        # 새로운 텍스트를 끝에 추가
        current_end = text_widget.index("end-1c")
        text_widget.insert(tk.END, "Hello World!\n")
        new_end = text_widget.index("end-1c")
        
        # 텍스트를 지정된 정렬 방식으로 설정
        tag_name = alignment + current_end  # 각 태그에 고유 이름을 부여
        text_widget.tag_add(tag_name, current_end, new_end)
        text_widget.tag_configure(tag_name, justify=alignment)
        
    def add_PersonalStatement(self):
        def submit(input_box):
            user_input = input_box.get("1.0", "end-1c")
            if user_input:
                self.show_temporary_alert(self.root, "자기소개서 처리 중...", delay=2000)
                # popup = self.show_temporary_alert(self.root, "자기소개서 처리 중...", delay=2000)
                # popup.after(2000, popup.destroy)
                
                # 자소서 항목당 질문 2개씩 생성
                self.question_list = self.cb.generate_ps_questions(user_input)
                
                # 모의 면접관의 첫 질문 
                self.ai_reply = "안녕하십니까 지원자님. 자기소개를 해주세요."
                self.cb.real_history_update("Q", self.ai_reply)
                dialog.destroy()
            else:
                messagebox.showinfo("Alert", "자기소개서를 입력해 주세요.")

        # 새 대화창 생성
        dialog = Toplevel(self.root)
        dialog.title("Add Personal Statement")
        dialog.geometry("600x700")  # 대화창 크기 설정
        dialog.configure(bg='lightblue')

        # 라벨 생성
        label = Label(dialog, text="자기소개서를 입력해 주세요.", bg="lightblue", fg="black", font=("Helvetica", 16, "bold"))
        label.pack(pady=10)

        # 텍스트 입력 필드 생성
        input_box = Text(dialog, height=40, width=70, bg="lightyellow")
        # entry = Entry(dialog, width=25)
        # entry.pack(pady=5)
        input_box.pack(pady=5)

        # 제출 버튼 생성
        submit_button = Button(dialog, text="Submit", command=lambda: submit(input_box), bg="#FFB6C1")
        submit_button.pack(pady=10)
        
    def start_interview(self):
        # 자소서를 입력해야 open_custom_dialog함수에서 ai의 질문이 생성됨
        if self.question_list == []:
            self.text_box.insert(tk.END, "먼저 자기소개서를 입력해 주세요.\n")
            return 
        
        # for first question
        print("start_interview questions, ai_answer: ", self.ai_reply, "\n")
        ai_speech_path = self.cb.make_tts(self.ai_reply) # 디버깅 위해 임시 주석
        # ai_speech_path = "AiSpeech_0.mp3" #디버깅용
        self.ask_question(self.ai_reply, ai_speech_path)
        # self.root.after(1000, lambda: self.response_question(filename=self.record_filename))
        # self.play_tts(ai_speech_path)
        # self.root.after(2000, self.record_question)
        return
    
    def ask_question(self, query, ai_speech_path):
        self.text_box.insert(tk.END, f"Q: {query}" + "\n")
        self.right_align()
        
        self.play_tts(ai_speech_path)

    def play_tts(self, filename, record=True):
        if filename:
            print(f"Loaded {filename}..")
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                continue  # MP3 재생이 끝날 때까지 기다림
        else:
            print("No file loaded")
        if record:
            self.root.after(2000, self.record_question)

    def record_question(self):
        # 녹음 설정 값
        silence_threshold = 1.0  # 침묵 임계값 설정
        max_silence_blocks = 50  # 연속 침묵을 허용하는 블록 수
        silence_counter = 0  # 침묵 블록 카운터 초기화
        q = queue.Queue()  # 오디오 데이터를 저장할 큐
        
        # 녹음 저장 파일 설정
        UserSpeech_filename = "UserSpeech_" + str(self.record_order) + ".wav"
        self.record_order += 1
        
        # 녹음 시작 효과음
        pygame.mixer.music.load('beep.wav')
        pygame.mixer.music.set_volume(0.2)  # 볼륨을 50%로 설정
        pygame.mixer.music.play()     
        while pygame.mixer.music.get_busy():
            continue  # MP3 재생이 끝날 때까지 기다림
        
        # 녹음 함수들
        def audio_callback(indata, frames, time, status):
            """이 콜백은 새로운 오디오 데이터가 도착할 때마다 호출됩니다."""
            volume_norm = np.linalg.norm(indata) * 10
            # print(f"Volume: {volume_norm:.2f}")  # 볼륨 수준 출력 (디버깅 목적)
            if volume_norm < silence_threshold:
                nonlocal silence_counter
                silence_counter += 1
            else:
                silence_counter = 0
            if silence_counter >= max_silence_blocks:
                raise sd.CallbackStop  # 침묵이 지속되면 콜백 중지
            q.put(indata.copy())  # 큐에 오디오 데이터 추가
        def recording_thread():
            try:
                with sd.InputStream(callback=audio_callback) as stream:
                    with sf.SoundFile(UserSpeech_filename, mode='w', samplerate=44100, channels=2, subtype="PCM_16") as file:
                        while True:
                            try:
                                data = q.get(timeout=1)  # 1초 타임아웃 설정
                                file.write(data)
                            except queue.Empty:
                                if not stream.active:
                                    break  # 스트림이 비활성화 상태이면 루프 종료                            
            except sd.CallbackStop:
                print("recording CallbackStop(except)")
                pass  # 예상되는 종료
            except Exception as e:
                print(f"Unexpected error: {e}")
            finally:
                print("recording finally")
        
        # 녹음 시작
        recording_thread()
        
        # 답변 출력 위해 stt사용
        user_text = self.cb.make_stt(UserSpeech_filename)
        print("생성된 유저텍스트:", user_text)
        # user_text = "Test Textinput22"#make_stt(filename)
        self.text_box.insert(tk.END, "A: " + user_text + "\n\n")
        
        # 답변을 통해 query, tts 생성하고 인자 넘겨주기
        self.proceed_conversation(user_text)

    def proceed_conversation(self, user_text):
        # 자소서 기반 질문이 끝나고, reply까지 완료하면 면접 종료
        if self.question_list == [] and self.all_qc % 2 == 1:
            ai_text = "네, 알겠습니다. 수고하셨습니다. 면접이 종료되었습니다. 면접 내용을 확인해주세요."
            ai_speech_path = self.cb.make_tts(ai_text)
            self.play_tts(ai_speech_path, record=False)
            self.text_box.insert(tk.END, "\n면접이 종료되었습니다. 면접 내용을 확인해주세요.\n")
            # pygame.mixer.music.load(filename)
            # pygame.mixer.music.play()
            # while pygame.mixer.music.get_busy():
            #     continue  # MP3 재생이 끝날 때까지 기다림
            
            # 면접 내용 수집에 동의한 경우, 면접 종료 후 면접 내용 저장
            if self.var1.get():
                self.save_chat_history()
            return
        
        # 답변을 통해 query, tts 생성하고 인자 넘겨주기
        if self.all_qc % 2 == 0: # 꼬리 질문을 생성해서 사용
            ai_text = self.cb.generate_response(user_text)
        else: # 미리 생성된 자소서 기반 질문 사용
            ai_text = self.cb.generate_response(user_text, self.question_list.pop())
            if self.all_qc == 1: #첫 번째 질문이면 인사 추가
                ai_text  = "네, 반갑습니다." + ai_text
        self.all_qc += 1
        
        ai_speech_path = self.cb.make_tts(ai_text)
        # ai_speech_path = "C:/workspace/docs/mock_gui/AiSpeech_0.mp3"
        self.root.after(3000, lambda: self.ask_question(ai_text, ai_speech_path))
        
        return ai_speech_path

    def save_chat_history(self):
        self.cb.real_history = "Q: 안녕하세요, 자기소개를 해주세요.\nA: 안녕하세요, 저는 김지원입니다. 대학교에서 컴퓨터공학을 전공하였고, 현재는 인공지능 개발자로 일하고 있습니다.\n\nQ: 무슨 인공지능을 개발하고 있나요?\nA: 저는 강력 인공지능을 개발하고 있습니다.\n\n"
        print(f"리얼히스토리 확인 =====\n{self.cb.real_history}")
        if self.cb.real_history == "":
            self.text_box.insert(tk.END, "면접 내용이 없습니다.\n")
            return

        temp_history = self.cb.real_history.strip().split('\n')
        temp_history = [temp for temp in temp_history if temp != '']
        print(temp_history)
        Q_list = []
        A_list = []
        for temp in temp_history:
            if temp[0] == 'Q':
                Q_list.append(temp[3:])
            elif temp[0] == 'A':
                A_list.append(temp[3:])
            else:
                print("append error")
        
        print(Q_list)        
        print(A_list)
        assert len(Q_list) == len(A_list)
        
        for i in range(len(Q_list)):
            self.db.insert_interview_data(Q_list[i], A_list[i])
            
        
    def show_chat_history(self, history):
        if history == "":
            self.text_box.insert(tk.END, "면접 내용 확인에 앞서 면접을 진행해 주세요.\n")
            return 
            
        # 새 대화창 생성
        dialog = Toplevel(self.root)
        dialog.title("Input")
        dialog.geometry("500x500")  # 대화창 크기 설정
        dialog.configure(bg='lightblue')

        # 라벨 생성
        label = Label(dialog, text="면접 내용 확인", bg="lightblue", fg="black", font=("Helvetica", 16, "bold"))
        label.pack(pady=10)

        # 텍스트 입력 필드 생성
        input_box = Text(dialog, height=30, width=50, bg="lightyellow")
        input_box.pack(pady=5)
        input_box.insert(tk.END, history)
        input_box.config(state=tk.DISABLED)

        # 확인 버튼 생성
        submit_button = Button(dialog, text="확인", command=lambda: dialog.destroy(), bg="#FFB6C1")
        submit_button.pack(pady=10)
        
    def make_customized_mock_interviewer(self): 
        # evaluation = self.cb.evaluate_interview()
            
        # 새 대화창 생성
        dialog = Toplevel(self.root)
        dialog.title("Customizing")
        dialog.geometry("600x700")  # 대화창 크기 설정
        dialog.configure(bg='lightblue')

        # 라벨 생성
        label = Label(dialog, text="모의 면접관 제작", bg="lightblue", fg="black", font=("Helvetica", 16, "bold"))
        label.pack(pady=10)
        # 텍스트 입력 필드 생성
        input_box = Text(dialog, height=35, width=70, bg="lightyellow")
        input_box.pack(pady=5)
        # input_box.insert("1.0", evaluation)
        input_box.config(state=tk.DISABLED)

        # 확인 버튼 생성
        submit_button = Button(dialog, text="확인", command=lambda: dialog.destroy(), bg="#FFB6C1")
        submit_button.pack(pady=10)
        
    def show_summary(self):
        summary = self.cb.generate_summary()
            
        # 새 대화창 생성
        dialog = Toplevel(self.root)
        dialog.title("Summary")
        dialog.geometry("600x700")  # 대화창 크기 설정
        dialog.configure(bg='lightblue')

        # 라벨 생성
        label = Label(dialog, text="면접 요약 확인", bg="lightblue", fg="black", font=("Helvetica", 16, "bold"))
        label.pack(pady=10)
        # 텍스트 입력 필드 생성
        input_box = Text(dialog, height=35, width=75, bg="lightyellow")
        input_box.pack(pady=5)
        input_box.insert("1.0", summary)
        input_box.config(state=tk.DISABLED)

        # 확인 버튼 생성
        submit_button = Button(dialog, text="확인", command=lambda: dialog.destroy(), bg="#FFB6C1")
        submit_button.pack(pady=10)
        
    def show_evaluation(self): 
        evaluation = self.cb.evaluate_interview()
            
        # 새 대화창 생성
        dialog = Toplevel(self.root)
        dialog.title("Evaluation")
        dialog.geometry("600x700")  # 대화창 크기 설정
        dialog.configure(bg='lightblue')

        # 라벨 생성
        label = Label(dialog, text="면접 평가 확인", bg="lightblue", fg="black", font=("Helvetica", 16, "bold"))
        label.pack(pady=10)
        # 텍스트 입력 필드 생성
        input_box = Text(dialog, height=35, width=70, bg="lightyellow")
        input_box.pack(pady=5)
        input_box.insert("1.0", evaluation)
        input_box.config(state=tk.DISABLED)

        # 확인 버튼 생성
        submit_button = Button(dialog, text="확인", command=lambda: dialog.destroy(), bg="#FFB6C1")
        submit_button.pack(pady=10)
        
    def right_align(self):
        new_end = self.text_box.index("end-1c")
        tag_name = 'right' + new_end.replace('.', '_')
        self.text_box.tag_add(tag_name, new_end + "-1l linestart", new_end)
        self.text_box.tag_configure(tag_name, justify='right')