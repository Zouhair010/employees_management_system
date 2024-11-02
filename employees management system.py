import tkinter as tk
import csv
import os

window = tk.Tk()
# window.geometry('600x400')
window.title("employees management")

#hash map
class HashMap:
    def __init__(self,size):
        self.buckets = [[] for _ in range(size*20)]
        self.size = size
    def hash_function(self,key):
        return sum(int(char) for char in key if char.isdigit())%(self.size*20)
    def add(self,info):
        key = info[0]
        index = self.hash_function(key)
        bucket = self.buckets[index]
        for i, name_key_rank in enumerate(bucket):
            if name_key_rank[0] == key:
                bucket[i] = info
                return
        bucket.append(info)
    def contains(self,key):
        index = self.hash_function(key)
        bucket = self.buckets[index]
        for info in bucket:
            if info[0] == key:
                return True    
    def get(self,key):
        index = self.hash_function(key)
        bucket = self.buckets[index]
        for info in bucket:
            if info[0] == key:
                return info

def load_employees():
    try:
        if not os.path.exists('C:\\Users\\dell\\Desktop\\newdata.csv'): #check if the file is not exist
            fieldnames = ['number','fname','lname','rank'] #headers names
            with open('C:\\Users\\dell\\Desktop\\newdata.csv', 'w+', newline='') as csvfile: #creat a csv file and open it in the write mode
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames) # writer for write 
                writer.writeheader() # add the headers to the file
    
        with open('C:\\Users\\dell\\Desktop\\newdata.csv','r') as csvfile: #open the csv file in the read mod
            reader = csv.DictReader(csvfile) #convert the data on the csv file to dictionaries with keys names of columns and values is the data in rows
            data = [(row['number'],row['fname'],row['lname'],row['rank']) for row in reader] #list of dicts 
        return data 
    except Exception as E:
        print('the process not done', E) #to show the type of the exception
        return None

def push_hashmap():
    data = load_employees()
    length = len(data) 
    if length == 0:
        length = 10
    hash_map = HashMap(length) #length of data as size of the hash map
    for row in data:
        hash_map.add(row) #add  data to the hash map
    return hash_map #return the hash map instance

#search function for search for an employee by using hash map quick search 
def search_employee():
    hash_map = push_hashmap() #the hash map 
    key = search_entry.get() #get the entry of the user
    info_employee = hash_map.get(key)
    if key == '' or key == ' ' or key == '  ' or not any(char.isdigit() for char in key): #if the user enter nothing or space or double space tells him he should enter a key
        show_label['fg'] = 'red'
        show_label.config(text=f"you should enter id number")
        return
    if hash_map.contains(key): #quick check if an employee exist on file
        show_label['fg'] = 'green'
        show_label.config(text=f"{info_employee[1]} {info_employee[2]} exist")
    elif not hash_map.contains(key): #quick check if an employee does not exist on file
        show_label['fg'] = 'red'
        show_label.config(text=f"the employee with the number {key} does not exist")

def add_employee():
    hash_map = push_hashmap()
    employee_info = add_entry.get() #get the entry of the user
    list_employee_info = employee_info.split() # separate the string to list of info ['number', 'first_name', 'last_name', 'rank']
    if list_employee_info == '' or list_employee_info == ' ' or list_employee_info == '  ' or len(list_employee_info)<4: #if the user enter nothing or space or double space tells him he should enter a key
        show_label['fg'] = 'red'
        show_label.config(text=f"you should enter the right info")
        return
    key= list_employee_info[0]
    if not hash_map.contains(key): #quick check if an employee not to add it exist on file 
                # append an employee to the file
        fieldnames = ['number','fname','lname','rank']
        with open('C:\\Users\\dell\\Desktop\\newdata.csv','a',newline='') as csvfile:
            writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
            # writer.writeheader()
            writer.writerow({'number':f'{list_employee_info[0]}','fname':f'{list_employee_info[1]}','lname':f'{list_employee_info[2]}','rank':f'{list_employee_info[3]}'})
        hash_map.add(employee_info)
        show_label['fg'] = 'green'
        show_label.config(text=f"{list_employee_info[1]} {list_employee_info[2]} has been added")

    else: #if the employeer is already on the file
        show_label['fg'] = 'red'
        show_label.config(text=f"{list_employee_info[1]} {list_employee_info[2]} is already added")

