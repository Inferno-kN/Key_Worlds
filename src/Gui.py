import tkinter
import sys
import random
from tkinter import *
from tkinter import messagebox
from src.Game import Game


class GUI:
    def __init__(self, window):
        self.window = window
        self.window.resizable(False, False)
        window.title("Keys of the World")
        window.geometry("800x600")

        self.bg_color = "#1a0000"
        window.configure(bg=self.bg_color)

        self.canvas = Canvas(window, width=800, height=600, bg=self.bg_color, highlightthickness=0)
        self.canvas.place(x=0, y=0)

        self.blood_drops = []
        for _ in range(30):
            x = random.randint(0, 800)
            y = random.randint(-200, 600)
            speed = random.uniform(2, 5)
            size = random.randint(3, 8)
            self.blood_drops.append([x, y, speed, size])

        self.animate_blood()

        self.title_frame = Frame(window, bg=self.bg_color)
        self.title_frame.place(relx=0.5, rely=0.15, anchor=CENTER)

        self.title_label = Label(
            self.title_frame,
            text='KEYS OF THE WORLD',
            font=("Arial Black", 36),
            bg=self.bg_color,
            fg="#ff3333"
        )
        self.title_label.pack()

        self.title_shadow = Label(
            self.title_frame,
            text='KEYS OF THE WORLD',
            font=("Arial Black", 36),
            bg=self.bg_color,
            fg="#660000"
        )
        self.title_shadow.place(x=3, y=3)
        self.title_shadow.lower()

        self.button_frame = Frame(window, bg=self.bg_color)
        self.button_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.button_start = Button(
            self.button_frame,
            text="Новая игра",
            width=20,
            height=2,
            bg="#90EE90",
            fg="black",
            activebackground="#7ccd7c",
            font=("Arial", 12, "bold"),
            command=self.start_game
        )
        self.button_start.pack(pady=10)

        self.button_score = Button(
            self.button_frame,
            text="Об авторе",
            width=20,
            height=2,
            bg="#F0E68C",
            fg="black",
            activebackground="#dbd26b",
            font=("Arial", 12, "bold"),
            command=self.info_author
        )
        self.button_score.pack(pady=10)

        self.button_exit = Button(
            self.button_frame,
            text="Выйти из игры",
            width=20,
            height=2,
            bg="#FA8072",
            fg="black",
            activebackground="#e06b5e",
            font=("Arial", 12, "bold"),
            command=self.exit_game
        )
        self.button_exit.pack(pady=10)

        self.label_author = Label(
            window,
            text="Made by Inferno",
            font=("Arial", 12),
            bg=self.bg_color,
            fg="#993333"
        )
        self.label_author.place(relx=0.5, rely=0.9, anchor=CENTER)

        self.flicker_title()


    def animate_blood(self):
        self.canvas.delete("blood")

        for drop in self.blood_drops:
            drop[1] += drop[2]

            if drop[1] > 620:
                drop[1] = random.randint(-50, 0)
                drop[0] = random.randint(0, 800)

            x, y, _, size = drop
            color = f"#{random.randint(120, 180):02x}0000"
            self.canvas.create_oval(
                x - size // 2, y - size // 2, x + size // 2, y + size // 2,
                fill=color, outline="", tags="blood"
            )

            if random.random() < 0.1:
                self.canvas.create_oval(
                    x - size // 2, y + size, x + size // 2, y + size * 3,
                    fill=color, outline="", tags="blood"
                )

        self.window.after(50, self.animate_blood)


    def flicker_title(self):
        r = random.randint(200, 255)
        self.title_label.config(fg=f"#{r:02x}3333")

        if random.random() < 0.1:
            self.title_label.config(fg="#ffffff")
            self.window.after(50, lambda: self.title_label.config(fg=f"#{r:02x}3333"))

        self.window.after(200, self.flicker_title)


    def start_game(self):
        self.window.withdraw()
        confirm = Toplevel(self.window)
        confirm.title("")
        confirm.geometry("400x200")
        confirm.configure(bg=self.bg_color)
        confirm.resizable(False, False)

        confirm.update_idletasks()
        x = (confirm.winfo_screenwidth() // 2) - (400 // 2)
        y = (confirm.winfo_screenheight() // 2) - (200 // 2)
        confirm.geometry(f'400x200+{x}+{y}')

        msg = Label(
            confirm,
            text="Войти в Ключи Миров?",
            font=("Arial", 14),
            bg=self.bg_color,
            fg="#ff6666"
        )
        msg.pack(pady=30)


        def yes():
            confirm.destroy()
            game = Game()
            game.run()
            self.window.deiconify()


        def no():
            confirm.destroy()
            self.window.deiconify()

        btn_frame = Frame(confirm, bg=self.bg_color)
        btn_frame.pack(pady=20)

        yes_btn = Button(
            btn_frame,
            text="ДА",
            font=("Arial", 12, "bold"),
            bg="#90EE90",
            fg="black",
            command=yes
        )
        yes_btn.pack(side=LEFT, padx=20)

        no_btn = Button(
            btn_frame,
            text="НЕТ",
            font=("Arial", 12),
            bg="#FA8072",
            fg="black",
            command=no
        )
        no_btn.pack(side=LEFT, padx=20)


    def info_author(self):
        author_window = Toplevel(self.window)
        author_window.geometry("500x300")
        author_window.configure(bg=self.bg_color)
        author_window.resizable(False, False)

        author_window.update_idletasks()
        x = (author_window.winfo_screenwidth() // 2) - (500 // 2)
        y = (author_window.winfo_screenheight() // 2) - (300 // 2)
        author_window.geometry(f'500x300+{x}+{y}')

        text_label = Label(
            author_window,
            text="Меня зовут Пашка.\nЯ Junior Backend Developer Python/Go.\nНадеюсь тебе понравится моя игра.\nХорошей игры! :)",
            bg="#F0E68C",
            font=("Arial", 12),
            padx=20,
            pady=20
        )
        text_label.pack(pady=20)

        close_btn = Button(
            author_window,
            text="ЗАКРЫТЬ",
            font=("Arial", 10, "bold"),
            bg="#FA8072",
            fg="black",
            cursor="hand2",
            command=author_window.destroy
        )
        close_btn.pack(pady=10)


    def exit_game(self):
        if messagebox.askyesno(
                "Выход",
                "Точно хочешь уйти?"
        ):
            self.window.quit()
            self.window.destroy()
            sys.exit()


root = Tk()
gui = GUI(root)
root.mainloop()