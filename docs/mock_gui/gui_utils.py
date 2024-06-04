import tkinter as tk
from tkinter import Toplevel, Label, Entry, Button, Text, messagebox, filedialog
from gpt_utils import *
import pdb
import pygame
import time
import soundfile as sf
import threading
import sounddevice as sd
import numpy as np
import queue

class Gui_utils:
    def __init__(self, root, text_box, chatbot:Chatbot):
        self.root = root
        self.question_queue = queue.Queue()
        self.text_box = text_box
        
        self.record_order = 0
        self.ai_answer_order = 0
        
        self.ai_reply = "" #디버깅, None
        self.question_list = []
        self.question_count = 0
        self.all_qc = 0
        
        self.cb = chatbot
        self.requestion = False
        
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
        
    def open_custom_dialog(self):
        # qs = self.cb.get_PersonalStatement('simple_questions.txt').replace("\n\n", "\n")
        # self.question_list = qs.split('\n')
        # self.question_list = list(reversed(self.question_list))
        # print("퀘리개수: ", len(self.question_list))
        # self.ai_answer = "안녕하십니까, 자기소개를 해주세요.\n"
        # return 
        def submit(input_box):
            user_input = input_box.get("1.0", "end-1c")
            if user_input:
                popup = self.show_temporary_alert(self.root, "자기소개서 처리 중...", delay=2000)
                popup.after(2000, popup.destroy)
                
                self.question_list = self.cb.generate_ps_questions(user_input)
                self.ai_reply = "안녕하십니까, 자기소개를 해주세요.\n"
                dialog.destroy()
            else:
                messagebox.showinfo("Alert", "자기소개서를 입력해 주세요.")

        # 새 대화창 생성
        dialog = Toplevel(self.root)
        dialog.title("Input")
        dialog.geometry("400x400")  # 대화창 크기 설정

        # 라벨 생성
        label = Label(dialog, text="자기소개서를 입력해 주세요.")
        label.pack(pady=10)

        # 텍스트 입력 필드 생성
        input_box = Text(dialog, height=10, width=40)
        # entry = Entry(dialog, width=25)
        # entry.pack(pady=5)
        input_box.pack(pady=5)

        # 제출 버튼 생성
        submit_button = Button(dialog, text="Submit", command=lambda: submit(input_box))
        submit_button.pack(pady=10)
        
    def start_interview(self):
        # 자소서를 입력해야 open_custom_dialog함수에서 ai의 질문이 생성됨
        if self.question_list == []:
            self.text_box.insert(tk.END, "먼저 자기소개서를 입력해 주세요.\n")
            return 
        
        # for first question
        print("start_interview questions, ai_answer: ", self.ai_reply, "\n")
        ai_speech_path = self.cb.make_tts(self.ai_answer) # 디버깅 위해 임시 주석
        # ai_speech_path = "AiSpeech_0.mp3" #디버깅용
        self.ask_question(self.ai_reply, ai_speech_path)
        # self.root.after(1000, lambda: self.response_question(filename=self.record_filename))
        return
    
    def ask_question(self, query, ai_speech_path):
        self.text_box.insert(tk.END, f"Q: {query}" + "\n")
        self.right_align()
        
        self.play_tts(ai_speech_path)

    def play_tts(self, filename):
        if filename:
            print(f"Loaded {filename}..")
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                continue  # MP3 재생이 끝날 때까지 기다림
        else:
            print("No file loaded")
        self.root.after(2000, self.record_question)

    def record_question(self):
        print("유저텍스트:", "가보자고")
        # user_text = "Test Textinput22"#make_stt(filename)
        self.text_box.insert(tk.END, "A: " + "가보자고" + "\n")
        
        # 답변을 통해 query, tts 생성하고 인자 넘겨주기
        # self.proceed_conversation("가보자고")
        # return 
        
        # 녹음 설정 값
        silence_threshold = 1.0  # 침묵 임계값 설정
        max_silence_blocks = 100  # 연속 침묵을 허용하는 블록 수
        silence_counter = 0  # 침묵 블록 카운터 초기화
        q = queue.Queue()  # 오디오 데이터를 저장할 큐
        
        # 녹음 저장 파일 설정
        UserSpeech_filename = "UserSpeech_" + str(self.record_order) + ".wav"
        self.record_order += 1
        
        # 녹음 시작 효과음
        pygame.mixer.music.load('beep.wav')
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
        self.text_box.insert(tk.END, "A: " + user_text + "\n")
        
        # 답변을 통해 query, tts 생성하고 인자 넘겨주기
        self.proceed_conversation(user_text)

    def proceed_conversation(self, user_text):
        # 자소서 기반 질문이 끝나고, reply까지 완료하면 면접 종료
        if self.question_list == [] and self.all_qc % 2 != 0:
            self.text_box.insert(tk.END, "\n면접이 종료되었습니다. 면접 내용을 확인해주세요.\n")
            return
        
        # 답변을 통해 query, tts 생성하고 인자 넘겨주기
        if self.all_qc % 2 == 0: # 꼬리 질문을 생성해서 사용
            ai_text = self.cb.generate_response(user_text)
        else: # 미리 생성된 자소서 기반 질문 사용
            ai_text = self.cb.generate_response(user_text, self.question_list.pop())
        self.all_qc += 1
        
        ai_speech_path = self.cb.make_tts(ai_text)
        # ai_speech_path = "C:/workspace/docs/mock_gui/AiSpeech_0.mp3"
        self.root.after(3000, lambda: self.ask_question(ai_text, ai_speech_path))
        
        return ai_speech_path

    def show_chat_history(self, history):
        # 새 대화창 생성
        dialog = Toplevel(self.root)
        dialog.title("Input")
        dialog.geometry("500x500")  # 대화창 크기 설정

        # 라벨 생성
        label = Label(dialog, text="면접 히스토리 확인")
        label.pack(pady=10)

        # 텍스트 입력 필드 생성
        input_box = Text(dialog, height=30, width=50)
        input_box.pack(pady=5)
        input_box.insert(tk.END, history)

        # 확인 버튼 생성
        submit_button = Button(dialog, text="확인", command=lambda: dialog.destroy())
        submit_button.pack(pady=10)
        
    def right_align(self):
        new_end = self.text_box.index("end-1c")
        tag_name = 'right' + new_end.replace('.', '_')
        self.text_box.tag_add(tag_name, new_end + "-1l linestart", new_end)
        self.text_box.tag_configure(tag_name, justify='right')