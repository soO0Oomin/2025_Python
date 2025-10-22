from tkinter import*

def move_oval():
    Canvas.move(id,3,0)
    if Canvas.coords(id)[2] < 400:
        root.after(50,move_oval)

root = Tk()

Canvas=Canvas(root,width=400,height=300)
Canvas.pack()

id=Canvas.create_oval(10,100,50,150,fill="green")
move_oval()

root.mainloop()