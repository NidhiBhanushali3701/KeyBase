from tkinter import *
from tkinter import messagebox
import sqlite3
from tkinter.ttk import Treeview

root = Tk()
root.geometry('783x423')
root.configure(background='#F0F8FF')
root.title('KeyBase')
conn = sqlite3.connect("database.db")
c = conn.cursor()
# Created Tables
#users table
c.execute(
"""
CREATE TABLE IF NOT EXISTS users (
     first_name text, 
     last_name text, 
     username text, 
     password text
)
"""
)
#passwords table
c.execute(
"""
CREATE TABLE IF NOT EXISTS passwords (
     username text, 
     application text, 
     app_email text, 
     app_username text, 
     app_password text
)
"""
)
#commit & close
conn.commit()
conn.close()

def register_user(first_name, last_name, username, password1, password2):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("SELECT username FROM users")
    username_list = c.fetchall()
    print("username list: ",username_list)
    if (username,) in username_list:
       wrong_username_error = Label(register, text="Username already exists!", fg="red").grid(row=8, column=1, columnspan= 3).grid(row=6, column=1, columnspan= 3)

    elif password1 == '' or password2 == '' or username == '' or first_name == '' or last_name == '':
        messagebox.showwarning(title='Input Warning', message='Please Enter all Data.')

    elif password1 != password2 :
        messagebox.showwarning(title='Input Warning', message='Passwords Dont match!!')
        
    else:
        password = password1
        
        c.execute("INSERT INTO users VALUES(:first_name, :last_name, :username, :password)",{'first_name' : first_name, 'last_name':last_name, 'username':username, 'password':password})
        message=messagebox.showinfo(title='Successfully Registered!', message='Please proceed to Login.')
        
        first_name_entry.delete(0,END)
        last_name_entry.delete(0,END)
        username_entry.delete(0,END)
        password1_entry.delete(0,END)
        password2_entry.delete(0,END)

        if message == 'ok':
            register.destroy()
        
       
    # c.execute("SELECT * FROM users")

    # first_name_entry.delete(0,END)
    # last_name_entry.delete(0,END)
    # username_entry.delete(0,END)
    # password1_entry.delete(0,END)
    # password2_entry.delete(0,END)


    conn.commit()
    conn.close()


def login_user(username, password):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    all_users = c.fetchall()
    print("all users: ",all_users)
    global user
    if username!="" and password!="":
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?",(username, password))
        user = c.fetchall()
        if user:
            print(user)
            main_screen(user)
        else:
            no_user_error =  Label(login, text="No such user exists!", fg="red").grid(row=4, column=1, columnspan= 3)
    else:
        login_error = Label(login, text="Please ented all fields!", fg="red").grid(row=4, column=1, columnspan= 3)

    conn.commit()
    conn.close()

def login():
    global login
    login = Toplevel()
    login.title("Login Page")
    
    login.configure(background='#F0F8FF')
    login.title('Login: KeyBase')

    global username_login
    global password_login


    Label(login, text='Login ', bg='#F0F8FF', font=('verdana', 30, 'bold')).grid(row =0, column=0, columnspan=2)
    username_login = Entry(login, width=30)
    username_login.grid(row = 2, column=1)
    password_login = Entry(login, width=30, show="*")
    password_login.grid(row = 3, column=1)


    username_loginlabel = Label(login, text="Username", bg='#F0F8FF', font=('arial', 20, 'normal')).grid(row = 2, column=0)
    password_loginlabel = Label(login, text="Password", bg='#F0F8FF', font=('arial', 20, 'normal')).grid(row = 3, column=0)

    login_btn = Button(login, text="Login", bg='#8EE5EE', font=('courier', 10, 'italic'),command=lambda: login_user(username_login.get(), password_login.get())).grid(row = 5, column=0, columnspan=2)


def register():
    global register
    register = Toplevel()
    register.geometry('783x423')
    register.configure(background='#F0F8FF')
    register.title('Register: KeyBase')
    
    Label(register, text='Register as New User', bg='#F0F8FF', font=('verdana', 30, 'bold')).grid(row =0, column=0, columnspan=2)

    global first_name_entry
    global last_name_entry
    global username_entry
    global password1_entry
    global password2_entry
    
    first_name_entry = Entry(register, width=30)
    first_name_entry.grid(row =2, column = 1)
    last_name_entry = Entry(register, width=30)
    last_name_entry.grid(row = 3, column=1)
    username_entry = Entry(register, width=30)
    username_entry.grid(row = 4, column=1)
    password1_entry = Entry(register, width=30)
    password1_entry.grid(row = 5, column=1)
    password2_entry = Entry(register, width=30)
    password2_entry.grid(row = 6, column=1)

    first_name_label = Label(register, text='First Name: ', bg='#F0F8FF', font=('arial', 20, 'normal')).grid(row= 2, column = 0)
    last_name_label = Label(register, text="Last Name: ", bg='#F0F8FF', font=('arial', 20, 'normal')).grid(row= 3, column = 0)
    username_label = Label(register, text="Username", bg='#F0F8FF', font=('arial', 20, 'normal')).grid(row = 4, column=0)
    password1_label = Label(register, text="Password", bg='#F0F8FF', font=('arial', 20, 'normal')).grid(row = 5, column=0)
    password2_label = Label(register, text="Confirm Password",  bg='#F0F8FF', font=('arial', 20, 'normal')).grid(row = 6, column=0)

    register_btn = Button(register, text="Register", bg='#8EE5EE', font=('courier', 10, 'italic'), command=lambda: register_user(first_name_entry.get(), last_name_entry.get(), username_entry.get(), password1_entry.get(), password2_entry.get())).grid(row = 7, column=0, columnspan=2)



