from tkinter import *
from tkinter import ttk, messagebox
window = Tk()
window.geometry("1550x700")
window.title("Harbor Ship Management")
icon_image = PhotoImage(file=r"static\images\png-transparent-harbor-ship-line-art.png")
window.iconphoto(True, icon_image)
window.config(background="#80b7b0")
def distribute_containers_among_ships(ships, containers):
    sorted_containers = sorted(containers, key=lambda x: (x['distance'], x['delivery_date']))
    num_ships = len(ships)
    ship_assignments = {ship: [] for ship in ships}  
    ship_distances = {ship: 0 for ship in ships}  
    for container in sorted_containers:
        min_distance_ship = min(ship_distances, key=ship_distances.get)
        ship_assignments[min_distance_ship].append(container)
        ship_distances[min_distance_ship] += int(container['distance'])
    return ship_assignments
def job_sequencing(ships):
    ships.sort(key=lambda x: (-x[2], x[1]))
    max_deadline = max(ship[1] for ship in ships)
    schedule = [-1] * (max_deadline + 1)
    result = []
    for ship in ships:
        ship_name, containers, priority = ship
        for t in range(min(max_deadline, containers), 0, -1):
            if schedule[t] == -1:
                schedule[t] = ship_name
                result.append(ship)
                break
    return result
def store_containers_in_harbor(max_size, ships):
    sorted_ships = {}
    for ship_name, containers in ships.items():
        sorted_containers = sorted(containers, key=lambda x: (x['distance'], x['delivery_date']))
        sorted_ships[ship_name] = sorted_containers
    slots = [[] for _ in range(max_size)]
    slot_index = 0
    for ship_name, containers in sorted_ships.items():
        for container in containers:
            if slot_index < max_size and len(slots[slot_index]) < max_size:
                slots[slot_index].append({'ship_name': ship_name, **container})
            else:
                slot_index += 1
                if slot_index < max_size:
                    slots[slot_index].append({'ship_name': ship_name, **container})
                else:
                    print("No more slots available in the harbor!")
                    return slots
    display_harbor_status(slots)
    return slots
def display_harbor_status(slots):
    status_text = "Harbor Availability:\n"
    for i, slot in enumerate(slots):
        status_text += f"Slot {i + 1}: "
        if len(slot) == 0:
            status_text += "No containers"
        else:
            container_names = [container['name'] for container in slot]
            status_text += ", ".join(container_names)
        status_text += "\n"
    harbor_status_label.config(text=status_text)
ships_near_harbor = []
ships = {}
containers = []
list_of_container_details = []
stored_containers = []
no_of_slots = 0
def submit1():
    global no_of_slots
    no_of_slots = int(no_of_ships.get())
    messagebox.showinfo("Success", "Number of ships registered successfully!")
    no_of_ships.delete(0, END)
    update_harbor_availability()
def update_ship_scroll_region():
    ship_canvas.update_idletasks()
    ship_canvas.config(scrollregion=ship_canvas.bbox("all"))
def update_ship_details():
    global ships_near_harbor
    for widget in ship_details_inner_frame.winfo_children():
        widget.destroy()
    headers = ["Ship Name", "No of Containers", "Priority"]
    for col, header in enumerate(headers):
        label = Label(ship_details_inner_frame, text=header, font=("Arial", 10, "bold"), relief="solid", width=18, bg="#b0e0d0")
        label.grid(row=0, column=col, sticky="nsew")
    for row, ship in enumerate(ships_near_harbor, start=1):
        Label(ship_details_inner_frame, text=ship[0], relief="solid", width=18, bg="#e0f7f0").grid(row=row, column=0, sticky="nsew")
        Label(ship_details_inner_frame, text=ship[1], relief="solid", width=18, bg="#e0f7f0").grid(row=row, column=1, sticky="nsew")
        Label(ship_details_inner_frame, text=ship[2], relief="solid", width=18, bg="#e0f7f0").grid(row=row, column=2, sticky="nsew")
    update_ship_scroll_region()
def submit2():
    global ships_near_harbor
    ship_name1 = ship_name.get()
    no_of_containers1 = int(no_of_containers.get())
    priority1 = int(priority.get())
    ships_near_harbor.append([ship_name1, no_of_containers1, priority1])
    messagebox.showinfo("Success", f"Ship {ship_name1} added successfully!")
    update_ship_details()
    ship_name.delete(0, END)
    no_of_containers.delete(0, END)
    priority.delete(0, END)
