import tkinter as tk
import pandas as pd
import random
# --------------------------------Constants----------------------------------------#

FILE_TO_LEARN = 'freq_list.txt'
BACKGROUND_COLOR = "#B1DDC6"
TOP_WORD_FONT = ('Ariel', 30, 'italic')
BOT_WORD_FONT = ('Ariel', 40, 'bold')
CURRENT_CARD = ''
FLIP_SIDE = 1
# --------------------------------Datafile----------------------------------------#

try:
    data_frame = pd.read_csv('words_to_learn.csv')
except FileNotFoundError:
    data_frame = pd.read_csv(FILE_TO_LEARN)
finally:
    flash_card_data = {row.Japanese: row.English for (word, row) in data_frame.iterrows()}
    japanese_words = [key for key in flash_card_data]


def get_random():
    return random.choice(japanese_words)

# --------------------------------Button Functionality----------------------------------------#


def flip():
    global FLIP_SIDE
    FLIP_SIDE *= -1
    if FLIP_SIDE == -1:
        translation = flash_card_data[CURRENT_CARD]
        canvas.itemconfig(canvas_current_image, image=card_back_image)
        canvas.itemconfig(card_title, text='English', fill='white')
        canvas.itemconfig(card_word, text=translation, fill='white')
    else:
        canvas.itemconfig(canvas_current_image, image=card_front_image)
        canvas.itemconfig(card_word, text=CURRENT_CARD, fill='black')
        canvas.itemconfig(card_title, text='Japanese', fill='black')


def next_card():
    global CURRENT_CARD, FLIP_SIDE
    CURRENT_CARD = get_random()
    canvas.itemconfig(canvas_current_image, image=card_front_image)
    canvas.itemconfig(card_word, text=CURRENT_CARD, fill='black')
    canvas.itemconfig(card_title, text='Japanese', fill='black')
    FLIP_SIDE = 1


def correct_press():
    index_to_drop = data_frame[data_frame.Japanese == CURRENT_CARD].index
    data_frame.drop(index_to_drop, inplace=True)
    data_frame.to_csv('words_to_learn.csv', index=False)
    next_card()


# --------------------------------UI----------------------------------------#
# ------MAIN WINDOW------#
win = tk.Tk()
win.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
win.title('Flashy')


# ------CANVAS for CARDS------#
canvas = tk.Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_image = tk.PhotoImage(file='images/card_front.png')
card_back_image = tk.PhotoImage(file='images/card_back.png')
canvas_current_image = canvas.create_image(400, 263, image=card_front_image)
canvas.grid(row=0, column=0, columnspan=3)

# ------Words in CANVAS------#
card_title = canvas.create_text(400, 150, text='', font=TOP_WORD_FONT)
card_word = canvas.create_text(400, 263, text='', font=BOT_WORD_FONT)
next_card()

# ------Buttons------#
right_image = tk.PhotoImage(file='images/right.png')
wrong_image = tk.PhotoImage(file='images/wrong.png')

right_button = tk.Button(image=right_image, highlightthickness=0, command=correct_press)
right_button.grid(row=1, column=2)

wrong_button = tk.Button(image=wrong_image, highlightthickness=0, command=next_card)
wrong_button.grid(row=1, column=0)

flip_button = tk.Button(text='Flip', fg='black', width=12, font=('Ariel', 15, 'bold'), command=flip)
flip_button.grid(row=1, column=1)


win.mainloop()
