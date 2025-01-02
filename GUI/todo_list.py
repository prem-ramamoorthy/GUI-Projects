from tkinter import *
window = Tk()
window.title("TODO_List - By Prem Kumar R")
background_color = "#8ec8e2"
font_color = "#23212d"
button_background = "#729296"
font_details = ("Georgia", 12)
window.iconphoto(True, PhotoImage(file=r"static\images\Todo_list_logo.png"))
window.config(background=background_color)
window.geometry("500x500")
image_logo = PhotoImage(file=r"static\images\to-do-list-logo_1-1-30.png")
Label_image = Label(window, image=image_logo, background=background_color)
Label_image.pack(side="top")
todo_list_creater = Entry(window)
todo_list_creater.config(
    bg="#728096",
    fg=font_color,
    width=29,
    font=("Georgia", 16 , ),
)
todo_list_creater.place(x=10, y=80)
list_todo = []
list_values = []
y = 125  
def striker():
    for i in range(len(list_todo)):
        if list_values[i].get() == 1:
            list_todo[i].config(font=("Georgia", 16 , "overstrike"))
        else: 
            list_todo[i].config(font = ("Georgia", 16 ,))
def add_TODO_list():
    global list_todo, list_values , y
    text = todo_list_creater.get()
    if text.strip():  
        todo_list_creater.delete(0, END)
        value = IntVar()
        checkbox = Checkbutton(
            window,
            text=text,
            variable=value,
            onvalue=1,
            offvalue=0,
            anchor="w",
            font=("Georgia", 16),
            background=background_color,
            activebackground=background_color,
            fg=font_color,
            activeforeground=font_color, padx=20, pady=5,command=striker
        )
        checkbox.place(x = 10 , y = y )
        y+=30
        list_todo.append(checkbox)
        list_values.append(value)
def clear_completed():
    global list_todo, list_values
    for i in range(len(list_todo) - 1, -1, -1):  
        if list_values[i].get() == 1: 
            list_todo[i].destroy()
            del list_todo[i]
            del list_values[i]
submit_button = Button(
    window,
    background=button_background,
    activebackground="#490b63",
    command=add_TODO_list,
    text="Submit",
    font=font_details,
    fg=font_color,
)
submit_button.place(x=400, y=78)
clear_button = Button(
    window,
    background=button_background,
    activebackground="#490b63",
    command=clear_completed,
    text="Clear Completed",
    font=font_details,
    fg=font_color,
)
clear_button.place(x=350, y=450)
window.mainloop()
