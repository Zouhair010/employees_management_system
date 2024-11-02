import tkinter as tk
import csv

window = tk.Tk()
# window.geometry('600x400')
window.title("temployees management")

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
    def remove(self,key):
        index = self.hash_function(key)
        bucket = self.buckets[index]
        for i, info in enumerate(bucket):
            if info[0] == key:
                del bucket[i]
    def get(self,key):
        index = self.hash_function(key)
        bucket = self.buckets[index]
        for info in bucket:
            if info[0] == key:
                return info


def load_employees():
    try:
        with open('C:\\Users\\dell\\Desktop\\data.csv','r') as csvfile: #open the csv file in the read mod
            reader = csv.DictReader(csvfile) #convert the data on the csv file to dictionaries with keys names of columns and values is the data in rows
            data = [(row['number'],row['fname'],row['lname'],row['rank']) for row in reader] #list of dicts 
        return data 
    except Exception as a:
        print('the process not done',a) #to show the type of the exception
        return None

def push_hashmap():
    data = load_employees()
    length = len(data) 
    if length == 0:
        length = 10
    hash_map = HashMap(length) #length of data as size of the hash map
    for row in data:
        hash_map.add(row) #add  data to the hash map
    return hash_map #return the jash map instance

#search function for search for an employee by using hash map quick search 
def search_employee():
    hash_map = push_hashmap() #the hash map 
    key = search_entry.get() #get the entry of the user
    if key == '' or key == ' ' or key == '  ': #if the user enter nothing or space or double space tells him he should enter a key
        result_label['fg'] = 'red'
        result_label.config(text=f"you should enter a key")
        return
    if hash_map.contains(key): #quick check if an employee exist on file
        result_label['fg'] = 'green'
        result_label.config(text=f"{hash_map.get(key)} exist")
    elif not hash_map.contains(key): #quick check if an employee does not exist on file
        result_label['fg'] = 'red'
        result_label.config(text=f"{hash_map.get(key)} does not exist")

def add_employee():
    hash_map = push_hashmap()
    employee_info = add_entry.get() #get the entry of the user
    employee_info_whitespaces = [] # list chars in info with whitespaces to make them separate words after
    for char in employee_info:
        if char == ',':
            employee_info_whitespaces.append(' ') #replace the camma with whitespace
        else:
            employee_info_whitespaces.append(char)
    string_employee_info_whitespaces = ''.join(employee_info_whitespaces) #convert the list of chars in employee info to string
    list_employee_info = string_employee_info_whitespaces.split() # separate the string to list of info ['number', 'first_name', 'last_name', 'rank']

    if list_employee_info == '' or list_employee_info == ' ' or list_employee_info == '  ' or len(list_employee_info)<3: #if the user enter nothing or space or double space tells him he should enter a key
        result_label['fg'] = 'red'
        result_label.config(text=f"you should enter a key")
        return
    key= list_employee_info[0]
    if not hash_map.contains(key): #quick check if an employee not to add it exist on file 
                # append an employee to the file
        fieldnames = ['number','fname','lname','rank']
        with open('C:\\Users\\dell\\Desktop\\data.csv','a',newline='') as csvfile:
            writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
            # writer.writeheader()
            writer.writerow({'number':f'{list_employee_info[0]}','fname':f'{list_employee_info[1]}','lname':f'{list_employee_info[2]}','rank':f'{list_employee_info[3]}'})
        hash_map.add(employee_info)
        result_label['fg'] = 'green'
        result_label.config(text=f"{list_employee_info[1]} {list_employee_info[2]} has been added")

    else: #if the employeer is already on the file
        result_label['fg'] = 'red'
        result_label.config(text=f"{list_employee_info[1]} {list_employee_info[2]} is already added")

