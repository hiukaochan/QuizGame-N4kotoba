import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import json
import random as rd

class QuizGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Game")
        self.style = tb.Style(theme="darkly")
        self.root.geometry('800x400')
        
        self.current_question = 0
        self.score = 0
        self.num_questions = 30  # Default number of questions
        self.words = {}
        
        #READ FILE N4.JSON
        with open("N4.json","r") as filejson:
            self.words = json.load(filejson)
        
        self.create_start_screen()

    def create_start_screen(self):
        self.clear_screen()

        self.current_question = 0
        self.score = 0
        self.num_questions = 30  # Default number of questions 
        self.dict_quest = {}
        
        start_frame = ttk.Frame(self.root, padding="20")
        start_frame.pack(expand=True)
        
        title_label = ttk.Label(start_frame, text="Welcome to the Quiz Game", style="primary.TLabel", font=("Helvetica", 18))
        title_label.pack(pady=20)
        
        start_button = ttk.Button(start_frame, text="Start Quiz", style="success.TButton", command=self.create_question_number_screen)
        start_button.pack(pady=10)

    def create_question_number_screen(self):
        self.clear_screen()
        
        num_frame = ttk.Frame(self.root, padding="20")
        num_frame.pack(expand=True)
        
        title_label = ttk.Label(num_frame, text="Choose question numbers", style="primary.TLabel", font=("Helvetica", 16))
        title_label.pack(pady=20)
        
        control_frame = ttk.Frame(num_frame)
        control_frame.pack(pady=10)
        
        decrease_button = ttk.Button(control_frame, text="-", style="warning.TButton", command=self.decrease_questions)
        decrease_button.grid(row=0, column=0, padx=5)
        
        self.num_label = ttk.Label(control_frame, text=str(self.num_questions), style="secondary.TLabel", font=("Helvetica", 14), background = "white")
        self.num_label.grid(row=0, column=1, padx=5)
        
        increase_button = ttk.Button(control_frame, text="+", style="warning.TButton", command=self.increase_questions)
        increase_button.grid(row=0, column=2, padx=5)
        
        proceed_button = ttk.Button(num_frame, text="Proceed", style="success.TButton", command=self.create_question_screen)
        proceed_button.pack(pady=20)

    def increase_questions(self):
        self.num_questions += 5
        self.num_label.config(text=str(self.num_questions))

    def decrease_questions(self):
        if self.num_questions > 5:
            self.num_questions -= 5
            self.num_label.config(text=str(self.num_questions))

    def create_question(self):
        #self.current_question = self.current_question + 1
        stt_word = rd.randint(1,645)
        type_ques = rd.randint(0,1)
        pos_ans = rd.randint(0,3)

        tmp_list = [0,0,0,0]
        tmp_list[pos_ans] = stt_word
        j = 0
        while j < 4:
            stt_ans = rd.randint(1,645)
            if j == pos_ans: 
                j = j + 1
            else:
                if stt_ans != tmp_list[0] and stt_ans != tmp_list[1] and stt_ans != tmp_list[2] and stt_ans != tmp_list[3]:
                    tmp_list[j] = stt_ans
                    j = j + 1 

        tmp_choice = []

        if type_ques == 0: #quest = nihongo
            for i in tmp_list:
                tmp_choice.append(self.words[str(i)]['Meaning'])
            self.dict_quest = {"question":self.words[str(stt_word)]['Word'],"choices":tmp_choice,"ans":self.words[str(stt_word)]['Meaning']}
        else: #quest = betonamugo
            for i in tmp_list: 
                tmp_choice.append(self.words[str(i)]['Word'])
            self.dict_quest = {"question":self.words[str(stt_word)]['Meaning'],"choices":tmp_choice,"ans":self.words[str(stt_word)]['Word']}


    def create_question_screen(self):
        self.clear_screen()
        
        if self.current_question < self.num_questions:
            self.create_question()
            question_frame = ttk.Frame(self.root, padding="20")
            question_frame.pack(expand=True)
            
            question_label = ttk.Label(question_frame, text=self.dict_quest['question'], style="primary.TLabel", font=("Helvetica", 16), background = "White")
            question_label.pack(pady=20)
            
            for choice in self.dict_quest["choices"]:
                choice_button = ttk.Button(question_frame, text=choice, style="info.TButton", command=lambda c=choice: self.check_answer(c))
                choice_button.pack(fill='x', pady=5)

            self.feedback_label = ttk.Label(question_frame, text="", style="secondary.TLabel", font=("Helvetica", 14))
            self.feedback_label.pack(pady=20)
            
        else:
            self.create_score_screen()

    def check_answer(self, chosen_answer):
        correct_answer = self.dict_quest["ans"]
        if chosen_answer == correct_answer:
            self.score += 1
            self.feedback_label.config(text="Correct!", style="success.TLabel")
        else:
            text_inc = "Incorrect! The correct answer is: " + correct_answer
            self.feedback_label.config(text=text_inc, style="danger.TLabel")
        
        self.current_question = self.current_question + 1
        self.root.after(2000, self.create_question_screen)

    def create_score_screen(self):
        self.clear_screen()
        
        score_frame = ttk.Frame(self.root, padding="20")
        score_frame.pack(expand=True)
        
        score_label = ttk.Label(score_frame, text=f"Your Score: {self.score}/{self.num_questions}", style="primary.TLabel", font=("Helvetica", 18))
        score_label.pack(pady=20)
        
        restart_button = ttk.Button(score_frame, text="Restart Quiz", style="success.TButton", command=self.restart_quiz)
        restart_button.pack(pady=10)

    def restart_quiz(self):
        self.current_question = 0
        self.score = 0
        self.create_start_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    quiz_game = QuizGame(root)
    root.mainloop()
