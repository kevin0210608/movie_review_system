import tkinter as tk
from turtle import tilt
import ttkthemes
from tkinter import messagebox, ttk
import time
import pymysql, bcrypt
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

#functional part

def toplevel_data(title,button_text,command):
    global title_entry, description_entry, release_year_entry, director_entry, genre_entry, username_entry, email_entry, password_entry, screen, listdata
    screen = tk.Toplevel()
    screen.title(title)
    screen.resizable(False,False)
    screen.grab_set()
    if dropdown_var.get() == 'Movies':
        #title entry
        title_label = tk.Label(screen, text='Title', font=('times new roman', 20, 'bold'))
        title_label.grid(row=0, column=0, padx=30, pady=15, sticky='W')
        title_entry = tk.Entry(screen, font=('roman', 15, 'bold'), width=24)
        title_entry.grid(row=0, column=1, padx=10, pady=15)
        #description entry
        description_label = tk.Label(screen, text='Description', font=('times new roman', 20, 'bold'))
        description_label.grid(row=2, column=0, padx=30, pady=15, sticky='W')
        description_entry = tk.Entry(screen, font=('roman', 15, 'bold'), width=24)
        description_entry.grid(row=2, column=1, padx=10, pady=15)
        #release year entry
        release_year_label = tk.Label(screen, text='Release_year', font=('times new roman', 20, 'bold'))
        release_year_label.grid(row=3, column=0, padx=30, pady=15, sticky='W')
        release_year_entry = tk.Entry(screen, font=('roman', 15, 'bold'), width=24)
        release_year_entry.grid(row=3, column=1, padx=10, pady=15)
        #director entry
        director_label = tk.Label(screen, text='Director', font=('times new roman', 20, 'bold'))
        director_label.grid(row=4, column=0, padx=30, pady=15, sticky='W')
        director_entry = tk.Entry(screen, font=('roman', 15, 'bold'), width=24)
        director_entry.grid(row=4, column=1, padx=10, pady=15)
        #genre entry
        genre_label = tk.Label(screen, text='Genre', font=('times new roman', 20, 'bold'))
        genre_label.grid(row=5, column=0, padx=30, pady=15, sticky='W')
        genre_entry = tk.Entry(screen, font=('roman', 15, 'bold'), width=24)
        genre_entry.grid(row=5, column=1, padx=10, pady=15)
    elif dropdown_var.get() == 'Users':
        #username entry
        username_label = tk.Label(screen, text='Username', font=('times new roman', 20, 'bold'))
        username_label.grid(row=0, column=0, padx=30, pady=15, sticky='W')
        username_entry = tk.Entry(screen, font=('roman', 15, 'bold'), width=24)
        username_entry.grid(row=0, column=1, padx=10, pady=15)
        #email entry
        email_label = tk.Label(screen, text='Email', font=('times new roman', 20, 'bold'))
        email_label.grid(row=1, column=0, padx=30, pady=15, sticky='W')
        email_entry = tk.Entry(screen, font=('roman', 15, 'bold'), width=24)
        email_entry.grid(row=1, column=1, padx=10, pady=15)
        #password entry
        password_label = tk.Label(screen, text='Password', font=('times new roman', 20, 'bold'))
        password_label.grid(row=2, column=0, padx=30, pady=15, sticky='W')
        password_entry = tk.Entry(screen, font=('roman', 15, 'bold'), width=24)
        password_entry.grid(row=2, column=1, padx=10, pady=15)
        password_entry.config(state='normal')
    #button
    top_button = ttk.Button(screen, text=button_text, command=command)
    top_button.grid(row=7, columnspan=2, pady=15)

    if title in ['Update Users', 'Update Movies']:
        indexing = tree.focus()
        if indexing == '':
            screen.destroy()
            messagebox.showerror('Error', 'Please update after choosing a data')
            return
        content = tree.item(indexing)
        listdata = content['values']
        if dropdown_var.get() == 'Movies':
            title_entry.insert(0, listdata[1])
            description_entry.insert(0,listdata[2])
            release_year_entry.insert(0, listdata[3])
            director_entry.insert(0,listdata[4])
            genre_entry.insert(0, listdata[5])
        else:
            password_entry.config(state='disabled')
            username_entry.insert(0,listdata[1])
            email_entry.insert(0,listdata[2])
    if title in ['Search Users', 'Search Movies']:
        password_entry.config(state='disabled')

