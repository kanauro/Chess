from tkinter import *

def init_hru_1():
    print(color.get())
    with open('setting.txt', 'w') as t:
        t.write('New Game\n')
        t.write('Player vs Computer\n')
        if color.get() == 1:
            t.write('Color: White\n')
        else:
            t.write('Color: Black\n')

set_okno = Tk()
color = IntVar(value=1)
setting = Label(set_okno, text = 'Choose color', font='Consolas 20 bold')
black = Radiobutton(set_okno, text="Black", font='Consolas 10', variable=color, value = 2)
white = Radiobutton(set_okno, text="White", font='Consolas 10', variable=color, value = 1)
b_save = Button(set_okno, text="Save", command=init_hru_1)
setting.pack()
black.pack()
white.pack()
b_save.pack()
set_okno.mainloop()