# remove function 
def remove_employee():
    hash_map = push_hashmap()
    key = remove_entry.get()
    info_employee = hash_map.get(key) #get the info employees from hash map by their number
    if key == '' or key == ' ' or key == '  ' or not any(char.isdigit() for char in key): #if the user enter nothing or space or double space tells him he should enter a key
        show_label['fg'] = 'red'
        show_label.config(text=f"you should enter the id number")
        return
    elif hash_map.contains(key): #quick check if an employee exist on file to remove it
        show_label['fg'] = 'green'
        show_label.config(text=f"{info_employee[1]} {info_employee[2]} has been deleted")
        # hash_map.remove(key)
        # apdate the employee file
        with open('C:\\Users\\dell\\Desktop\\newdata.csv','r') as csvfile: #open the csv file in the read mode
            reader = csv.DictReader(csvfile) #convert the data on the csv file to dictionaries with keys names of columns and values is the data in rows
            data = list(reader) #list of dicts
        data = [row for row in data if not (row['number']==info_employee[0] and row['fname']==info_employee[1] and row['lname']==info_employee[2] and row['rank']==info_employee[3])] #remove the info of employees the data 
        fieldnames = ['number','fname','lname','rank'] 
        with open('C:\\Users\\dell\\Desktop\\newdata.csv', 'w', newline='') as csvfile: #open the csv file in the write mode
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames) 
            writer.writeheader() # add the headers to the file
            writer.writerows(data) # write the updated data
    elif any(char.isdigit() for char in key): # tell user if the employee does not exist
        show_label['fg'] = 'red'
        show_label.config(text=f"the employee with the number {key} does not exist")

def show_list_employees():
    if not os.path.exists("C:\\Users\\dell\\Desktop\\newdata.csv") :#check if the file is not exist
        fieldnames = ['number','fname','lname','rank']
        with open('C:\\Users\\dell\\Desktop\\newdata.csv','w+') as csvfile: #creat a csv file and open it in the write mode
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader() # add the headers to the file
    choice = list_box.get(list_box.curselection()) #get the choice from the list box 
    if choice == 'junior': #if the choice is junior
        with open('C:\\Users\\dell\\Desktop\\newdata.csv','r') as csvfile:
            reader = csv.DictReader(csvfile)
            data = list(reader)
            data_juniors = [row for row in data if row['rank'] == 'junior'] # the employees that are juniors 
            data_juniors= '\n'.join(f"{data['fname']} {data['lname']} {data['number']}" for data in data_juniors)
            canvas = tk.Canvas(frame1, width=300, height=200, bg='#c4fbcf',highlightbackground='#47b75f',highlightthickness=1)
            canvas.grid(row=1, column=0,sticky='nsew')
            scrollbar = tk.Scrollbar(frame1, orient=tk.VERTICAL, command=canvas.yview, bg='#b1f1a7')
            scrollbar.grid(row=1, column=1, sticky='ns')
            canvas.configure(yscrollcommand=scrollbar.set)
            label = tk.Label(canvas, text=f"{data_juniors}", wraplength=200 , bg='#c4fbcf') #show the juniors employees in the label
            canvas.create_window(150, 100, window=label)
            canvas.update_idletasks()  
            canvas.config(scrollregion=canvas.bbox("all")) 
            def on_scroll(event):
                    canvas.yview_scroll(int(-1*(event.delta/120)), "units")
                    frame1.bind("<MouseWheel>", on_scroll)
    elif choice == 'sinior':#if the choice is sinior
        with open('C:\\Users\\dell\\Desktop\\newdata.csv','r') as csvfile:
            reader = csv.DictReader(csvfile)
            data = list(reader)
            data_siniors = [row for row in data if row['rank'] == 'sinior']
            r= '\n'.join(f"{data['fname']} {data['lname']} {data['number']}" for data in data_siniors)# the employees that are siniors 
            canvas = tk.Canvas(frame1, width=300, height=200, bg='#c4fbcf',highlightbackground='#47b75f',highlightthickness=1)
            canvas.grid(row=1, column=0,sticky='nsew')
            scrollbar = tk.Scrollbar(frame1, orient=tk.VERTICAL, command=canvas.yview, bg='#b1f1a7') #scroll vertically the convas
            scrollbar.grid(row=1, column=1, sticky='ns')
            canvas.configure(yscrollcommand=scrollbar.set)
            label = tk.Label(canvas, text=f"{r}",wraplength=200 , bg='#c4fbcf')#show the siniors employees in the label
            canvas.create_window(150, 100, window=label) # add the label into the convas in the coordination 150(from the left),100(from the top)
            canvas.update_idletasks()  # update the convas size
            canvas.config(scrollregion=canvas.bbox("all")) 
            def on_scroll(event):
                    canvas.yview_scroll(int(-1*(event.delta/120)), "units")
                    frame1.bind("<MouseWheel>", on_scroll)
    elif choice == 'all':#if the choice is sall
        with open('C:\\Users\\dell\\Desktop\\newdata.csv','r') as csvfile:
            reader = csv.DictReader(csvfile)
            data = list(reader)
            r= '\n'.join(f"{data['fname']} {data['lname']} {data['number']}" for data in data)# the employees that are siniors 
            canvas = tk.Canvas(frame1, width=300, height=200, bg='#c4fbcf',highlightbackground='#47b75f',highlightthickness=1)
            canvas.grid(row=1, column=0,sticky='nsew')
            scrollbar = tk.Scrollbar(frame1, orient=tk.VERTICAL, command=canvas.yview, bg='#b1f1a7') #scroll vertically the convas
            scrollbar.grid(row=1, column=1, sticky='ns')
            canvas.configure(yscrollcommand=scrollbar.set)
            label = tk.Label(canvas, text=f"{r}",wraplength=200 , bg='#c4fbcf')#show the employees in the label
            canvas.create_window(150, 100, window=label) # add the label into the convas in the coordination 150(from the left),100(from the top)
            canvas.update_idletasks()  # update the convas size
            canvas.config(scrollregion=canvas.bbox("all")) 
            def on_scroll(event):
                    canvas.yview_scroll(int(-1*(event.delta/120)), "units")
                    frame1.bind("<MouseWheel>", on_scroll)