def completed():
    global sequenced_data, ships_near_harbor
    sequenced_data = job_sequencing(ships_near_harbor)
    messagebox.showinfo("Success", "Successfully sequenced the ships!")
    t = 'The Sequenced Ships to Unload is:\n'
    for i in sequenced_data:
        t += str(i[0]) + ', '
    label6.config(text=t)
def create_dynamic_entries(n):
    entry_fields = []
    for i in range(n):
        x_pos = 780
        y_pos = 50 + (i * 30)
        entry = Entry(window, width=30)
        entry.place(x=x_pos, y=y_pos)
        entry_fields.append(entry)
    return entry_fields
def submit3():
    global list_of_container_entries, list_of_container_details, containers
    d = {
        "name": list_of_container_entries[1].get(),
        "destination": list_of_container_entries[2].get(),
        "distance": list_of_container_entries[3].get(),
        "delivery_date": list_of_container_entries[4].get()
    }
    shipname = list_of_container_entries[0].get()
    containers.append(d)
    list_of_container_details.append([shipname, d])
    update_container_details_table() 
    list_of_container_entries[1].delete(0, END)
    list_of_container_entries[2].delete(0, END)
    list_of_container_entries[3].delete(0, END)
    list_of_container_entries[4].delete(0, END)
    messagebox.showinfo("Success", f"Successfully!! Added container details of ship: {shipname}")
def completed1():
    global ships,no_of_slots
    for i in list_of_container_details:
        if i[0] in ships:
            ships[i[0]].append(i[1])
        else:
            ships[i[0]] = [i[1]]
    update_container_details_table() 
    store_containers_in_harbor(no_of_slots, ships)
    messagebox.showinfo("Success", "All container details have been completed and added!")
canvas = Canvas(window, width=10000, height=10000, background="#80b7b0")
canvas.pack()
canvas.create_line(500, -12, 500, 1000, width=2)
canvas.create_line(1120, -12, 1120, 1000, width=2)
label1 = Label(window, text="Enter the No Slots Available in Harbor :", background="#80b7b0")
label2 = Label(window, text="  *  ---  Ship Arrival Management  ---  * ", background="#80b7b0", font=("Arial", 16, "bold"))
label2.place(x=5, y=10)
label1.place(x=90, y=50)
no_of_ships = Entry(window, width=10)
no_of_ships.place(x=310, y=51)
submit_button1 = Button(window, text="<-Submit", background="#80b7b0", command=submit1)
submit_button1.place(x=380, y=48)
label3 = Label(window, text="Enter the Name of the Ship:", background="#80b7b0")
label4 = Label(window, text="Enter the No of containers:", background="#80b7b0")
label5 = Label(window, text="Enter the priority in minutes:", background="#80b7b0")
label3.place(x=30, y=150)
label4.place(x=30, y=180)
label5.place(x=30, y=210)
ship_name = Entry(window, width=30)
no_of_containers = Entry(window, width=30)
priority = Entry(window, width=30)
ship_name.place(x=210, y=150)
no_of_containers.place(x=210, y=180)
priority.place(x=210, y=210)
ship_details_frame = Frame(window, background="#80b7b0")
ship_details_frame.place(x=50, y=300)
header_labels = ["Ship Name", "No of Containers", "Priority"]
ship_details = Button(window, text="Submit", background="#80b7b0", command=submit2)
ship_details.place(x=180, y=250)
completed = Button(window, text="Completed!", background="#80b7b0", command=completed)
completed.place(x=260, y=250)
label6 = Label(window, text='The Sequenced Ships to Unload is:\n', background="#80b7b0", font=("Arial", 13, "bold"))
label6.place(x=20, y=590)
label7 = Label(window, text="  *  ---  Container Management  ---  * ", background="#80b7b0", font=("Arial", 16, "bold"))
label7.place(x=610, y=10)
label9 = Label(window , text = "Enter the Ship Name           :" , background="#80b7b0") 
label9.place(x=610 , y = 50 )
label8 = Label(window , text = "Enter the Container Name :" , background="#80b7b0") 
label8.place(x=610 , y = 80 )
label10 = Label(window , text = "Enter the Destination          :" , background="#80b7b0") 
label10.place(x=610 , y = 110 ) 
label11 = Label(window , text = "Enter the Distance               :" , background="#80b7b0") 
label11.place(x=610 , y = 140 )
label12 = Label(window , text = "Enter the Date of Delivery  :" , background="#80b7b0") 
label12.place(x=610 , y = 170 )
label13 =  Label(window , text = "* Click submit if you completed filling details of a container or \n "+
                 "Click completed button if you completed filling a containers details of a ship .*" , background="#80b7b0",font=("Arial", 9, "bold")) 
