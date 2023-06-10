from tkinter import *
from tkinter.ttk import *
import sv_ttk
import random
from pygame import mixer
import time
from playsound import playsound
import pandas
import tkinter.filedialog

mixer.init()

welcome = ["Were you happy yesterday?","How are you?","Feel free to play with Quizsy!","Nice to meet you!","Hi!","Hello!","(●'◡'●)","(≧▽≦)"]
y = len(welcome)-1
x = random.randint(0,y)
nowwelcome = welcome[x]

class Quiz:
    '''
    It's a quiz format of Quizsy.

    Format: test = Questions({Quiz Name}, {Quiz Author}, {Questions List}, {Answers List}, {Questions Types}, {Default Score}, {Points per question}, {Deductions?(True, False)}, {Points per wrong question}) 
    '''
    def __init__(self,name,author,questions,answers,types,defaultscore=0,defaultadd=1000,deductions=False,takeawaypoints=0):
        self.questions = questions
        self.answers = answers
        self.name = name
        self.author = author
        self.defaultscore = defaultscore
        self.defaultadd = defaultadd
        self.deductions = deductions
        self.takeawaypoints = takeawaypoints
        self.types = types


class QuizsyClientUI:
    def __init__(self,lang,studiomode=False):
        self.lang=lang
        self.studiomode=studiomode
        self.nowlangname='en_US'
        self.nowlang=lang[self.nowlangname]
        self.tk=Tk()
        self.styles=Style(self.tk)
        screen_width = self.tk.winfo_screenwidth()
        screen_height = self.tk.winfo_screenheight()
        x = (screen_width/2) - (800/2)
        y = (screen_height/2) - (500/2)
        self.tk.geometry('%dx%d+%d+%d' % (800,500, x, y))
        sv_ttk.use_light_theme()
        self.topbar=Frame(self.tk)
        self.topbar.pack(side='top',fill=X)
        self.tk.minsize(800,500)
        if self.studiomode==False:
            self.tk.title(f'Quizsy {quizsy.ver}')
            fullscreenbutton=Button(self.topbar,text=self.nowlang['fullscreen'],command=quizsy.dofullscreen).pack(side='right')
        self.tk.iconbitmap("icon.ico")
        
        #closebutton=Button(self.topbar,text="Close",command=exit).pack(side='right')
        
        self.bottombar=Frame(self.tk)
        self.bottombar.pack(side='bottom',fill=X)
        self.centerframe=Frame(self.tk)
        self.centerframe.pack(padx=50,pady=20,ipady=100,anchor="center",fill=BOTH)
        
    def uiloop(self):
        if self.studiomode==False:
            self.startup()
        elif self.studiomode==True:
            self.studiostartup()
        self.tk.mainloop()
    def studiostartup(self):
        self.clear()
        self.tk.title("Virtual Quizsy Xperimental Client")
        label=Label(text=f"Virtual Quizsy Xperimental Client is ready.",font=("Segoe UI",12)).pack()
    def startup(self):
        frameCnt = 60
        frames = [PhotoImage(file='loading-pin4.gif',format = 'gif -index %i' %(i)) for i in range(frameCnt)]
        self.centerframe.after(1500, lambda:self.main())
        def update(ind):
            frame = frames[ind]
            ind += 1
            if ind == frameCnt:
                ind = 0
            label.configure(image=frame)
            label.after(10, update, ind)
        label = Label(self.centerframe)
        label.after(0,update,0)
        label.place(relx=0.5,rely=0.5,anchor="center")
    def clear(self):
        self.bottombar.destroy()
        self.centerframe.destroy()
        self.bottombar=Frame(self.tk)
        self.bottombar.pack(side='bottom',fill=X)
        self.centerframe=Frame(self.tk)
        self.centerframe.pack(padx=50,pady=20,ipady=100,anchor="center",fill=BOTH)
    def main(self):
        self.clear()
        funcbar=Frame(self.centerframe)
        funcbar.pack(side="top",anchor="e",ipadx=5)
        mainframe=Frame(self.centerframe)
        mainframe.pack(padx=5,fill=BOTH)
        openbutton = Button(funcbar,text=self.nowlang['openfromafile'],command=self.quiz_open).grid(row=0,column=3,padx=5,pady=5,ipadx=5,sticky="e")
        settingsbutton=Button(funcbar,text=self.nowlang['settings'],command=self.settings).grid(row=0,column=2,padx=5,pady=5,ipadx=5,sticky="e")
        hellolabel = Label(mainframe,text=self.nowlang['welcome'],font=("Segoe UI",30),anchor="w").grid(row=1,column=0,columnspan=4,sticky="w")
        welcomelabel = Label(mainframe,text=f"{nowwelcome}",font=("Segoe UI",20),anchor="w").grid(row=2,column=0,columnspan=4,sticky="w")
        playbutton = Button(mainframe,text=self.nowlang['playaquiz'],command=self.quiz_open).grid(row=3,column=0,columnspan=4,sticky="w",padx=5,pady=5)
        trybutton = Button(mainframe,text=self.nowlang['tryquizsybuiltinquiz'],command=lambda:quizsy.play(quizsy.builtinquiz)).grid(row=4,column=0,columnspan=4,sticky="w",padx=5,pady=5,ipadx=100)
    def settings(self):
        self.clear()
        def darkmode():
            quizsy.metrox=True
            if sv_ttk.get_theme() == 'light':
                sv_ttk.use_dark_theme()
            else:
                sv_ttk.use_light_theme()
        label = Label(self.centerframe,text=self.nowlang['settings'],font=("Segoe UI Bold",24),anchor="w")
        label.pack(side='top',anchor='w')
        button = Button(self.centerframe,text=self.nowlang['back'],command=self.main)
        button.pack(side='bottom')
        frame=Frame(self.centerframe)
        frame.pack(side='top',fill=BOTH)
        darkmodebutton=Button(frame,text=self.nowlang['toggledark'],command=darkmode)
        darkmodebutton.pack(fill=X,anchor='w',ipady=5,pady=5)
        fullscreenbutton=Button(frame,text=self.nowlang['togglefullscreen'],command=quizsy.dofullscreen)
        fullscreenbutton.pack(fill=X,anchor='w',ipady=5,pady=5)
        fullscreenbutton=Button(frame,text=self.nowlang['languagessettings'],command=self.langsettings)
        fullscreenbutton.pack(fill=X,anchor='w',ipady=5,pady=5)
        advancedbutton=Button(frame,text=self.nowlang['advancedsettings'],command=self.advancedsettings)
        advancedbutton.pack(fill=X,anchor='w',ipady=5,pady=5)
        fullscreenbutton.pack(fill=X,anchor='w',ipady=5,pady=5)
        aboutbutton=Button(frame,text=self.nowlang['about'],command=self.about)
        aboutbutton.pack(fill=X,anchor='w',ipady=5,pady=5)
    def langsettings(self):
        def enus():
            self.nowlangname='en_US'
            self.nowlang=self.lang[self.nowlangname]
            self.langsettings()
        def zhtw():
            self.nowlangname='zh_TW'
            self.nowlang=self.lang[self.nowlangname]
            self.langsettings()
        self.clear()
        label = Label(self.centerframe,text=self.nowlang['languagessettings'],font=("Segoe UI Bold",24),anchor="w")
        label.pack(side='top',anchor='w')
        button = Button(self.centerframe,text=self.nowlang['back'],command=self.settings)
        button.pack(side='bottom')
        frame=Frame(self.centerframe)
        frame.pack(side='top',fill=BOTH)
        enusbutton=Button(frame,text='English (United States)',command=enus)
        enusbutton.pack(fill=X,anchor='w',ipady=5,pady=5)
        zhtwbutton=Button(frame,text='Chinese (Traditional)',command=zhtw)
        zhtwbutton.pack(fill=X,anchor='w',ipady=5,pady=5)
    def advancedsettings(self):
        self.clear()
        label = Label(self.centerframe,text=self.nowlang['advancedsettings'],font=("Segoe UI Bold",24),anchor="w")
        label.pack(side='top',anchor='w')
        button = Button(self.centerframe,text=self.nowlang['back'],command=self.settings)
        button.pack(side='bottom')
        frame=Frame(self.centerframe)
        frame.pack(side='top',fill=BOTH)
        metroxbutton=Button(frame,text=self.nowlang['togglewinnative'],command=quizsy.dometrox)
        metroxbutton.pack(fill=X,anchor='w',ipady=5,pady=5)
    def about(self):
        self.clear()
        label = Label(self.centerframe,text=self.nowlang['about'],font=("Segoe UI Bold",24),anchor="w")
        label.pack(side='top',anchor='w')
        label1=Label(self.centerframe,text=f"Quizsy {quizsy.ver}",font=("Segoe UI",12))
        label1.pack(side='top',anchor='w')
        button = Button(self.centerframe,text=self.nowlang['ok'],command=self.settings)
        button.pack(side='bottom')
    def quiz_open(self):
        self.clear()
        dir =tkinter.filedialog.askopenfile(defaultextension=".quizsy_std",filetypes=[("Quizsy Standard Format","*.quizsy_std")])
        if dir == "" or dir == None:
            self.main()
            return 0
        temp_df = pandas.read_json(dir)
        column1 = temp_df[0].to_list()
        column2 = temp_df[1].to_list()
        column3 = temp_df[2].to_list()
        name = column1[0]
        author = column2[0]
        defaultscore = column3[0]
        defaultadd = column1[1]
        deductions = column2[1]
        takeawaypoints = column3[1]
        column1 = column1[2:]
        column2 = column2[2:]
        column3 = column3[2:]
        types = column1.copy()
        questions = column2.copy()
        answers = column3.copy()
        tempclassquestions=Quiz(name,author,questions,answers,types,defaultscore,defaultadd,deductions,takeawaypoints)
        quizsy.play(tempclassquestions)
    def threetwoone(self):
        label=Label(self.centerframe,text='',font=("Segoe UI",50))
        label.place(relx=0.5,rely=0.5,anchor="center")
        def anim():
            for i in range(0,51,3):
                label.config(font=("Segoe UI",i))
                self.tk.update()
                time.sleep(0.01)
        for i in range(5,0,-1):
            label.config(text=f"{i}")
            mixer.music.load("count.mp3")
            mixer.music.play(1)
            label.after(0,anim)
            self.tk.update()
            time.sleep(1)
        label.config(text="GO!")
        mixer.music.load("start.mp3")
        mixer.music.play(1)
        label.after(0,anim)
        self.tk.update()
        self.tk.update()
        time.sleep(1)
    def choose_question(self,nownumber,nowquestion:str,quizname,defaultadd,deductions,takeawaypoints,nowanswer):
        self.clear()
        question=nowquestion.split('A. ')[0]
        a=nowquestion.split('A. ')[1].split('B. ')[0]
        b=nowquestion.split('B. ')[1].split('C. ')[0]
        c=nowquestion.split('C. ')[1].split('D. ')[0]
        d=nowquestion.split('D. ')[1]
        bigframe=Frame(self.centerframe)
        bigframe.pack(fill=BOTH)
        def choose_checkanswer(x,y,z,a):
            buttona["state"] = "disabled"
            buttonb["state"] = "disabled"
            buttonc["state"] = "disabled"
            buttond["state"] = "disabled"

            quizsy.choose_checkanswer(x,y,z,a,nowanswer)
        label=Label(bigframe,text=f"{nownumber}. {question}",font=("Segoe UI",18))
        label.pack(side='top',fill=X)
        frame=Frame(self.bottombar)
        frame.pack(side='bottom',fill=X)
        s = Style()
        s.configure('choosebutton.TButton', font=("Segoe UI",15))
        buttona = Button(frame,text=f"\nA. {a}",command=lambda:choose_checkanswer("A",defaultadd,deductions,takeawaypoints),style='choosebutton.TButton')
        buttonb = Button(frame,text=f"\nB. {b}",command=lambda:choose_checkanswer("B",defaultadd,deductions,takeawaypoints),style='choosebutton.TButton')
        buttonc = Button(frame,text=f"\nC. {c}",command=lambda:choose_checkanswer("C",defaultadd,deductions,takeawaypoints),style='choosebutton.TButton')
        buttond = Button(frame,text=f"\nD. {d}\n",command=lambda:choose_checkanswer("D",defaultadd,deductions,takeawaypoints),style='choosebutton.TButton')
        buttona.grid(row=1,column=0,padx=10,pady=5,ipadx=10,sticky=E+W)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        buttonb.grid(row=1,column=1,padx=10,pady=5,ipadx=10,sticky=E+W)
        buttonc.grid(row=2,column=0,padx=10,pady=5,ipadx=10,sticky=E+W)
        buttond.grid(row=2,column=1,padx=10,pady=5,ipadx=10,sticky=E+W)
        scorelabel=Label(frame,text=f"{self.nowlang['score']}: {quizsy.score}",font=("Segoe UI",12),anchor="e")
        scorelabel.grid(row=3,column=1,sticky=E)
        quizsy.questioning=True
        while quizsy.questioning:
            self.tk.update()
    def fill_question(self,nownumber,nowquestion:str,quizname,defaultadd,deductions,takeawaypoints,nowanswer):
        self.clear()
        question=nowquestion
        def fill_checkanswer(y,z,a):
            buttona["state"] = "disabled"
            quizsy.fill_checkanswer(entry.get(),y,z,a,nowanswer)
        label=Label(self.centerframe,text=f"{nownumber}. {question}",font=("Segoe UI",18))
        label.pack(side='top')
        entry=Entry(self.centerframe,font=("Segoe UI",12))
        entry.place(relx=0.5,rely=0.5,anchor=CENTER)
        buttona = Button(self.centerframe,text=self.nowlang['submit'],command=lambda:fill_checkanswer(defaultadd,deductions,takeawaypoints))
        buttona.pack(side='bottom')
        quizsy.questioning=True
        scorelabel=Label(self.bottombar,text=f"{self.nowlang['score']}: {quizsy.score}",font=("Segoe UI",12),anchor="e")
        scorelabel.pack(side='bottom',anchor='e',fill=X)
        while quizsy.questioning:
            self.tk.update()
    def finalui(self,score,questionsname,length):
        mixer.music.load('final.mp3')
        mixer.music.play(-1)
        self.clear()
        def back():
            mixer.music.stop()
            self.main()
        label = Label(self.centerframe,text=self.nowlang['conclusion'],font=("Segoe UI Bold",24),anchor="w")
        label.pack(side='top',anchor='w')
        label1=Label(self.centerframe,text=f"{self.nowlang['conclusion1']} {questionsname}!\n{self.nowlang['conclusion2']} {length} {self.nowlang['conclusion3']} {score}",font=("Segoe UI",12))
        label1.pack(side='top',anchor='w')
        if self.studiomode==False:
            button = Button(self.centerframe,text=self.nowlang['ok'],command=back)
        if self.studiomode==True:
            button = Button(self.centerframe,text=self.nowlang['ok'],command=self.studiostartup)
        button.pack(side='bottom')