frame = tk.Frame(window,background='#b1f1a7')
frame.grid()

frame1 = tk.Frame(frame, background='#b1f1a7',border=1,relief='groove',highlightbackground='#b1f1a7')
frame1.grid(row=0,column=1,padx=(7,0),sticky='nsew')

show_label = tk.Label(frame1, text="", background='#b1f1a7',width=50)
show_label.grid(row=0,column=0,sticky='nsew')

label_frame1 = tk.LabelFrame(frame, text='Add Delete Search info',background='#b1f1a7',highlightbackground='#b1f1a7',highlightthickness=1)
label_frame1.grid(row=0,column=0,sticky='nsew')

add_label = tk.Label(label_frame1, text="add an employee's number first-name last-name rank",width=50, background='#b1f1a7')
add_label.grid(row=1,column=0,sticky='nsew')
add_entry = tk.Entry(label_frame1,width='25',border=1,relief="solid",background='#e1fae6')
add_entry.insert(0,'add an employee')
add_entry.bind("<FocusIn>",lambda e:add_entry.delete('0','end'))
add_entry.grid(row=2,column=0,pady=(0,10),sticky='nsew')
add_button = tk.Button(label_frame1, background='#47b75f',text="add",command=add_employee)
add_button.grid(row=2,column=1,pady=(0,10),sticky='nsew')

remove_label = tk.Label(label_frame1, text="remove an employee by input his number down",width=50, background='#b1f1a7')
remove_label.grid(row=3,column=0,sticky='nsew')
remove_entry =tk.Entry(label_frame1,width='25',border=1,relief="solid",background='#e1fae6')
remove_entry.insert(0,'remove an employee')
remove_entry.bind("<FocusIn>",lambda e:remove_entry.delete('0','end'))
remove_entry.grid(row=4,column=0,pady=(0,10),sticky='nsew')
remove_button = tk.Button(label_frame1,background='#47b75f', text="remove",command=remove_employee)
remove_button.grid(row=4,column=1,pady=(0,10),sticky='nsew')

search_label = tk.Label(label_frame1, text="search an employee by input his number down",width=50, background='#b1f1a7')
search_label.grid(row=5,column=0,sticky='nsew')
search_entry = tk.Entry(label_frame1,width='25',border=1,relief="solid",background='#e1fae6')
search_entry.insert(0,'search for an employee')
search_entry.bind("<FocusIn>",lambda e:search_entry.delete('0','end'))
search_entry.grid(row=6,column=0,pady=(0,10),sticky='nsew')
search_button = tk.Button(label_frame1, text="search",background='#47b75f',command=search_employee)
search_button.grid(row=6,column=1,pady=(0,10),sticky='nsew')

list_box_frame = tk.LabelFrame(label_frame1,frame, text='show the employees',background='#b1f1a7',width='25',border=1,relief="solid")
list_box_frame.grid(row=7,column=0,pady=(0,10),sticky='nsew')
list_box = tk.Listbox(list_box_frame,height=3, background='#b1f1a7',selectbackground='#47b75f',highlightbackground='#47b75f',highlightthickness=1)
list_box.insert(1,'all')
list_box.insert(2,'sinior')
list_box.insert(3,'junior')


list_box.grid(pady=(0,10),sticky='nsew')
show_button = tk.Button(label_frame1, text="show",background='#47b75f',command=show_list_employees)
show_button.grid(row=7,column=1,pady=(6,10),sticky='nsew')

window.mainloop()