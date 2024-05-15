from tkinter import *
from tkinter.font import Font

###예제4) ft -> cm로 바꾸는 단위 변환기 만들기
# Entry: input과 비슷한 역할 (사용자가 입력한 내용 전달)
# get: Entry를 사용한 입력 내용 가져올 수 있다.
# delete: 사용자 입력 삭제
# Frame: 컨테이너, 창 안에 프레임 생성
# grid: 격자 배치


tk = Tk()
frame = Frame(tk)
frame.pack()
font = Font(family='맑은 고딕', size=20)
tk.geometry('600x800')
tk.title('Mock Internviewer')
scrollbar = Scrollbar(frame)
scrollbar.pack(side="right", fill="y")

def Ft2Cm():
    ft2cm = entry1.get()
    entry2.delete(0,"end")
    entry2.insert(0,round(float(ft2cm)*30.48,4))
def Cm2Ft():
    cm2ft = entry2.get()
    entry1.delete(0,"end")
    entry1.insert(0,round(float(cm2ft)/30.48,4))
def human_text(text_box):
    chars = "테스트 글자입니닷"
    text_box.insert(END, chars=chars)
    # text_box.config(state='disabled')
    # text_box.pack(side="top")
    pass

def fill_text(text_box):
    text_box.insert(END, "gogo")
    # text_box.pack(side="top")
    # text_box.pack()

def temps():
    pass

label1 = Label(tk,text='피트(ft)', font=font)#.grid(row=0, column=0)
label2 = Label(tk,text='센티미터(cm)')#.grid(row=1,column=0)

# 각 단위 입력받는 부분 만들기
entry1 = Entry(tk)
entry2 = Entry(tk)


# entry1.grid(row=0,column=1)
# entry2.grid(row=1,column=1)
text_box = Text(tk, width=50, height=10)
text_box.pack(side="top")

btn1 = Button(tk,text='Create human text',bg='blue',fg='white',command=lambda: human_text(text_box))
btn2 = Button(tk,text='Create mock text',bg='black',fg='white',command=lambda: fill_text(text_box))

btn1.pack()
btn2.pack()

# scrollbar.config(command=btn1.yview)

tk.mainloop()