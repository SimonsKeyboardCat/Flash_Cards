from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}

# Checking what to load
try:
    data = pandas.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("./data/french_words.csv")
    to_learn = data.to_dict(orient="records")
    print("Loaded new set of words.")
else:
    to_learn = data.to_dict(orient="records")
    print("Loaded words to learn.")


# Functionality
def new_flashcard():
    global current_card, flip_timer

    window.after_cancel(flip_timer)

    current_card = random.choice(to_learn)
    canvas_card_front.itemconfig(image, image=card_front)
    canvas_card_front.itemconfig(upper_text, text="French", fill="black")
    canvas_card_front.itemconfig(lower_text, text=current_card["French"], fill="black")

    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas_card_front.itemconfig(image, image=card_back)
    canvas_card_front.itemconfig(upper_text, text="English", fill="white")
    canvas_card_front.itemconfig(lower_text, text=current_card["English"], fill="white")


def learned():
    to_learn.remove(current_card)
    words_to_learn = pandas.DataFrame(to_learn)
    words_to_learn.to_csv("./data/words_to_learn.csv", index=False)

    new_flashcard()


# UI setup
window = Tk()
window.title("Flash Card")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)
# Flashcard
canvas_card_front = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front = PhotoImage(file="./images/card_front.png")
card_back = PhotoImage(file="./images/card_back.png")
image = canvas_card_front.create_image(400, 263, image=card_front)
upper_text = canvas_card_front.create_text(400, 150, font=("Ariel", 40, "italic"), fill="black", anchor=CENTER, text="")
lower_text = canvas_card_front.create_text(400, 263, font=("Ariel", 60, "bold"), fill="black", anchor=CENTER, text="")
canvas_card_front.grid(column=0, row=0, columnspan=2)

# Buttons
right = PhotoImage(file="./images/right.png")
button_right = Button(image=right, highlightthickness=0, command=learned)
button_right.grid(column=1, row=1)

wrong = PhotoImage(file="./images/wrong.png")
button_wrong = Button(image=wrong, highlightthickness=0, command=new_flashcard)
button_wrong.grid(column=0, row=1)

new_flashcard()

window.mainloop()
