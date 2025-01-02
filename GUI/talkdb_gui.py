from tkinter import *
from tkinter.ttk import Treeview, Style
from PIL import Image, ImageTk
import subprocess as s
import mysql.connector

def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="prem@2005",
        )
        return conn if conn.is_connected() else None
    except mysql.connector.Error:
        return None

def fetch_data():
    conn = connect_to_database()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute("SHOW DATABASES;")
        databases = [db[0] for db in cursor.fetchall() if db[0] not in (
            "information_schema", "mysql", "performance_schema", "sys")]

        data = {}
        for db in databases:
            cursor.execute(f"USE {db};")
            cursor.execute("SHOW TABLES;")
            tables = [table[0] for table in cursor.fetchall()]

            if tables:
                data[db] = {}
                for table in tables:
                    cursor.execute(f"DESCRIBE {table};")
                    columns = [col[0] for col in cursor.fetchall()]
                    data[db][table] = columns
        return data
    finally:
        conn.close()

def populate_tree(tree, parent, data):
    for db_name, tables in data.items():
        db_id = tree.insert(parent, "end", text=f" {db_name}", open=False)
        for table_name, columns in tables.items():
            table_id = tree.insert(db_id, "end", text=f"{table_name}", open=False)
            for column_name in columns:
                tree.insert(table_id, "end", text=f" {column_name}", open=False)

def generate_query(prompt, data):
    try:
        command = (
            f"ollama run llama3.2 \""
            f"where the data is :{data} and the question is : {prompt}\""
            " Analyze the given database details, including table names, column names, data types, relationships, "
            "and any additional constraints provided. Generate a MySQL query that meets the described requirements, "
            "adhering to standard SQL syntax. Only return the query."
        )
        result = s.run(command, shell=True, capture_output=True, text=True)
        return result.stdout.strip()
    except Exception:
        return "Error generating query."

def submit():
    text = entry_bar.get()
    entry_bar.delete(0,END)
    scrolling_label.update_text(text)
    query = generate_query(text, data)
    Query_label.update_text(query)
    with open(r"GUI-Projects\GUI\query.txt", "w") as f:
        f.write(query)   
tree = None
def toggle_treeview():
    global tree
    if tree and tree.winfo_ismapped():
        tree.destroy()
        tree = None
    else:
        tree = Treeview(window, style="Custom.Treeview")
        tree.place(x=0, y=50, height=300, width=250)
        populate_tree(tree, "", data)

class ScrollingLabel(Frame):
    def __init__(self, parent, text, width=200, height=30, speed=100, **kwargs):
        super().__init__(parent)
        self.text = text
        self.canvas = Canvas(self, width=width, height=height, bg="#3F4D52", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.text_id = self.canvas.create_text(0, height // 2, anchor="w", text=self.text,  **kwargs)
        kwargs.pop('fill', None)
        self.text_width = self.canvas.bbox(self.text_id)[2]
        self.canvas_width = width
        self.speed = speed
        self.x = 0
        if self.text_width > self.canvas_width:
            self.scroll_text()
    def scroll_text(self):
        self.x -= 2
        if abs(self.x) > self.text_width:
            self.x = self.canvas_width
        self.canvas.coords(self.text_id, self.x, self.canvas.winfo_height() // 2)
        self.after(self.speed, self.scroll_text)
    def update_text(self, new_text):
        self.text = new_text
        self.canvas.itemconfig(self.text_id, text=self.text)
        self.text_width = self.canvas.bbox(self.text_id)[2]
        if self.text_width > self.canvas_width:
            self.scroll_text()

class ScrollableLabel2(Frame):
    def __init__(self, parent, width=300, height=50, **kwargs):
        super().__init__(parent)
        self.text_widget = Text(self, wrap="none", height=height, width=width, **kwargs)
        self.text_widget.config(state="disabled")  # Make it read-only
        self.text_widget.grid(row=0, column=0, sticky="nsew")
        self.h_scroll = Scrollbar(self, orient="horizontal", command=self.text_widget.xview)
        self.text_widget.configure(xscrollcommand=self.h_scroll.set)
        self.h_scroll.grid(row=1, column=0, sticky="ew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
    def update_text(self, new_text):
        self.text_widget.config(state="normal") 
        self.text_widget.delete("1.0", "end")  
        self.text_widget.insert("1.0", new_text) 
        self.text_widget.config(state="disabled") 

window = Tk()
window.geometry("600x400")
window.title("TalkDB")
window.config(background="#3F4D52")
window.resizable(False, False)

style = Style()
style.configure("Custom.Treeview", background="#3F4D52", foreground="white", font=("Arial", 10, "bold"), rowheight=30)
style.map("Custom.Treeview", background=[("active", "#4C5B5F"), ("selected", "#2C383C")], foreground=[("selected", "white")])


side_button_image = Image.open(r"GUI-Projects\GUI\static\images\sidebar.png").resize((50, 50))
side_button_main = ImageTk.PhotoImage(side_button_image)
Button(window, command=toggle_treeview, image=side_button_main, 
       bg="#3F4D52", relief="flat", activebackground="#3F4D52").place(x=0, y=0)
logo_image = Image.open(r"GUI-Projects\GUI\static\images\talkdb logo w.png").resize((300, 150))
logo = ImageTk.PhotoImage(logo_image)
Label(window, bg="#3F4D52", image=logo).pack()
entry_bar = Entry(window, font=("Arial", 16), relief="groove", width=40, bg="#3F4D52", fg="white")
entry_bar.insert(0, "")
entry_bar.place(x=10, y=350)
send_button_image = Image.open(r"GUI-Projects\GUI\static\images\send button.png").resize((25, 25))
send_button_resized = ImageTk.PhotoImage(send_button_image)
Button(window, command=submit, image=send_button_resized, 
       bg="#3F4D52", relief="flat", activebackground="#3F4D52").place(x=500, y=350)
delete_button_image = Image.open(r"GUI-Projects\GUI\static\images\Delete-Button.png").resize((25, 25))
delete_button_resized = ImageTk.PhotoImage(delete_button_image)
Button(window, command=lambda: entry_bar.delete(0, END), image=delete_button_resized, 
       bg="#3F4D52", relief="flat", activebackground="#3F4D52").place(x=530, y=350)
data = fetch_data()
scrolling_label = ScrollingLabel(window, text="Your Text Will be displayed here.", width=300,
                                  height=20, speed=40, font=("Arial", 15), fill="black")
scrolling_label.place(x=290, y=280)
Query_label = ScrollableLabel2(window, width=40, height=3, font=("Arial", 16), bg="#3F4D52")
Query_label.update_text("Generated Query will be displayed Here")
Query_label.place(x=20, y=150)
window.mainloop()
