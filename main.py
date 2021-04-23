from tkinter import *
import sqlite3
from tkinter.ttk import Treeview

root = Tk()
root.geometry('783x423')
root.configure(background='#F0F8FF')
root.title('KeyBase')
conn = sqlite3.connect("database.db")
c = conn.cursor()
# Created Tables
c.execute("""
CREATE TABLE IF NOT EXISTS users (
        first_name text, 
        last_name text, 
        username text, 
        password text
)
""")
c.execute("""
CREATE TABLE IF NOT EXISTS passwords (
        username text, 
        application text, 
        app_email text, 
        app_username text, 
        app_password text
)
""")
#commit & close 
conn.commit()
conn.close()

def register_user(first_name, last_name, username, password1, password2):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    global up_register
    if (first_name!='' and last_name!='' and username!='' and password1!='' and password2!=''):
      if (password1 == password2):
        password = password1
        c.execute("INSERT INTO users VALUES(:first_name, :last_name, :username, :password)",{'first_name' : first_name, 'last_name':last_name, 'username':username, 'password':password})
        conn.commit()
      else:
        messagebox.showwarning(title='Password Warning', message="Both Password don't match!")
        print()
        #wrong_password_error = Label(register, text="Passwords dont match!", fg="red").grid(row=6, column=1, columnspan= 3).grid(row=6, column=1, columnspan= 3)
      # c.execute("SELECT * FROM users")
    else:
      messagebox.showwarning(title='Input Warning', message='Please Enter all Data.')
      print()
      #wrong_password_error = Label(register, text="Enter all data!", fg="red").grid(row=6, column=1, columnspan= 3).grid(row=6, column=1, columnspan= 3)
    
    first_name_entry.delete(0,END)
    last_name_entry.delete(0,END)
    username_entry.delete(0,END)
    password1_entry.delete(0,END)
    password2_entry.delete(0,END)

    register_success = Label(register, text="Registeration Successful!", fg="green").grid(row=6, column=1, columnspan= 3)
    c.execute("SELECT * FROM users WHERE username = (:un) AND password = (:pass) ",{'un':username,'pass':password1})
    up_register = c.fetchall()
    main_screen(up_register)
    conn.commit()
    conn.close()


def login_user(username, password):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    if username!="" and password!="":
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?",(username, password))
        rows = c.fetchall()
        if rows:
            print(rows)
            main_screen(rows)
        else:
            messagebox.showwarning(title='User Warning', message='No such user exists!')
            #no_user_error =  Label(login, text="No such user exists!", fg="red").grid(row=4, column=1, columnspan= 3)
    else:
      messagebox.showerror(title='Input Error', message='Please Enter all Data.')
      #login_error = Label(login, text="Please ented all fields!", fg="red").grid(row=4, column=1, columnspan= 3)

    conn.commit()
    conn.close()

def login():
    global login
    login = Toplevel()
    login.title("Login Page")
    login.geometry('783x423')
    login.configure(background='#F0F8FF')

    global username_login
    global password_login
    Label(register, text='Log In as Existing User', bg='#F0F8ff', font=('verdana', 30, 'bold')).place(x=125, y=40)
    
    username_login = Entry(login, width=30).place(x=300,y=150,height = 30)
    password_login = Entry(login, width=30, show="*").place(x=300,y=250,height = 30)

    username_loginlabel = Label(login, text="Username", bg='#F0F8FF', font=('arial', 20, 'normal')).place(x=60,y=150)
    password_loginlabel = Label(login, text="Password", bg='#F0F8FF', font=('arial', 20, 'normal')).place(x=60,y=250)

    login_btn = Button(login, text="Login",bg='#8EE5EE', font=('courier', 15, 'italic'), command=lambda: (login_user(username_login.get(), password_login.get()))).place(x=200,y=350,height=60,width = 175)
    print(username_login.get(),password_login.get())


