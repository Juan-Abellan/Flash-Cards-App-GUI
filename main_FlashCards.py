# TODO | IMPORTS -------------------------------------------------------------------------------------------------------
from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json
import pandas as pd

# TODO | CONSTANTS -----------------------------------------------------------------------------------------------------
BACKGROUND_COLOR = "#B1DDC6"
DATA_PATH = "data/french_words.csv"
random_dict = {}
to_learn = {}

# TODO | LOGIC FLOW & DATA FRAME TO DICT -------------------------------------------------------------------------------
try:
    words_df = pd.read_csv("data/french_words_to_learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv(DATA_PATH)
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = words_df.to_dict(orient="records")


# TODO | ACCESS TO WORDS -----------------------------------------------------------------------------------------------
def pick_random_word():
    """Randomly picks a French word from the list of dictionaries"""
    global random_dict, time_to_flip
    window.after_cancel(time_to_flip)
    random_dict = choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=random_dict["French"], fill="black")
    canvas.itemconfig(card_background, image=flashcard_front)
    time_to_flip = window.after(ms=3000, func=flip_the_card)


# TODO | WORDS KNOWN----------------------------------------------------------------------------------------------------
def known_word():
    """Removes the already learnt word from the list to learn"""
    to_learn.remove(random_dict)
    print(len(to_learn))
    data = pd.DataFrame(to_learn)
    data.to_csv("data/french_words_to_learn.csv", index=False)
    pick_random_word()


# TODO | FLIP THE CARD -------------------------------------------------------------------------------------------------
def flip_the_card():
    """Shows the English version of the French word, modifying the color of the background and the words"""
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=random_dict["English"], fill="white")
    canvas.itemconfig(card_background, image=flashcard_back)


# TODO | UI SETUP-------------------------------------------------------------------------------------------------------
# Window
window = Tk()
window.title("Flash Cards")
window.config(padx=50, pady=50, background=BACKGROUND_COLOR)
time_to_flip = window.after(ms=3000, func=flip_the_card)

# Canvas
flashcard_front = PhotoImage(file="images/card_front.png")
flashcard_back = PhotoImage(file="images/card_back.png")
canvas = Canvas(height=526, width=800)
card_background = canvas.create_image(400, 263, image=flashcard_front)
canvas.grid(row=0, column=0, columnspan=2)
canvas.config(background=BACKGROUND_COLOR, highlightthickness=0)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))

# Buttons
red_cross = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=red_cross, background=BACKGROUND_COLOR, highlightthickness=0, command=pick_random_word)
unknown_button.grid(row=1, column=0)

green_check = PhotoImage(file="images/right.png")
unknown_button = Button(image=green_check, background=BACKGROUND_COLOR, highlightthickness=0, command=known_word)
unknown_button.grid(row=1, column=1)

pick_random_word()

window.mainloop()
