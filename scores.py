import pandas as pd

df = pd.read_csv("leaderboard.csv").sort_values("Wynik", ascending = False)
df = df.to_string(index=False)



from tkinter import *

class Example(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent, background="white")

        self.parent = parent
        self.parent.title('Tabela wyników')
        self.pack(fill=BOTH, expand=1)


def main():
    root = Tk()
    root.geometry("500x900+300+300")
    root.resizable(width=True, height=True)
    label = Label(root, text=df)
    label.config(font=("Courier", 30))
    label.pack()
    root.mainloop()

if __name__ == '__main__':
    main()