label13.place(x=605 , y = 200 )
label14 = Label(window, text="  *  ---  Harbor Visualization ---  * ", background="#80b7b0", font=("Arial", 16, "bold"))
label14.place(x=1125, y=10)
list_of_container_entries = create_dynamic_entries(5)
submit3_button = Button(window, text="Submit", background="#80b7b0", command=submit3)
submit3_button.place(x=780, y=250)
completed1_button = Button(window, text="Completed", background="#80b7b0", command=completed1)
completed1_button.place(x=840, y=250)
scrollable_container_frame = Frame(window, background="#80b7b0", relief="solid", borderwidth=1)
scrollable_container_frame.place(x=620, y=300, width=470, height=300)
container_canvas = Canvas(scrollable_container_frame, background="#80b7b0", relief="flat")
scrollbar_y = Scrollbar(scrollable_container_frame, orient=VERTICAL, command=container_canvas.yview)
scrollbar_x = Scrollbar(scrollable_container_frame, orient=HORIZONTAL, command=container_canvas.xview)
container_canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
container_canvas.grid(row=0, column=0, sticky="nsew")
scrollbar_y.grid(row=0, column=1, sticky="ns")
scrollbar_x.grid(row=1, column=0, sticky="ew")
container_details_frame = Frame(container_canvas, background="#80b7b0", relief="solid")
container_canvas.create_window((0, 0), window=container_details_frame, anchor="nw")
def update_scroll_region():
    container_canvas.update_idletasks()
    container_canvas.config(scrollregion=container_canvas.bbox("all"))
def update_container_details_table():
    global list_of_container_details
    for widget in container_details_frame.winfo_children():
        widget.destroy()
    headers = ["Ship Name", "Container Name", "Destination", "Distance", "Delivery Date"]
    for col, header in enumerate(headers):
        label = Label(container_details_frame, text=header, font=("Arial", 10, "bold"), relief="solid", width=18, bg="#b0e0d0")
        label.grid(row=0, column=col, sticky="nsew")
    for row, (ship, container) in enumerate(list_of_container_details, start=1):
        Label(container_details_frame, text=ship, relief="solid", width=18, bg="#e0f7f0").grid(row=row, column=0, sticky="nsew")
        Label(container_details_frame, text=container["name"], relief="solid", width=18, bg="#e0f7f0").grid(row=row, column=1, sticky="nsew")
        Label(container_details_frame, text=container["destination"], relief="solid", width=18, bg="#e0f7f0").grid(row=row, column=2, sticky="nsew")
        Label(container_details_frame, text=container["distance"], relief="solid", width=18, bg="#e0f7f0").grid(row=row, column=3, sticky="nsew")
        Label(container_details_frame, text=container["delivery_date"], relief="solid", width=18, bg="#e0f7f0").grid(row=row, column=4, sticky="nsew")
    update_scroll_region()
scrollable_ship_frame = Frame(window, background="#80b7b0", relief="solid", borderwidth=1)
scrollable_ship_frame.place(x=50, y=300, width=405, height=290)
ship_canvas = Canvas(scrollable_ship_frame, background="#80b7b0", relief="flat")
scrollbar_y_ship = Scrollbar(scrollable_ship_frame, orient=VERTICAL, command=ship_canvas.yview)
scrollbar_x_ship = Scrollbar(scrollable_ship_frame, orient=HORIZONTAL, command=ship_canvas.xview)
ship_canvas.configure(yscrollcommand=scrollbar_y_ship.set, xscrollcommand=scrollbar_x_ship.set)
ship_canvas.grid(row=0, column=0, sticky="nsew")
scrollbar_y_ship.grid(row=0, column=1, sticky="ns")
scrollbar_x_ship.grid(row=1, column=0, sticky="ew")
ship_details_inner_frame = Frame(ship_canvas, background="#80b7b0", relief="solid")
ship_canvas.create_window((0, 0), window=ship_details_inner_frame, anchor="nw")
scrollable_container_frame.rowconfigure(0, weight=1)
scrollable_container_frame.columnconfigure(0, weight=1)
harbor_canvas = Canvas(window, background="#80b7b0", width=300, height=300)
harbor_canvas.place(x=1150, y=50)
def update_harbor_availability():
    max_rows = no_of_slots 
    max_columns = no_of_slots 
    harbor_canvas.delete("all")
    total_slots = max_rows * max_columns
    filled_slots = len(stored_containers)
    block_width = 25
    block_height = 25
    margin = 5
    for i in range(total_slots):
        row = i // max_columns 
        col = i % max_columns        
        if i < filled_slots:
            color = "#006400" 
        else:
            color = "#8FBC8F"
        harbor_canvas.create_rectangle(
            col * (block_width + margin), 
            row * (block_height + margin), 
            col * (block_width + margin) + block_width, 
            row * (block_height + margin) + block_height,
            fill=color, outline="black"
        )