def register():
    global register
    register = Toplevel()
    register.geometry('783x423')
    register.configure(background='#F0F8FF')
    register.title('Register: KeyBase')
    
    Label(register, text='Register as New User', bg='#F0F8ff', font=('verdana', 30, 'bold')).place(x=125, y=40)

    global first_name_entry
    global last_name_entry
    global username_entry
    global password1_entry
    global password2_entry
    
    first_name_entry = Entry(register, width=30)
    first_name_entry.place(x=300,y=150,height = 30)
    last_name_entry = Entry(register, width=30)
    last_name_entry.place(x=300,y=200,height = 30)
    username_entry = Entry(register, width=30)
    username_entry.place(x=300,y=250,height = 30)
    password1_entry = Entry(register, width=30)
    password1_entry.place(x=300,y=300,height = 30)
    password2_entry = Entry(register, width=30)
    password2_entry.place(x=350,y=355,height = 30)

    first_name_label = Label(register, text='First Name: ', bg='#F0F8FF', font=('arial', 20, 'normal')).place(x=60,y=150)
    last_name_label = Label(register, text="Last Name: ", bg='#F0F8FF', font=('arial', 20, 'normal')).place(x=60,y=200)
    username_label = Label(register, text="Username", bg='#F0F8FF', font=('arial', 20, 'normal')).place(x=60,y=250)
    password1_label = Label(register, text="Password", bg='#F0F8FF', font=('arial', 20, 'normal')).place(x=60,y=300)
    password2_label = Label(register, text="Confirm Password", bg='#F0F8FF', font=('arial', 20, 'normal')).place(x=60,y=350)

    register_btn = Button(register, text="Register",bg='#8EE5EE', font=('courier', 15, 'italic'),command=lambda: register_user(first_name_entry.get(), last_name_entry.get(), username_entry.get(), password1_entry.get(), password2_entry.get())).place(x=200,y=400,height=60,width = 175)
    #main_screen(up_register)



def add_password_form(user):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    global app_name
    global app_email
    global app_username
    global app_password
    app_name = Entry(keybase, width=30)
    app_name.grid(row=2, column=1)
    app_email = Entry(keybase, width=30)
    app_email.grid(row=3, column=1)
    app_username = Entry(keybase, width=30)
    app_username.grid(row=4, column=1)
    app_password = Entry(keybase, width=30)
    app_password.grid(row=5, column=1)

    # newpass_list = [app_name.get(), app_email.get(), app_username.get(), app_password.get()]
    global app_name_label
    global app_email_label
    global app_username_label
    global app_password_label
    global add_new_button

    app_name_label = Label(keybase, text="Application Name ")
    app_name_label.grid(row=2, column=0)
    app_email_label = Label(keybase, text="Application email ")
    app_email_label.grid(row=3, column=0)
    app_username_label = Label(keybase, text="Application username ")
    app_username_label.grid(row=4, column=0)
    app_password_label = Label(keybase, text="Application password ")
    app_password_label.grid(row=5, column=0)
    add_new_button = Button(keybase, text="Add", command=lambda: add_new_password(user))
    add_new_button.grid(row=6,column=0)

    conn.commit()
    conn.close()


def add_new_password(user):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    newpass_list = [app_name.get(), app_email.get(), app_username.get(), app_password.get()]
    # print(newpass_list)
    # print(user)

    c.execute("INSERT INTO passwords VALUES(:username, :application , :app_email,:app_username,:app_password)",{'username' : user[0][2], 'application':newpass_list[0], 'app_email':newpass_list[1],'app_username':newpass_list[2], 'app_password':newpass_list[3]})
    # keybase.destroy()]
    app_name.grid_forget()
    app_email.grid_forget()
    app_username.grid_forget()
    app_password.grid_forget()


    app_name_label.grid_remove()
    app_email_label.grid_remove()
    app_username_label.grid_remove()
    app_password_label.grid_remove()

    add_new_button.grid_remove()

    current_user = user[0][2]

    c.execute("SELECT * FROM passwords WHERE username = ?",(current_user,))
    pass_records = c.fetchall()
    for j in range(1,5):

        Label(keybase, text=pass_records[len(pass_records)-1][j]).grid(row = (len(pass_records)-1+8), column=(j-1))

    print(pass_records)
    
    


    conn.commit()
    conn.close()

def selected_item(current_user,a):
    curItem = listbox.focus()
    curr_values_list = listbox.item(curItem)['values']
    # print(listbox.item(curItem)['values'])
    
    update_entry_button = Button(keybase, text="Update an Entry", command=lambda: update_entry_form(current_user,curr_values_list)).grid(row=0,column=2)


