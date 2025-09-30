import tkinter as tk

root = tk.Tk()
root.title("Tkinter 예제")
root.geometry("200x100") #가로x세로

label = tk.Label(root, text="Hello, Tkinter!")
label.pack(pady=20)

root.mainloop()