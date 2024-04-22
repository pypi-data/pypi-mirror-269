from tkinter import *
from tkinter import messagebox
import wikipedia

root = Tk()
root.geometry("700x250")
root.resizable(False, False)
root.configure(bg='white')
root.title("Our Search Engine")

var = StringVar()

def run():
    try:
        search_query = var.get()
        summary = wikipedia.summary(search_query)
        messagebox.showinfo(search_query, summary)
    except wikipedia.exceptions.PageError as e:
        messagebox.showerror("Error", "No Wikipedia page found for the given query.")

label = Label(root, text="Our Search Engine", font=("timesnewroman", 35), bg='white')
label.place(x=150, y=10)

entry = Entry(root, font=("timesnewroman", 25), textvariable=var)
entry.place(x=170, y=120)

button = Button(root, text="Search", font=("arial", 15, 'bold'), command=run)
button.place(x=300, y=200)

root.mainloop()