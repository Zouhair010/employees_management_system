import tkinter as tk
import tkinter.ttk as ttk
import csv
import os
from PIL import Image, ImageTk

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
        for i, name_key_rank in enumerate(bucket):
            if name_key_rank[0] == key:
                del bucket[i]
    def gett(self,key):
        index = self.hash_function(key)
        bucket = self.buckets[index]
        for info in bucket:
            if info[0] == key:
                return info

def load_employees(): #function to load employees info from a csv file
    try:
        if not os.path.exists('C:\\Users\\dell\\Desktop\\newdata.csv'): #check if the file is not exist
            fieldnames = ['ID','age','phone','fullname','email','salary'] #headers names
            with open('C:\\Users\\dell\\Desktop\\newdata.csv', 'w+', newline='') as csvfile: #creat a csv file and open it in the write mode
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames) # writer for write 
                writer.writeheader() # add the headers to the file
    
        with open('C:\\Users\\dell\\Desktop\\newdata.csv','r') as csvfile: #open the csv file in the read mod
            reader = csv.DictReader(csvfile) #convert the data on the csv file to dictionaries with keys names of columns and values is the data in rows
            data = [(row['ID'],row['age'],row['phone'],row['fullname'],row['email'],row['salary']) for row in reader] #list of dicts 
        return data
    except Exception as E:
        print('the process not done', E) #to show the type of the exception
        return None

data = load_employees() #employees info
length = len(data) 
if length == 0: #if the file is empty
    length = 10
hash_map = HashMap(length) #length of data as size of the hash map
for row in data:
    hash_map.add(row) #add  data to the hash map

def search_employee(): #search function for search for an employee by using hash map quick search 
    key = search_entry.get() #get the entry of the user
    info_employee = hash_map.gett(key)
    if key == '' or key == ' ' or key == '  ' or not any(char.isdigit() for char in key): #if the user enter nothing or space or double space tells him he should enter a key
        show_label['fg'] = 'red'
        show_label.config(text=f"you should enter id number")
        return
    if hash_map.contains(key): #quick check if an employee exist on file
        show_label['fg'] = 'green'
        show_label.config(text=f"{info_employee[3]} exist")
    elif not hash_map.contains(key): #quick check if an employee does not exist on file
        show_label['fg'] = 'red'
        show_label.config(text=f"the employee with the number {key} does not exist")

def add_employee():
    employee_info = (EmployeeID.get(),Employee_age.get(),Employee_phone.get(),Employee_name.get(),Employee_email.get(),Employee_salary.get()) #a tuple of entry that includes 'ID','age','phone','fullname','email','salary' of an employee
    if any( info=='' for info in employee_info): #if any of these entry that includes info are empty 
        show_label['fg'] = 'red'
        show_label.config(text=f"you should enter the right info")
        return
    #if the user enters the default text in any entry that should includes info of an employee
    elif EmployeeID.get()==' insert the Employee ID' or Employee_age.get()==' insert the Employee age' or Employee_phone.get()==' insert the Employee phone' or Employee_name.get()==' insert the Employee full name' or Employee_email.get()==' insert the Employee email' or Employee_salary.get()==' insert the Employee salary':
        show_label['fg'] = 'red'
        show_label.config(text=f"you should enter the employee info")
        return
    id= EmployeeID.get()
    if not hash_map.contains(id): #quick check if an employee not exist on file 
        hash_map.add(employee_info)
        # append an employee to the file
        fieldnames = ['ID','age','phone','fullname','email','salary']
        with open('C:\\Users\\dell\\Desktop\\newdata.csv','a',newline='') as csvfile:
            writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
            #append info of an employee
            writer.writerow({'ID': EmployeeID.get() ,'age': Employee_age.get(),'phone': Employee_phone.get(),'fullname': Employee_name.get() ,'email': Employee_email.get(),'salary': Employee_salary.get()})
        show_label['fg'] = 'green'
        show_label.config(text=f"{employee_info[3]} has been added")

    else: #if the employeer is already on the file
        show_label['fg'] = 'red'
        show_label.config(text=f"{employee_info[3]} is already added")