def fetch_data(table_name):
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            sql = f"SELECT * FROM {table_name}"
            cursor.execute(sql)
            data = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            return data, columns
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
        return [], []
    finally:
        connection.close()

def on_select(event):
    selected_option = dropdown_var.get()
    tree.pack_forget()
    if selected_option == "Movies":
        load_table("Movies")
    elif selected_option == "Users":
        load_table("Users")

def load_table(table_name):
    data, columns = fetch_data(table_name)

    for col in tree.get_children():
        tree.delete(col)
    tree["columns"] = columns
    tree.config(show='headings')

    # setting scroll bar to treeview
    tree.configure(xscrollcommand=scroll_bar_X.set, yscrollcommand=scroll_bar_Y.set)
    scroll_bar_X.pack(side='bottom', fill='x')
    scroll_bar_Y.pack(side='right', fill='y')
    tree.pack(fill='both',expand=1)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor='center')

    for row in data:
        tree.insert("", tk.END, values=row)

#admin add data into database
def add_data():
    if dropdown_var.get() == "Movies":
        if title_entry.get() == '' or description_entry.get() == '' or release_year_entry.get() == '' or\
        director_entry.get() == '' or genre_entry.get() == '':
            messagebox.showerror('Error', 'All feilds are riquired', parent = screen)
            return
    elif dropdown_var.get() == "Users":
        password_entry.config(state='normal')
        if username_entry.get() == '' or email_entry.get() == '' or password_entry.get() == '':
            messagebox.showerror('Error', 'All feilds are riquired', parent = screen)
            return
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            if dropdown_var.get() == 'Movies':
                sql = 'INSERT INTO Movies (title, description, release_year, director, genre) VALUES (%s,%s,%s,%s,%s)'
                cursor.execute(sql, (title_entry.get(), description_entry.get(), release_year_entry.get(), director_entry.get(), genre_entry.get()))
            else:
                # 將密碼進行雜湊處理
                password_hash = bcrypt.hashpw(password_entry.get().encode('utf-8'), bcrypt.gensalt())
                sql = "INSERT INTO Users (username, email, password_hash, is_admin) VALUES (%s, %s, %s, False);"
                cursor.execute(sql, (username_entry.get(), email_entry.get(), password_hash))
            connection.commit()
            messagebox.showinfo('Successfully', dropdown_var.get() + ' data insert successfully.')
            screen.destroy()
    except pymysql.MySQLError as e:
        messagebox.showerror('Error', f"Error: {e}")
    finally:
        connection.close()

    tree.pack_forget()
    load_table(dropdown_var.get())

#admin update data
def update_data():
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            if dropdown_var.get() == 'Movies':
                sql = 'UPDATE Movies SET title = %s, description = %s, release_year = %s, director = %s, genre = %s where movie_id = %s'
                cursor.execute(sql, (title_entry.get(), description_entry.get(), release_year_entry.get(), director_entry.get(), genre_entry.get(), listdata[0]))
            else:
                sql = "UPDATE Users SET username = %s, email = %s where user_id = %s"
                cursor.execute(sql, (username_entry.get(), email_entry.get(), listdata[0]))
            connection.commit()
            messagebox.showinfo('Successfully', dropdown_var.get() + ' data update successfully.')
            screen.destroy()
    except pymysql.MySQLError as e:
        messagebox.showerror('Error', f"Error: {e}")
    finally:
        connection.close()

    tree.pack_forget()
    load_table(dropdown_var.get())

