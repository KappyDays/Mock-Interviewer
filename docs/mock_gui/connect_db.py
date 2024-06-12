import sqlite3

class ConnectDB:
    def __init__(self):
        print("DB연결 완료")
        self.conn = sqlite3.connect('mock_interview2.db')
        self.cursor = self.conn.cursor()
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS interview_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    # 데이터 삽입 함수
    def insert_interview_data(self, question, answer):
        print("데이터를 삽입합니다.!")
        
        self.cursor.execute('''
            INSERT INTO interview_data (question, answer)
            VALUES (?, ?)
        ''', (question, answer))
        self.conn.commit()
        
    def select_interview_data(self):
        self.cursor.execute('SELECT question, answer FROM interview_data')
        rows = self.cursor.fetchall()
        
        questions = []
        answers = []

        # 결과를 변수에 저장
        for row in rows:
            question, answer = row
            questions.append(question)
            answers.append(answer)

        # 데이터 출력 (확인용)
        print("Questions:")
        for q in questions:
            print(q)

        print("\nAnswers:")
        for a in answers:
            print(a)