# remove function 
def remove_employee():
    hash_map = push_hashmap()
    key = remove_entry.get()
    info_employee = hash_map.get(key) #get the info employees from hash map by their number
    if key == '' or key == ' ' or key == '  ': #if the user enter nothing or space or double space tells him he should enter a key
        result_label['fg'] = 'red'
        result_label.config(text=f"you should enter a key")
        return
    elif hash_map.contains(key): #quick check if an employee exist on file to remove it
        result_label['fg'] = 'green'
        result_label.config(text=f"{info_employee} has been deleted")
        hash_map.remove(key)
        # apdate the employee file
        with open('C:\\Users\\dell\\Desktop\\data.csv','r') as csvfile: #open the csv file in the read mode
            reader = csv.DictReader(csvfile) #convert the data on the csv file to dictionaries with keys names of columns and values is the data in rows
            data = list(reader) #list of dicts
        data = [row for row in data if not (row['number']==info_employee[0] and row['fname']==info_employee[1] and row['lname']==info_employee[2] and row['rank']==info_employee[3])] #remove the info of employees the data 
        fieldnames = ['number','fname','lname','rank'] 
        with open('C:\\Users\\dell\\Desktop\\data.csv', 'w', newline='') as csvfile: #open the csv file in the write mode
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames) 
            writer.writeheader() # add the headers to the file
            writer.writerows(data) # write the updated data
    else: # tell user if the employee does not exist
        result_label['fg'] = 'red'
        result_label.config(text=f"{key} does not exist")


def show_employees():
    info_employees = load_employees()
    password = show_entry.get()
    if password == 'employees':
        show_label['foreground'] = 'black'
        show_label['text']= f'{info_employees}'
        
    else:
        show_label['foreground'] = 'red'
        show_label['text']= 'wrong password'


frame = tk.Frame(window,border=2,background='#b1f1a7', relief="solid")
frame.pack()

label_frame1 = tk.LabelFrame(frame, text='Info Manipulation',background='#b1f1a7')
label_frame1.grid(row=0,column=0,sticky='nsew')

label_frame3 = tk.LabelFrame(frame ,background='#b1f1a7', text='result')
label_frame3.grid(row=0,column=1,sticky='nsew')


result_label = tk.Label(label_frame3 ,text='',background='#b1f1a7',foreground='black',border=1,relief='solid')
result_label.grid(row=0,column=0,sticky='nsnsew')

label_frame2 = tk.LabelFrame(frame, text='Searching Info   ',background='#b1f1a7')
label_frame2.grid(row=1,column=0,pady=(17,0),sticky='nsew')

add_entry = tk.Entry(label_frame1,width='25',border=1,relief="solid",background='#e1fae6')
add_entry.insert(0,'add an employee')
add_entry.bind("<FocusIn>",lambda e:add_entry.delete('0','end'))
add_entry.grid(row=0,column=0,pady=(10,0),sticky='nsew')
add_button = tk.Button(label_frame1, background='#47b75f',text="add",command=add_employee)
add_button.grid(row=1,column=0,padx=5,sticky='nsew')

remove_entry =tk.Entry(label_frame1,width='25',border=1,relief="solid",background='#e1fae6')
remove_entry.insert(0,'remove an employee')
remove_entry.bind("<FocusIn>",lambda e:remove_entry.delete('0','end'))
remove_entry.grid(row=3,column=0,pady=(10,0),sticky='nsew')
remove_button = tk.Button(label_frame1,background='#47b75f', text="remove",command=remove_employee)
remove_button.grid(row=4,column=0,padx=5,sticky='nsew')

search_entry = tk.Entry(label_frame2,width='25',border=1,relief="solid",background='#e1fae6')
search_entry.insert(0,'search for an employee')
search_entry.bind("<FocusIn>",lambda e:search_entry.delete('0','end'))
search_entry.grid(row=0,column=0,pady=(10,0),sticky='nsew')
search_button = tk.Button(label_frame2, text="search",background='#47b75f',command=search_employee)
search_button.grid(row=1,column=0,padx=5,sticky='nsew')

show_entry = tk.Entry(label_frame2,width='25',border=1,relief="solid",background='#e1fae6')
show_entry.insert(0,'password')
show_entry.bind("<FocusIn>",lambda e: show_entry.delete('0','end'))
show_entry.grid(row=2,pady=(10,0),sticky='nsew')
show_button = tk.Button(label_frame2,background='#47b75f', text="show",command=show_employees)
show_button.grid(row=3,column=0,padx=5,sticky='nsew')
show_label = tk.Label(label_frame3, text="",width=100, wraplength=200, background='#b1f1a7')
show_label.grid(row=1,column=0,sticky='nsew')

window.mainloop()