#delete student
def delete_data():
    indexing = tree.focus()
    if indexing == '':
        messagebox.showerror('Error', 'Please delete after choosing a data')
        return
    content = tree.item(indexing)
    content_id = content['values'][0]
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            id_name = 'user_id'
            if dropdown_var.get() == 'Movies':
                id_name = 'movie_id'
            sql = 'DELETE FROM '+ dropdown_var.get() + ' where ' + id_name + ' = %s'
            cursor.execute(sql, content_id)
            connection.commit()
            messagebox.showinfo('Deleted',f'{content["values"][1]} is deleted successfully')
    except pymysql.MySQLError as e:
        messagebox.showerror('Error', f"Error: {e}")
    finally:
        connection.close()

    tree.pack_forget()
    load_table(dropdown_var.get())

#search student
def search_data():
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            if dropdown_var.get() == 'Movies':
                sql = 'SELECT * FROM Movies where title = %s or description = %s or release_year = %s or director = %s\
                        or genre = %s'
                cursor.execute(sql, (title_entry.get(), description_entry.get(), release_year_entry.get(), director_entry.get(), genre_entry.get()))
            else:
                sql = 'SELECT * FROM Users where username = %s or email = %s'
                cursor.execute(sql, (username_entry.get(), email_entry.get()))
            tree.delete(*tree.get_children())
            fetched_data = cursor.fetchall()
            for data in fetched_data:
                tree.insert('', tk.END, values=data)
    except pymysql.MySQLError as e:
        messagebox.showerror('Error', f"Error: {e}")
    finally:
        connection.close()

#exit
def exit_admin():
    result = messagebox.askyesno('Confirm', 'Do you want to exit?')
    if result:
        root.destroy()
        import login

#GUI Part
root = ttkthemes.ThemedTk()
root.get_themes()
root.set_theme('radiance')
#set title and window size
root.title('Admin Page')
root.geometry('1174x680+200+200')
#set no resizable
root.resizable(False,False)


#left frame
left_frame = tk.Frame(root)
left_frame.place(x=50, y=80, width=300, height=600)

# drop-down menu setting
dropdown_var = tk.StringVar(value="Movies")
dropdown_menu = ttk.Combobox(left_frame, textvariable=dropdown_var)
dropdown_menu['values'] = ("Movies", "Users")
dropdown_menu.grid(row=0, column=0, padx=10, pady=10)
dropdown_menu.bind("<<ComboboxSelected>>", on_select)

#create button
add_button = ttk.Button(left_frame, text='Add', width=25, command=lambda :toplevel_data('Add Movie', 'Add Movie', add_data) if dropdown_var.get() == 'Movies' else toplevel_data('Add Users','Add Users',add_data))
add_button.grid(row=1, column=0, pady=20)

update_button = ttk.Button(left_frame, text='Update', width=25, command=lambda :toplevel_data('Update Movie', 'Update Movie', update_data) if dropdown_var.get() == 'Movies' else toplevel_data('Update Users','Update Users',update_data))
update_button.grid(row=2, column=0, pady=20)

delete_button = ttk.Button(left_frame, text='Delete', width=25, command=delete_data)
delete_button.grid(row=3, column=0, pady=20)

search_button = ttk.Button(left_frame, text='Search', width=25, command=lambda :toplevel_data('Search Movie', 'Search Movie', search_data) if dropdown_var.get() == 'Movies' else toplevel_data('Search Users','Search Users', search_data))
search_button.grid(row=4, column=0, pady=20)

exit_button = ttk.Button(left_frame, text='Exit', width=25, command=exit_admin)
exit_button.grid(row=5, column=0, pady=20)

#right frame
right_frame = tk.Frame(root)
right_frame.place(x=350, y=80, width=820, height=600)

tree = ttk.Treeview(right_frame)
#scrollbar
scroll_bar_X = tk.Scrollbar(right_frame, orient='horizontal', command=tree.xview)
scroll_bar_Y = tk.Scrollbar(right_frame, orient='vertical', command=tree.yview)
load_table('Movies')
# 主循環
root.mainloop()