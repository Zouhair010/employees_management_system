import tkinter as tk
import csv
# create the main window
window = tk.Tk()
window.geometry('600x400')
window.configure(bg='orange')
window.title("temployees management")


#frame
frame0 = tk.Frame(window,bg='orange')
frame1 = tk.Frame(window,bg='orange')
frame2 = tk.Frame(window,bg='orange')
frame3 = tk.Frame(window,bg='orange')
frame4 = tk.Frame(window,bg='orange')

frame0.grid(column=1,row=1)
# frame0.place(x=20,y=19)
frame1.grid(column=1,row=2)
frame2.grid(column=2,row=2)
frame3.grid(column=1,row=3)
frame4.grid(column=2,row=3)
# frame4.place(x=400,y=400)

#text to welcome the user
label = tk.Label(frame0, text="welcome to the employees management", height='2', fg='gold', font=('Arial',30,'bold','underline'),bg='orange',padx= 40)
label.grid()
# label.place()
# label to show the result
result_label = tk.Label(frame0, text="", fg='red', font=('Arial',15,'bold'),bg='orange')
result_label.grid()

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
        with open('C:\\Users\\dell\\Desktop\\datanew.csv','w+') as csvfile:
            csvfile.seek(0)
            reader = csv.DictReader(csvfile)
            data = [(row['number'],row['fname'],row['lname'],row['rank']) for row in reader]
        return data 
    except Exception as a:
        print('the process not done',a)
        return None

def push_hashmap():
    data = load_employees()
    hash_map = HashMap(20)
    if type(data) != 'NoneType':
        for row in data:
            hash_map.add(row)
    
    return hash_map

def add_employee():
    hash_map = push_hashmap()
    employee_info = add_entry.get()
    employee_info_whitespaces = []
    for char in employee_info:
        if char == ',':
            employee_info_whitespaces.append(' ')
        else:
            employee_info_whitespaces.append(char)
    string_employee_info_whitespaces = ''.join(employee_info_whitespaces)
    list_employee_info = string_employee_info_whitespaces.split()

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

def search_employee():
    hash_map = push_hashmap()
    key = search_entry.get()
    if key == '' or key == ' ' or key == '  ': #if the user enter nothing or space or double space tells him he should enter a key
        result_label['fg'] = 'red'
        result_label.config(text=f"you should enter a key")
        return
    if hash_map.contains(key): #quick check if an employee exist on file
        result_label['fg'] = 'green'
        result_label.config(text=f"{hash_map.get(key)} exist")
    elif not hash_map.contains(key):
        result_label['fg'] = 'red'
        result_label.config(text=f"{hash_map.get(key)} does not exist")

def remove_employee():
    hash_map = push_hashmap()
    key = remove_entry.get()
    info_employee = hash_map.get(key)
    if key == '' or key == ' ' or key == '  ': #if the user enter nothing or space or double space tells him he should enter a key
        result_label['fg'] = 'red'
        result_label.config(text=f"you should enter a key")
        return
    elif hash_map.contains(key): #quick check if an employee exist on file to remove it
        result_label['fg'] = 'green'
        result_label.config(text=f"{info_employee} has been deleted")
        hash_map.remove(key)
        # apdate the employee file
        with open('C:\\Users\\dell\\Desktop\\data.csv','r') as csvfile:
            reader = csv.DictReader(csvfile)
            data = list(reader)
            print('data befor deleting',data)
        data = [row for row in data if not (row['number']==info_employee[0] and row['fname']==info_employee[1] and row['lname']==info_employee[2] and row['rank']==info_employee[3])]
        fieldnames = ['number','fname','lname','rank']
        print('data after deleting',data)
        with open('C:\\Users\\dell\\Desktop\\data.csv', 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
    else: # tell user if the employee does not exist
        result_label['fg'] = 'red'
        result_label.config(text=f"{key} does not exist")

#search box
search_label = tk.Label(frame1, text="search for an employee",bg='orange')
search_label.grid(row=1)
search_entry = tk.Entry(frame1,width='25')
search_entry.grid(row=2)
search_button = tk.Button(frame1, text="search", width='20', height='1', bg='#F0E68C', command=search_employee)
search_button.grid(row=3)
#addition box
add_label = tk.Label(frame2, text="add an employee",bg='orange')
add_label.grid(row=1)
add_entry = tk.Entry(frame2,width='25')
add_entry.grid(row=2)
add_button = tk.Button(frame2, text="add",width='20', height='1', bg='#F0E68C', command=add_employee)
add_button.grid(row=3)
#delete box
remove_label = tk.Label(frame3, text="remove an employee",bg='orange')
remove_label.grid(row=1)
remove_entry =tk.Entry(frame3,width='25')
remove_entry.grid(row=2)
remove_button = tk.Button(frame3, text="remove", width='20', height='1', bg='#F0E68C',command=remove_employee)
remove_button.grid(row=3)
#password box
instraction_label = tk.Label(frame4, text="pravite information of employees",bg='orange')
instraction_label.grid(row=1)
print_entry = tk.Entry(frame4,width='25')
print_entry.grid(row=2)
print_button = tk.Button(frame4, text="show", width='20', height='1', bg='#F0E68C')
print_button.grid(row=3)
print_label = tk.Label(frame0, text="",height='4', fg='red', font=('Arial',15,'bold'),bg='orange')
print_label.grid()

#run the window
window.mainloop()