def add_password_form(user):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    global app_name
    global app_email
    global app_username
    global app_password
    app_name = Entry(keybase, width=30)
    app_name.grid(row=4, column=1)
    app_email = Entry(keybase, width=30)
    app_email.grid(row=5, column=1)
    app_username = Entry(keybase, width=30)
    app_username.grid(row=6, column=1)
    app_password = Entry(keybase, width=30)
    app_password.grid(row=7, column=1)

    # newpass_list = [app_name.get(), app_email.get(), app_username.get(), app_password.get()]
    global app_name_label
    global app_email_label
    global app_username_label
    global app_password_label
    global add_new_button

    app_name_label = Label(keybase, text="Application Name ",bg='#F0F8FF', font=('courier', 10, 'italic'))
    app_name_label.grid(row=4, column=0)
    app_email_label = Label(keybase, text="Application email ",bg='#F0F8FF', font=('courier', 10, 'italic'))
    app_email_label.grid(row=5, column=0)
    app_username_label = Label(keybase, text="Application username ",bg='#F0F8FF', font=('courier', 10, 'italic'))
    app_username_label.grid(row=6, column=0)
    app_password_label = Label(keybase, text="Application password ",bg='#F0F8FF', font=('courier', 10, 'italic'))
    app_password_label.grid(row=7, column=0)
    add_new_button = Button(keybase, padx=10, pady = 5, bg='#8EE5EE', font=('courier', 10, 'italic'), text="Add", command=lambda: add_new_password(user))
    add_new_button.grid(row=8,column=0)

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
    # for j in range(1,5):

    #     Label(keybase, text=pass_records[len(pass_records)-1][j]).grid(row = (len(pass_records)-1+8), column=(j-1))
    listbox.insert("","end",values = (len(pass_records),newpass_list[0], newpass_list[1], newpass_list[2], newpass_list[3]))
    listbox.grid(row = 2, column=0,columnspan = 3)


    print(pass_records)
    
    conn.commit()
    conn.close()

def selected_item(a):
    global curItem
    global curr_values_list
    global curItem_id
    global update_entry_button
    global delete_entry_button
    curItem = listbox.focus()
    curItem_id = listbox.selection()[0]
    print(listbox.selection()[0])
    curr_values_list = listbox.item(curItem)['values']
    print(listbox.item(curItem)['values'])
    update_entry_button = Button(keybase, padx=5, pady = 5, relief = 'solid', bg='#8EE5EE', font=('courier', 10, 'italic'),  text="Update an Entry", command=update_entry_form)
    update_entry_button.grid(row=3,column=1)
    delete_entry_button = Button(keybase, padx=5, pady = 5, relief = 'solid', bg='#8EE5EE', font=('courier', 10, 'italic'),  text="Delete an Entry", command=delete_entry)
    delete_entry_button.grid(row=3,column=2)


# DELETE START

def delete_entry():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    
    c.execute("DELETE FROM passwords WHERE application = ? AND app_username = ?",(curr_values_list[1],curr_values_list[3],))
    listbox.delete(curItem_id)
    update_entry_button.grid_forget()
    delete_entry_button.grid_forget()
    


    conn.commit()
    conn.close()


