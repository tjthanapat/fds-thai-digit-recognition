from tkinter import *
import tkinter as tk
import win32gui
from PIL import ImageGrab
import numpy as np

from model import predict_digit
from digit_segmentation import segment_digits


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.x = 0
        self.y = 0
        # Creating elements
        self.canvas = tk.Canvas(
            self, width=500, height=300, bg="white", cursor="cross")
        self.label = tk.Label(self, text="Write Number",
                              font=("Tahoma", 32))
        self.classify_btn = tk.Button(
            self, text="Recognise", command=self.classify_handwriting)
        self.button_clear = tk.Button(
            self, text="Clear", command=self.clear_all)
        # Grid structure
        self.canvas.grid(row=0, column=0, columnspan=2, pady=2, sticky=W, )
        self.label.grid(row=1, column=0, columnspan=2, pady=2, padx=2)
        self.classify_btn.grid(row=2, column=1, pady=20)
        self.button_clear.grid(row=2, column=0, pady=20)
        self.canvas.bind("<B1-Motion>", self.draw_lines)

    def clear_all(self):
        self.canvas.delete("all")
        self.label.configure(text="Write Number")

    def classify_handwriting(self):
        self.label.configure(text='Recognising...')
        HWND = self.canvas.winfo_id()  # get the handle of the canvas
        rect = win32gui.GetWindowRect(HWND)  # get the coordinate of the canvas
        img = ImageGrab.grab(rect)
        img = np.array(img)
        digits = segment_digits(img)
        result = ''
        for digit in digits:
            digit = predict_digit(digit)
            result = result + str(digit)
        self.label.configure(text=result)

    def draw_lines(self, event):
        self.x = event.x
        self.y = event.y
        r = 5
        self.canvas.create_oval(
            self.x-r, self.y-r, self.x + r, self.y + r, fill='black')


app = App()
app.title('Handwritten Thai Digit Recognition')
mainloop()