# remove function 
def remove_employee():
    key = EmployeeID.get()
    info_employee = hash_map.gett(key) #get the info employees from hash map by their number
    if key == '' or key == ' ' or key == '  ' or not any(char.isdigit() for char in key): #if the user enter nothing or space or double space tells him he should enter a key
        show_label['fg'] = 'red'
        show_label.config(text=f"you should enter the id number")
        return
    elif hash_map.contains(key): #quick check if an employee exist on file to remove it
        hash_map.remove(key)
        show_label['fg'] = 'green'
        show_label.config(text=f"{info_employee[3]} has been deleted")
        # apdate the employee file
        with open('C:\\Users\\dell\\Desktop\\newdata.csv','r') as csvfile: #open the csv file in the read mode
            reader = csv.DictReader(csvfile) #convert the data on the csv file to dictionaries with keys names of columns and values is the data in rows
            data = list(reader) #list of dicts
        data = [row for row in data if not (row['ID']==info_employee[0] and row['age']==info_employee[1] and row['phone']==info_employee[2] and row['fullname']==info_employee[3] and row['email']==info_employee[4] and row['salary']==info_employee[5])] #remove the info of employees the data 
        fieldnames = ['ID','age','phone','fullname','email','salary']
        with open('C:\\Users\\dell\\Desktop\\newdata.csv', 'w', newline='') as csvfile: #open the csv file in the write mode
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames) 
            writer.writeheader() # add the headers to the file
            writer.writerows(data) # write the updated data
    elif any(char.isdigit() for char in key): # tell user if the employee does not exist
        show_label['fg'] = 'red'
        show_label.config(text=f"the employee with the number {key} does not exist")

def show_list_employees():
    with open('C:\\Users\\dell\\Desktop\\newdata.csv','r') as csvfile:
        reader = csv.DictReader(csvfile)
        data = list(reader)
    columns = ("#1", "#2", "#3", "#4", "#5", "#6") #number of columns in the table
    tree = ttk.Treeview(list_frame, columns=columns, show="headings") #treeview that shows a table 
    fieldnames = ['ID','age','phone','fullname','email','salary'] #column names
    for i in range(1, 7): #numbers of columns
        tree.heading(f"#{i}", text=f"{fieldnames[i-1]}")
        tree.column(f"#{i}", width=160) #width of a column

    tree['style'] = 'Treeview'
    style = ttk.Style() #add style(colors ,font ...) to the table
    style.configure('Treeview', rowheight=25, background='#ceffa4', foreground='black') 
    style.map('Treeview', background=[('selected', '#1af125')],foreground=[('selected', 'black')])

    for d in data: #include employees info to the table to shows them
        tree.insert("", "end", values=(f"{d['ID']}", f"{d['age']}", 
                                         f"{d['phone']}", f"{d['fullname']}", 
                                         f"{d['email']}", f"{d['salary']}"))

    scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=tree.yview) #scrollbar to scroll up or down(vertically) the table that includes info
    tree.configure(yscroll=scrollbar.set)
    tree.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")


window = tk.Tk()
window.iconbitmap("C:\\Users\\dell\\Desktop\\online_information_marketing_social_contact_connection_internet_icon_230574.ico") #to change the default icon
window.resizable(False, False) #to make the size of the window constant
window.title("Employees Management")

frame = tk.Frame(window,background='#ceffa4')
frame.grid(row=0,column=1,sticky='nsew')

frame0 = tk.Frame(frame,background='#ceffa4',border=1,relief='solid',highlightbackground='#ceffa4')
frame0.grid(row=0,column=0,sticky='nsew')

search_entry = tk.Entry(frame0,width='25',border=1,relief="solid",background='#e1fae6')
search_entry.insert(0,' insert the Employee ID')
search_entry.bind("<FocusIn>",lambda e:search_entry.delete('0','end'))
search_entry.grid(row=0,column=1,sticky='nsew',pady=30 ,padx=(90,0))
search_label = tk.Label(frame0, text=" Enter the ID you are searching for ", fg='#08268a', background='#ceffa4' ,font=('Arial',10,'bold'))
search_label.grid(row=0,column=0,sticky='nsew')
search_button = tk.Button(frame0, text="Search",background='#23bfcd',width=20,font=('Arial',9,'bold'),command=search_employee)
search_button.grid(row=0,column=2,pady=30,sticky='nsew',padx=(33,0))