def store_container_in_harbor():
    submit3()
    global stored_containers
    container_details = {
        "name": list_of_container_entries[1].get(),
        "destination": list_of_container_entries[2].get(),
        "distance": list_of_container_entries[3].get(),
        "delivery_date": list_of_container_entries[4].get()
    }
    shipname = list_of_container_entries[0].get()
    stored_containers.append(container_details) 
    update_harbor_availability() 
    list_of_container_entries[1].delete(0, END)
    list_of_container_entries[2].delete(0, END)
    list_of_container_entries[3].delete(0, END)
    list_of_container_entries[4].delete(0, END)
def submit3():
    global list_of_container_entries, list_of_container_details, containers
    d = {
        "name": list_of_container_entries[1].get(),
        "destination": list_of_container_entries[2].get(),
        "distance": list_of_container_entries[3].get(),
        "delivery_date": list_of_container_entries[4].get()
    }
    shipname = list_of_container_entries[0].get()
    containers.append(d)
    list_of_container_details.append([shipname, d])
    update_container_details_table() 
    list_of_container_entries[1].delete(0, END)
    list_of_container_entries[2].delete(0, END)
    list_of_container_entries[3].delete(0, END)
    list_of_container_entries[4].delete(0, END)
    messagebox.showinfo("Success", f"Successfully!! Added container details of ship: {shipname}")
submit3_button = Button(window, text="Submit", background="#80b7b0", command=store_container_in_harbor)
submit3_button.place(x=780, y=250)
harbor_status_label = Label(window, text="Harbor Availability:", background="#80b7b0", font=("Arial", 13, "bold"))
harbor_status_label.place(x=600, y=600)
labe99 = Label(window, text="  * --- Container distribution among the ships --- * ", background="#80b7b0", font=("Arial", 12, "bold"))
labe99.place(x=1123, y= 365)
ships_to_distribute = []    
labe98 = Label(window, text="Enter the ship Name : ", background="#80b7b0" )
labe98.place(x=1123, y= 410)
entry_ships = Entry(window, width=30)
entry_ships.place(x=1255, y= 410)
label97 =  Label(window , text = "* Click submit if you want to add ship details or \n Click completed button if you completed filling all details of a ships.*" , 
                 background="#80b7b0",font=("Arial", 9, "bold")) 
label97.place(x=1123, y= 430 )
def completed5():
    global ships_to_distribute, containers
    t = ''    
    for i in ships_to_distribute:
        t += i + " , "
    label95.config(text=t)    
    d = distribute_containers_among_ships(ships_to_distribute, containers)
    last_label = []
    for ship, assigned_containers in d.items():
        existing_ship = next((item for item in last_label if item[0] == ship), None)
        if existing_ship:
            existing_ship[1].extend([container["id"] for container in assigned_containers])
        else:
            last_label.append([ship, [container["name"] for container in assigned_containers]])
    t = ""
    for k in last_label:
        t += k[0] + " : " + ", ".join(map(str, k[1])) + " ; "
    label93.config(text=t)
def submit5():
    global ships_to_distribute
    v=entry_ships.get()
    ships_to_distribute.append(v)
    entry_ships.delete(0,END)
    messagebox.showinfo("Success", f"Successfully!! Added Name of the ship: {v}")
submit5 = Button(window, text="Submit!", background="#80b7b0", command=submit5)
submit5.place(x=1190, y= 480)
completed5 = Button(window, text="Completed!", background="#80b7b0", command=completed5)
completed5.place(x=1250, y= 480)
label96 = Label(window , text = "The Names of the Ships : \n", background="#80b7b0",font=("Arial", 12, "bold"))
label96.place(x=1130, y= 520)
label95 = Label(window , text = "", background="#80b7b0")
label95.place(x=1130, y= 550)
label94 = Label(window , text = "distributed containers among ships : ", background="#80b7b0",font=("Arial", 12, "bold"))
label94.place(x=1130, y= 600)
label93 = Label(window , text = "", background="#80b7b0")
label93.place(x=1130, y= 630)
update_harbor_availability()
window.mainloop()