# Update Function form
# Update Function form
def update_entry_form():

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    global update_app_name
    global update_app_email
    global update_app_username
    global update_app_password
    update_app_name = Entry(keybase,textvariable=curr_values_list[0], width=30)
    update_app_name.grid(row=4, column=1)
    update_app_name.insert(0,curr_values_list[1])
    update_app_email = Entry(keybase, width=30)
    update_app_email.grid(row=5, column=1)
    update_app_email.insert(0,curr_values_list[2])
    update_app_username = Entry(keybase, width=30)
    update_app_username.grid(row=6, column=1)
    update_app_username.insert(0,curr_values_list[3])
    update_app_password = Entry(keybase, width=30)
    update_app_password.grid(row=7, column=1)
    update_app_password.insert(0,curr_values_list[4])

    
    global update_app_name_label
    global update_app_email_label
    global update_app_username_label
    global update_app_password_label
    global update_password_button

    update_app_name_label = Label(keybase, text="Application Name ",bg='#F0F8FF', font=('courier', 10, 'italic'))
    update_app_name_label.grid(row=4, column=0)
    update_app_email_label = Label(keybase, text="Application email ",bg='#F0F8FF', font=('courier', 10, 'italic'))
    update_app_email_label.grid(row=5, column=0)
    update_app_username_label = Label(keybase, text="Application username ",bg='#F0F8FF', font=('courier', 10, 'italic'))
    update_app_username_label.grid(row=6, column=0)
    update_app_password_label = Label(keybase, text="Application password ",bg='#F0F8FF', font=('courier', 10, 'italic'))
    update_app_password_label.grid(row=7, column=0)
    print("Update function : ",[current_user,curr_values_list[0],curr_values_list[1],update_app_email.get(),update_app_username.get(),update_app_password.get()])
    update_password_button = Button(keybase, text="Update", padx=5, pady = 5, relief = 'solid',  bg='#8EE5EE', font=('courier', 10, 'italic'), command=lambda: update_user_appDetails([current_user,curr_values_list[0],curr_values_list[1],update_app_email.get(),update_app_username.get(),update_app_password.get() ,update_app_name.get()]))#add_new_password(user))
    
    update_password_button.grid(row=8,column=0)

    conn.commit()
    conn.close()

# Create update function to add values to database
def update_user_appDetails(user_updated_appDetails):
  conn = sqlite3.connect('database.db')
  c = conn.cursor()
  c.execute("""
  UPDATE passwords SET 
  application = (:update_app_name),
  app_email = (:app_email) , 
  app_username = (:app_username) , app_password = (:app_password) 
  WHERE username = (:username) AND application = (:app_name)
  """,{'app_email':user_updated_appDetails[3],'username':user_updated_appDetails[0],'app_name':user_updated_appDetails[2],
  'app_username':user_updated_appDetails[4],'app_password':user_updated_appDetails[5], 'update_app_name':user_updated_appDetails[6]})
  listbox.item(curItem, text="", values=(user_updated_appDetails[1],user_updated_appDetails[6], user_updated_appDetails[3], user_updated_appDetails[4], user_updated_appDetails[5]))
  update_app_name.grid_forget()
  update_app_email.grid_forget()
  update_app_username.grid_forget()
  update_app_password.grid_forget()


  update_app_name_label.grid_remove()
  update_app_email_label.grid_remove()
  update_app_username_label.grid_remove()
  update_app_password_label.grid_remove()

  update_password_button.grid_remove()
    
  conn.commit()
  conn.close()



def main_screen(user):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    login.destroy()
    global keybase
    keybase = Toplevel()
    keybase.configure(background='#F0F8FF')
    keybase.title("Keybase")
    welcome_label = Label(keybase, text="Welcome "+user[0][0],bg='#F0F8FF', font=("Verdana",20)).grid(row=0, columnspan=3)
    print(user)
    

    add_password_button = Button(keybase, text="Add new Password", command=lambda: add_password_form(user), padx=5, pady = 5, relief = 'solid',  bg='#8EE5EE', font=('courier', 10, 'italic')).grid(row=3,column=0, pady=20)
    global current_user
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
    label = Label(keybase, text="Your Passwords",bg='#F0F8FF', font=("Verdana",26)).grid(row=1, columnspan=3)
    cols = ('Serial Number','Application Name','Email','Username','Password')
    listbox = Treeview(keybase, columns = cols, show = 'headings', selectmode='browse')

    listbox.bind('<ButtonRelease-1>', selected_item)
    for i, (appname, appmail, appusername, apppassword) in enumerate(templist, start = 1):
        listbox.insert("","end",values = (i,appname, appmail, appusername, apppassword))

    for col in cols:
        listbox.heading(col, text=col)
    listbox.grid(row = 2, column=0, columnspan = 3)

    
    # closeButton = Button(keybase, text="Close", width=15, command=exit).grid(row=4, column=1)

    

    
    



    conn.commit()
    conn.close()


Label(root, text='Welcome to Keybase!', bg='#F0F8FF', font=('verdana', 30, 'bold')).place(x=143, y=86)
login = Button(root, text='Login', bg='#8EE5EE', font=('courier', 20, 'bold'),padx=10, pady=10, relief = "solid", borderwidth = 2, command=login)
login.place(x=233, y=186)
register = Button(root, text='Register', bg='#8EE5EE', font=('courier', 20, 'bold'), command=register, padx=10, pady=10, relief = "solid", borderwidth = 2)
register.place(x=429, y=186)




root.mainloop()