# Update Function form
def update_entry_form(username,*curr_values_list):

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    global app_name
    global app_email
    global app_username
    global app_password
    app_name = Entry(keybase,textvariable=curr_values_list[0], width=30,state = DISABLED)
    app_name.grid(row=2, column=1)
    #app_name.insert(0,curr_values_list[0])
    app_email = Entry(keybase, width=30)
    app_email.grid(row=3, column=1)
    app_email.insert(0,curr_values_list[1])
    app_username = Entry(keybase, width=30)
    app_username.grid(row=4, column=1)
    app_username.insert(0,curr_values_list[2])
    app_password = Entry(keybase, width=30)
    app_password.grid(row=5, column=1)
    app_password.insert(0,curr_values_list[3])

    
    global app_name_label
    global app_email_label
    global app_username_label
    global app_password_label
    global add_new_button

    app_name_label = Label(keybase, text="Application Name ")
    app_name_label.grid(row=2, column=0)
    app_email_label = Label(keybase, text="Application email ")
    app_email_label.grid(row=3, column=0)
    app_username_label = Label(keybase, text="Application username ")
    app_username_label.grid(row=4, column=0)
    app_password_label = Label(keybase, text="Application password ")
    app_password_label.grid(row=5, column=0)
    add_new_button = Button(keybase, text="Add", command=lambda: update_user_appDetails(username,curr_values_list[0],app_email.get(),app_username.get(),app_password.get()))#add_new_password(user))
    add_new_button.grid(row=6,column=0)

    conn.commit()
    conn.close()

# Create update function to add values to database
def update_user_appDetails(user_updated_appDetails):
  conn = sqlite3.connect('database.db')
  c = conn.cursor()
  c.execute("""
  UPDATE passwords SET 
  app_email = (:app_email) , 
  app_username = (:app_username) , app_password = (:app_password) 
  WHERE username = (:username) AND application = (:app_name)
  """,{'app_email':user_updated_appDetails[2],'username':user_updated_appDetails[0],'app_name':user_updated_appDetails[1],
  'app_username':user_updated_appDetails[3],'app_password':user_updated_appDetails[4]})
  conn.commit()
  conm.close()


    






def main_screen(user):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    login.destroy()
    global keybase
    keybase = Toplevel()
    keybase.title("Keybase")
    welcome_label = Label(keybase, text="Welcome "+user[0][0]).grid(row=6, column=1, columnspan= 3)
    print(user)
    

    add_password_button = Button(keybase, text="Add new Password", command=lambda: add_password_form(user)).grid(row=0,column=0)
    current_user = user[0][2]
    print(current_user)
    c.execute("SELECT * FROM passwords WHERE username = ?",(current_user,))
    pass_records = c.fetchall()
    templist = []
    for i in range(len(pass_records)):
        x = []
        for j in range(1,5):
            x.append(pass_records[i][j])
        templist.append(x)

    # print(pass_records)
    # print(pass_records[0][1])
    # print(pass_records[0][2])
    # print(pass_records[0][3])

    # appname_table = Label(keybase, text="Application Name").grid(row=7, column = 0)
    # appemail_table = Label(keybase, text="Email").grid(row=7, column = 1)
    # appusername_table = Label(keybase, text="Username").grid(row=7, column = 2)
    # apppassword_table = Label(keybase, text="Password").grid(row=7, column = 3)

    # for i in range(len(pass_records)):
    #     for j in range(1,5):
    #         Label(keybase, text=pass_records[i][j]).grid(row = (i+8), column=(j-1))

    global listbox
    label = Label(keybase, text="Your Passwords", font=("Arial",30)).grid(row=0, columnspan=3)
    cols = ('Serial Number','Application Name','Email','Username','Password')
    listbox = Treeview(keybase, columns = cols, show = 'headings')
    listbox.bind('<ButtonRelease-1>', selected_item(current_user))
    for i, (appname, appmail, appusername, apppassword) in enumerate(templist, start = 1):
        listbox.insert("","end",values = (i,appname, appmail, appusername, apppassword))

    for col in cols:
        listbox.heading(col, text=col)
    listbox.grid(row = 1, column=0,columnspan = 2)

    
    # closeButton = Button(keybase, text="Close", width=15, command=exit).grid(row=4, column=1)

    

    
    



    conn.commit()
    conn.close()


Label(root, text='Welcome to Keybase!', bg='#F0F8FF', font=('verdana', 30, 'bold')).place(x=143, y=86)
login = Button(root, text='Login', bg='#8EE5EE', font=('courier', 15, 'italic'), command=login).place(x=233, y=186,height = 50)
register = Button(root, text='Register',bg='#8EE5EE', font=('courier', 15, 'italic'), command=register).place(x=429, y=186,height = 50)




root.mainloop()
