from tkinter import *
from random import choice
import pandas

BACKGROUND_COLOR = "#B1DDC6"
FONT_NAME = "Ariel"
CURRENT_CARD = []

try:
    cards = pandas.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    cards = pandas.read_csv("./data/french_words.csv")
finally:
    cards_dict = cards.to_dict(orient="records")

# ----------------------- CREATE NEW FLASH CARDS ---------------------- #


def know_card():
    global CURRENT_CARD
    cards_dict.remove(CURRENT_CARD)
    data = pandas.DataFrame(cards_dict)
    data.to_csv('./data/words_to_learn.csv', index=False)
    create_card()


def need_to_learn():
    global CURRENT_CARD
    words_to_learn = {'French': 'chercher', 'English': 'search'}
    create_card()


def create_card():
    global CURRENT_CARD, change_color
    window.after_cancel(change_color)
    canvas.itemconfig(flashcard, image=card_image)
    canvas.itemconfig(language_text, fill="black")
    canvas.itemconfig(card_text, fill="black")
    CURRENT_CARD = choice(cards_dict)
    canvas.itemconfig(language_text, text="French")
    canvas.itemconfig(card_text, text=CURRENT_CARD['French'])
    change_color = window.after(3000, flip_card)


def flip_card():
    global CURRENT_CARD
    canvas.itemconfig(flashcard, image=reverse_card_image)
    canvas.itemconfig(language_text, text="English", fill="white")
    canvas.itemconfig(card_text, text=CURRENT_CARD['English'], fill="white")

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Learn in a Flash")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
change_color = window.after(3000, flip_card)


canvas = Canvas(height=526, width=800, highlightthickness=0, bg=BACKGROUND_COLOR)
card_image = PhotoImage(file="./images/card_front.png")
reverse_card_image = PhotoImage(file="./images/card_back.png")
flashcard = canvas.create_image(400, 263, image=card_image)
language_text = canvas.create_text(400, 150, text="Language", font=(FONT_NAME, 40, "italic"))
card_text = canvas.create_text(400, 263, text="word", font=(FONT_NAME, 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)


wrong_image = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, command=need_to_learn)
wrong_button.grid(column=0, row=1)


right_image = PhotoImage(file="./images/right.png")
right_button = Button(image=right_image, highlightthickness=0, command=know_card)
right_button.grid(column=1, row=1)

create_card()
change_color

window.mainloop()

