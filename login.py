import tkinter as tk
from tkinter import messagebox, ttk
from PIL import ImageTk
import pymysql
import bcrypt
import globals
import os
from dotenv import load_dotenv

# 加載 .env 文件中的環境變數
load_dotenv()

# db connection setting
def connect_db():
    return pymysql.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USERNAME'),
        password=os.getenv('DB_PASSWORD'),
        database='movie_review_system'
    )

#for admin generation
"""
def register_admin(username, password):
    # 將密碼進行雜湊處理
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO Users (username, email, password_hash, is_admin) VALUES (%s, %s, %s, True);"
            cursor.execute(sql, (username, 'root@gmail.com', password_hash))
        connection.commit()
    except pymysql.MySQLError as e:
        messagebox.showerror('Error',f'Error: {e}')
    finally:
        connection.close()

register_admin('root', '123')
"""

#Functional Part
def register():
    def register_user(username, password):
        if register_username_entry.get() == '' or email_entry.get() == '' or register_password_entry.get() == '':
            messagebox.showerror('Error','Fields cannot be empty')
        else:
            # 將密碼進行雜湊處理
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            connection = connect_db()
            try:
                with connection.cursor() as cursor:
                    sql = "INSERT INTO Users (username, email, password_hash, is_admin) VALUES (%s, %s, %s, False);"
                    cursor.execute(sql, (username, email_entry.get(), password_hash))
                connection.commit()
                messagebox.showinfo('Successfully',f"User {username} registered successfully.")
                screen.destroy()
            except pymysql.MySQLError as e:
                messagebox.showerror('Error',f'Error: {e}')
            finally:
                connection.close()

    screen = tk.Toplevel()
    screen.title('Register')
    screen.resizable(False,False)
    screen.grab_set()
    #name entry
    register_username_label = tk.Label(screen, text='Name', font=('times new roman', 20, 'bold'))
    register_username_label.grid(row=1, column=0, padx=30, pady=15, sticky='W')
    register_username_entry = tk.Entry(screen, font=('roman', 15, 'bold'), width=24)
    register_username_entry.grid(row=1, column=1, padx=10, pady=15)
    #password entry
    register_password_label = tk.Label(screen, text='Password', font=('times new roman', 20, 'bold'))
    register_password_label.grid(row=2, column=0, padx=30, pady=15, sticky='W')
    register_password_entry = tk.Entry(screen, font=('roman', 15, 'bold'), width=24)
    register_password_entry.grid(row=2, column=1, padx=10, pady=15)
    #email entry
    email_label = tk.Label(screen, text='Email', font=('times new roman', 20, 'bold'))
    email_label.grid(row=3, column=0, padx=30, pady=15, sticky='W')
    email_entry = tk.Entry(screen, font=('roman', 15, 'bold'), width=24)
    email_entry.grid(row=3, column=1, padx=10, pady=15)
    #add user into db
    user_button = ttk.Button(screen, text='Register', command=lambda :register_user(register_username_entry.get(), register_password_entry.get()))
    user_button.grid(row=4, columnspan=2, pady=15)


def login():
    if username_entry.get() == '' or password_entry.get() == '':
        messagebox.showerror('Error','Fields cannot be empty')
    else:
        connection = connect_db()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT user_id, password_hash, is_admin FROM users WHERE username=%s"
                cursor.execute(sql, (username_entry.get()))
                result = cursor.fetchone()
                if result:
                    stored_password_hash = result[1]
                    # 驗證密碼
                    if bcrypt.checkpw(password_entry.get().encode('utf-8'), stored_password_hash.encode('utf-8')):
                        is_admin = result[2]
                        messagebox.showinfo('Success','Login successful!')
                        globals.current_user_id = result[0]
                        if is_admin:
                            window.destroy()
                            import admin
                        else:
                            window.destroy()
                            open_movie_window()
                    else:
                        messagebox.showerror('Error','Invalid username or password.')
                else:
                    messagebox.showerror('Error','Invalid username or password.')
        except pymysql.MySQLError as e:
            print(f"Error: {e}")
        finally:
            connection.close()

def open_movie_window():
    import movie

#GUI Part

#create a window
window = tk.Tk()
window.title('Longin System Of Student Management System')
window.geometry('1280x700+200+200')

#set no resizable
window.resizable(False,False)

#window background
background_image = ImageTk.PhotoImage(file='picture/bg.jpg')
bgLabel = tk.Label(window,image=background_image)
bgLabel.place(x=0,y=0)

#建立frame
login_frame = tk.Frame(window, bg='gray92')
login_frame.place(x=400,y=150)

#logo image
logo_image = tk.PhotoImage(file='picture/logo.png')
logo_label = tk.Label(login_frame,image=logo_image,bg='gray92')
logo_label.grid(row=0,column=0,columnspan=2, pady=10)

#username
username_image = tk.PhotoImage(file='picture/user.png')
username_label = tk.Label(login_frame,image=username_image,text='Username',compound='left',
                         font=('times new roman',20,'bold'), bg='gray92')
username_label.grid(row=1,column=0, pady=10, padx=10)
username_entry = tk.Entry(login_frame,font=('times new roman',16,'bold'), bd=3, fg='royalblue')
username_entry.grid(row=1,column=1, pady=10, padx=10)

#password
password_image = tk.PhotoImage(file='picture/password.png')
password_label = tk.Label(login_frame,image=password_image,text='Password',compound='left',
                         font=('times new roman',20,'bold'), bg='gray92')
password_label.grid(row=2,column=0, pady=10, padx=10)
password_entry = tk.Entry(login_frame,font=('times new roman',16,'bold'), bd=3, fg='royalblue')
password_entry.grid(row=2,column=1, pady=10, padx=10)

style = ttk.Style()
style.configure("My.TButton", padding=(0, 10))  # 上下內邊距設置為 10 像素
#login button
login_button = ttk.Button(login_frame, text='Login',width=20,
                        cursor='hand2',command=login, style="My.TButton")
login_button.grid(row=3,column=0,pady=10, sticky='e', padx=50)

#register button
register_button = ttk.Button(login_frame, text='Register', width=20,
                             cursor='hand2', style="My.TButton", command=register)
register_button.grid(row=3,column=1,pady=10, sticky='w')

window.mainloop()