import queue
import pygame
import numpy as np
import sounddevice as sd
import soundfile as sf

pygame.mixer.init()

def record_question():
    record_order = 10
    # 녹음 설정 값
    silence_threshold = 1.0  # 침묵 임계값 설정
    max_silence_blocks = 100  # 연속 침묵을 허용하는 블록 수
    silence_counter = 0  # 침묵 블록 카운터 초기화
    q = queue.Queue()  # 오디오 데이터를 저장할 큐
    
    # 녹음 저장 파일 설정
    UserSpeech_filename = "UserSpeech_" + str(record_order) + ".wav"
    record_order += 1
    
    # 녹음 시작 효과음
    pygame.mixer.music.load('beep.wav')
    pygame.mixer.music.play()     
    while pygame.mixer.music.get_busy():
        continue  # MP3 재생이 끝날 때까지 기다림
    
    # 녹음 함수들
    def audio_callback(indata, frames, time, status):
        """이 콜백은 새로운 오디오 데이터가 도착할 때마다 호출됩니다."""
        nonlocal silence_counter
        volume_norm = np.linalg.norm(indata) * 10
        print(f"Volume: {volume_norm:.2f}")  # 볼륨 수준 출력 (디버깅 목적)
        if volume_norm < silence_threshold:
            nonlocal silence_counter
            silence_counter += 1
        else:
            silence_counter = 0
        if silence_counter >= max_silence_blocks:
            raise sd.CallbackStop  # 침묵이 지속되면 콜백 중지
        q.put(indata.copy())  # 큐에 오디오 데이터 추가

    def recording_thread():
        print("레코드시작")
        try:
            # 기본 오디오 장치 정보 출력
            print("Default input device:", sd.query_devices(kind='input'))            

            # 오디오 장치의 기본 샘플링 레이트 가져오기
            device_info = sd.query_devices(sd.default.device, 'input')
            samplerate = int(device_info['default_samplerate'])            

            with sd.InputStream(callback=audio_callback, samplerate=samplerate, channels=2, device=0) as stream:
                print("레코드시작2")
                with sf.SoundFile(UserSpeech_filename, mode='w', samplerate=samplerate, channels=2, subtype="PCM_16") as file:
                    print("레코드시작3")
                    while True:
                        try:
                            print("레코드시작4")
                            data = q.get(timeout=1)  # 1초 타임아웃 설정
                            file.write(data)
                        except queue.Empty:
                            print("레코드루프종료")
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
    print("녹음 시작안하나요?")
    recording_thread()

record_question()
print(sd.query_devices())
# print(sd.query_devices(sd.default.device, 'input'))