label_frame1 = tk.LabelFrame(frame, text='Employee info',background='#ceffa4',fg='#2c530c',highlightbackground='#ceffa4',highlightthickness=1,font=('Arial',10,'bold'))
label_frame1.grid(row=1,column=0,sticky='nsew')

frame1 = tk.Frame(frame, background='#ceffa4',border=1,relief='groove',highlightbackground='#ceffa4',pady=10)
frame1.grid(row=2,column=0,sticky='nsew')

frame2 = tk.Frame(frame, background='#ceffa4',border=1,relief='groove',highlightbackground='#ceffa4',height=100)
frame2.grid(row=3,column=0,sticky='nsew')

list_frame = tk.LabelFrame(frame, text='Employees list',background='#ceffa4',fg='#2c530c',width=980,height=300,border=1,relief="solid",font=('Arial',10,'bold'))
list_frame.grid(row=4,column=0,pady=(0,10),sticky='nsew')

show_label = tk.Label(frame1, text="", background='#ceffa4',width=50,font=('Arial',15,'bold'))
show_label.grid(row=0,column=0,sticky='nsew')

EmployeeID = tk.Entry(label_frame1,width='27',border=1,relief="solid",background='#e1fae6')
EmployeeID.insert(0,' insert the Employee ID')
EmployeeID.bind("<FocusIn>",lambda e:EmployeeID.delete('0','end'))
EmployeeID.grid(row=0,column=0,pady=(30,10),sticky='nsew',padx=(250,0))

Employee_age =tk.Entry(label_frame1,width='27',border=1,relief="solid",background='#e1fae6')
Employee_age.insert(0,' insert the Employee age')
Employee_age.bind("<FocusIn>",lambda e:Employee_age.delete('0','end'))
Employee_age.grid(row=1,column=0,pady=(0,10),sticky='nsew',padx=(250,0))

Employee_phone = tk.Entry(label_frame1,width='27',border=1,relief="solid",background='#e1fae6')
Employee_phone.insert(0,' insert the Employee phone')
Employee_phone.bind("<FocusIn>",lambda e:Employee_phone.delete('0','end'))
Employee_phone.grid(row=2,column=0,pady=(0,30),sticky='nsew',padx=(250,0))

Employee_name = tk.Entry(label_frame1,width='27',border=1,relief="solid",background='#e1fae6')
Employee_name.insert(0,' insert the Employee full name')
Employee_name.bind("<FocusIn>",lambda e:Employee_name.delete('0','end'))
Employee_name.grid(row=0,column=1,pady=(30,10),sticky='nsew', padx=(150,100))

Employee_email = tk.Entry(label_frame1,width='27',border=1,relief="solid",background='#e1fae6')
Employee_email.insert(0,' insert the Employee email')
Employee_email.bind("<FocusIn>",lambda e:Employee_email.delete('0','end'))
Employee_email.grid(row=1,column=1,pady=(0,10),sticky='nsew', padx=(150,100))

Employee_salary = tk.Entry(label_frame1,width='27',border=1,relief="solid",background='#e1fae6')
Employee_salary.insert(0,' insert the Employee salary')
Employee_salary.bind("<FocusIn>",lambda e:Employee_salary.delete('0','end'))
Employee_salary.grid(row=2,column=1,pady=(0,30),sticky='nsew', padx=(150,100))

add_button = tk.Button(frame2, background='#02a60b',text="Add",width=20,font=('Arial',9,'bold'),command=add_employee)
add_button.grid(row=0,column=1,pady=(10),sticky='nsew',padx=(250,10))
remove_button = tk.Button(frame2,background='#f21c1c', text="Remove",width=20,font=('Arial',9,'bold'),command=remove_employee)
remove_button.grid(row=0,column=2,pady=(10),sticky='nsew',padx=10)
show_button = tk.Button(frame2, text="Show Data",background='#f4df0f',width=20,font=('Arial',9,'bold'),command=show_list_employees)
show_button.grid(row=0,column=3,pady=(10),sticky='nsew',padx=(10,140))

window.mainloop()