class QuizsyClient:
    def __init__(self,ver:str="Dev",welcome:list=['Test Str'],builtinquiz:Quiz=Quiz("Built in Quiz","Quizsy Official",["1 + 1 = ?\nA. 2\nB. 3\nC. 4\nD. 1","1 + 2 = ?\nA. 2\nB. 4\nC. 0\nD. 3","2 + 2 = ?","3 + 2 = ?"],["A","D","4","5"],["choose","choose","fill","fill"],0,1000,True,100),studiomode=False):
        self.ver=ver
        self.welcome=welcome.copy()
        self.nowwelcome=welcome[random.randint(0,len(welcome)-1)]
        self.builtinquiz=builtinquiz
        self.score=0
        self.questioning=False
        self.fullscreen=False
        self.score=0
        self.metrox=True
        self.studiomode=studiomode
    def dometrox(self):
        if self.metrox==True:
            sv_ttk.use_light_theme()
            quizsy_ui.styles.theme_use('vista')
            self.metrox=False
        else:
            sv_ttk.use_light_theme()
            self.metrox=True
    def play(self,quiz:Quiz):
        if self.studiomode==False:
            quizsy_ui.clear()
        def cancel():
            quizsy_ui.clear()
            frame.destroy()
            quizsy_ui.main()
        def start():
            quizsy_ui.clear()
            frame.destroy()
            quizsy_ui.tk.update()
            self.game(quiz)
        frame=Frame()
        frame.place(relx=0.5,rely=0.5,anchor='center')
        label = Label(frame,text=f"{quizsy_ui.nowlang['play1']} {quiz.name}, {quizsy_ui.nowlang['play2']} {quiz.author}, \n{quizsy_ui.nowlang['play3']} {len(quiz.questions)} {quizsy_ui.nowlang['play4']}",font=("Segoe UI",12))
        label.grid(row=0,column=0,padx=10,pady=5,columnspan=2)
        button = Button(frame,text=quizsy_ui.nowlang['getstarted'],command=start)
        button.grid(row=1,column=0,padx=10,pady=5,ipadx=5)
        button = Button(frame,text=quizsy_ui.nowlang['cancel'],command=cancel)
        button.grid(row=1,column=1,padx=10,pady=5)
    def dofullscreen(self):
            if quizsy.fullscreen ==False:
                quizsy_ui.tk.attributes("-fullscreen", True)
                self.fullscreen=True
            else:
                self.fullscreen=False
                quizsy_ui.tk.attributes("-fullscreen", False)
    def game(self,quiz:Quiz):
        quizsy_ui.threetwoone()
        quizsy_ui.clear()
        mixer.music.load("playing.ogg")
        mixer.music.set_volume(0.5)
        mixer.music.play(-1)
        self.score = quiz.defaultscore
        for i in range(0,len(quiz.questions)):
            nowquestion = quiz.questions[i]
            nowanswer = quiz.answers[i]
            nownumber = i+1
            if quiz.types[i] == "choose":
                quizsy_ui.choose_question(nownumber,nowquestion,quiz.name,quiz.defaultadd,quiz.deductions,quiz.takeawaypoints,nowanswer)
            elif quiz.types[i] == "fill":
                quizsy_ui.fill_question(nownumber,nowquestion,quiz.name,quiz.defaultadd,quiz.deductions,quiz.takeawaypoints,nowanswer)
        quizsy_ui.finalui(self.score,quiz.name,len(quiz.questions))
    def choose_checkanswer(self,letter,defaultadd,deductions,takeawaypoints,nowanswer):
        if letter == nowanswer:
            playsound("correct.mp3")
            self.questioning=False
            self.score += defaultadd
            
            
        else:
            playsound("wrong.mp3")
            self.questioning=False
            if deductions == True:
                self.score -= takeawaypoints
                
            
    def fill_checkanswer(self,letter,defaultadd,deductions,takeawaypoints,nowanswer):
        if letter == nowanswer:
            playsound("correct.mp3")
            self.score += defaultadd
            self.questioning=False
            
            
        else:
            playsound("wrong.mp3")
            self.questioning=False
            if deductions == True:
                self.score -= takeawaypoints
                
            
