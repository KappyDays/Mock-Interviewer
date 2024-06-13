import openai
import time
from connect_db import *
import json

class FineTuning:
    def __init__(self, client):
        self.client = client
        self.openai = openai
        self.connect_db = ConnectDB()
        self.dataset_path = "user_data/training_data.jsonl"
        self.response = None
        
    def make_fine_tuning_data(self):
        questions, answers = self.connect_db.select_interview_data()

        # 데이터가 10개 미만인 경우 학습이 안됨        
        if len(questions) < 10:
            return "insufficient"
        
        with open(self.dataset_path, "w", encoding="utf-8") as f:
            for q, a in zip(questions, answers):
                data = {"messages": [{"role": "system", "content": "You are a competent mock interviewer, and you must answer in Korean. The conversation we are having now is the expected questions of the interview and answers to them. The question asks about your school days and what you gained from them. It is better not to end with mere boasting but to explain what you learned and how you grew. Topics that can impress the interviewer are desirable."}, 
                                     {"role": "user", "content": q}, 
                                     {"role": "assistant", "content": a}]}
                json_string = json.dumps(data, ensure_ascii=False)
                f.write(json_string + "\n")
        return "success"
    
    # 1. 데이터 업로드
    def upload_file(self, file_path):
        # 새로운 API에 맞게 파일 업로드
        with open(file_path, "rb") as f:
            response = self.client.files.create(
                file=f,
                purpose='fine-tune'
            )
        file_id = response.id
        return file_id

    # 2. 파인튜닝 작업 시작
    def create_fine_tune(self, file_id, model='gpt-3.5-turbo'):
        response = self.client.fine_tuning.jobs.create(
            training_file=file_id,
            model=model
        )
        fine_tune_id = response.id
        return fine_tune_id

    # 3. 파인튜닝 작업 상태 확인
    def check_fine_tune_status(self, fine_tune_id):
        while True:
            response = self.client.fine_tuning.jobs.retrieve(fine_tune_id)
            status = response.status
            print(f"Fine-tuning status: {status}")
            
            if status in ["succeeded", "failed"]:
                self.response = response
                return response
            
            time.sleep(30)  # 1분 대기 후 상태 재확인
            
    def get_fine_tuned_model(self):
        if self.response != None:
            return self.response.fine_tuned_model
        else:
            return None