if __name__=="__main__":
    en_US={'welcome':'Welcome to Quizsy',
           'playaquiz':'Play a Quiz',
           'tryquizsybuiltinquiz':'Try Quizsy using built in Quiz',
           'settings':'Settings',
           'openfromafile':'Open from a File',
           'fullscreen':'Fullscreen',
           'toggledark':'Toggle Dark Mode',
           'togglefullscreen':'Toggle Fullscreen',
           'advancedsettings':'Advanced Settings',
           'about':'About',
           'back':'Back',
           'togglewinnative':'Toggle WinNative Theme(High Performance and Experimental)',
           'cancel':'Cancel',
           'getstarted':"Let's get started!",
           'score':'Score',
           'submit':'Submit',
           'conclusion':'Conclusion',
           'ok':'Ok',
           'languagessettings':'Language Settings',
           'conclusion1':'Congrats! You finished the',
           'conclusion2':'Included',
           'conclusion3':'question(s)\nScore:',
           'play1':'You are going to play',
           'play2':'created by',
           'play3':'contain',
           'play4':'question(s).'
           }
    zh_TW={'welcome':'歡迎來到Quizsy',
           'playaquiz':'玩一個Quiz',
           'tryquizsybuiltinquiz':'使用内建Quiz來體驗Quizsy',
           'settings':'設定',
           'openfromafile':'打開檔案',
           'fullscreen':'全屏幕',
           'toggledark':'調節黑暗模式',
           'togglefullscreen':'調節全螢幕',
           'advancedsettings':'進階設定',
           'about':'關於',
           'back':'返回',
           'togglewinnative':'調節WinNative主題(高性能與實驗性)',
           'cancel':'取消',
           'getstarted':"開始吧！",
           'score':'分數',
           'submit':'提交',
           'conclusion':'總結',
           'ok':'確定',
           'languagessettings':'語言設定',
           'conclusion1':'恭喜! 你完成了',
           'conclusion2':'包含了',
           'conclusion3':'條問題\n分數:',
           'play1':'你將要玩',
           'play2':'作者為',
           'play3':'包含了',
           'play4':'條問題。'
           }
    lang={'en_US':en_US,'zh_TW':zh_TW}
    quizsy=QuizsyClient(ver="Client alpha-0.1",welcome=["Were you happy yesterday?","How are you?","Feel free to play with Quizsy!","Nice to meet you!","Hi!","Hello!","(●'◡'●)","(≧▽≦)"])
    quizsy_ui=QuizsyClientUI(lang=lang)
    quizsy_ui.uiloop()