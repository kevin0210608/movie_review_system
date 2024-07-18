import tkinter as tk
import ttkthemes
from tkinter import messagebox,ttk
import time
import pymysql
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

#Functional Part
#display current time
def clock():
    date = time.strftime('%Y/%m/%d')
    currenttime = time.strftime('%H:%m:%S')
    datetime_label.config(text=f'    Date: {date}\nTime: {currenttime}')
    datetime_label.after(1000, clock)

#slider for title
count = 0
text = ''

def slider():
    global count, text
    if count == len(s):
        count = 0
        text = ''
    text += s[count]
    count += 1
    slider_label.config(text=text)
    slider_label.after(300, slider)

def toplevel_data():
    def search_data():
        connection = connect_db()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT movie_id, title, description,release_year,director,genre FROM Movies where title = %s or description = %s\
                        or release_year = %s or director = %s or genre = %s"
                cursor.execute(sql, (title_entry.get(),description_entry.get(),release_year_entry.get(),director_entry.get(),genre_entry.get()))
                movie_table.delete(*movie_table.get_children())
                fetched_data = cursor.fetchall()
                for data in fetched_data:
                    movie_table.insert('', tk.END, values=data)
        except pymysql.MySQLError as e:
            print(f"Error: {e}")
        finally:
            connection.close()

    screen = tk.Toplevel()
    screen.title('Search Movie')
    screen.resizable(False,False)
    screen.grab_set()
    #title entry
    title_label = tk.Label(screen, text='Title', font=('times new roman', 20, 'bold'))
    title_label.grid(row=1, column=0, padx=30, pady=15, sticky='W')
    title_entry = tk.Entry(screen, font=('roman', 15, 'bold'), width=24)
    title_entry.grid(row=1, column=1, padx=10, pady=15)
    #description entry
    description_label = tk.Label(screen, text='Description', font=('times new roman', 20, 'bold'))
    description_label.grid(row=2, column=0, padx=30, pady=15, sticky='W')
    description_entry = tk.Entry(screen, font=('roman', 15, 'bold'), width=24)
    description_entry.grid(row=2, column=1, padx=10, pady=15)
    #release year entry
    release_year_label = tk.Label(screen, text='Release Year', font=('times new roman', 20, 'bold'))
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
    #search movie button
    search_button = ttk.Button(screen, text='Search', command=search_data)
    search_button.grid(row=7, columnspan=2, pady=15)

def get_movie():
    indexing = movie_table.focus()
    if indexing == '':
        messagebox.showerror('Error', 'Please choosing a data')
        return
    content = movie_table.item(indexing)
    movie_id = content['values'][0]
    movie_title = content['values'][1]
    return movie_id, movie_title

def show_movies():
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT movie_id, title, description,release_year,director,genre FROM Movies"
            cursor.execute(sql)
            movie_table.delete(*movie_table.get_children())
            fetched_data = cursor.fetchall()
            for data in fetched_data:
                movie_table.insert('', tk.END, values=data)
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
    finally:
        connection.close()

def rating_movie():
    #save current rating
    def save_rating():
        connection = connect_db()
        try:
            with connection.cursor() as cursor:
                sql = "REPLACE INTO Ratings (user_id, movie_id, rating) VALUES (%s, %s, %s)"
                cursor.execute(sql, (globals.current_user_id, movie_id, rating_var.get()))
                connection.commit()
                messagebox.showinfo('Success', 'Rating saved successfully')
                rate_window.destroy()
        except pymysql.MySQLError as e:
            print(f"Error: {e}")
        finally:
            connection.close()

    #get previous rating if no set default value 1
    def get_user_rating():
        connection = connect_db()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT rating FROM Ratings WHERE user_id = %s AND movie_id = %s"
                cursor.execute(sql, (globals.current_user_id, movie_id))
                result = cursor.fetchone()
                if result:
                    return result[0]
                else:
                    return 1  # default 1
        except pymysql.MySQLError as e:
            print(f"Error: {e}")
            return 1
        finally:
            connection.close()

    movie_id, movie_title = get_movie()

    #rate window GUI
    rate_window = tk.Toplevel(root)
    rate_window.title(f"Rate {movie_title}")
    rate_window.geometry('400x200+300+300')
    #set no resizable
    rate_window.resizable(False,False)

    #create a rating scale(1-5)
    tk.Label(rate_window, text=f"Rate {movie_title}").pack(pady=10)

    current_rating = get_user_rating()
    rating_var = tk.IntVar(value=current_rating)

    rating_scale = tk.Scale(rate_window, from_=1, to=5, orient=tk.HORIZONTAL, variable=rating_var)
    rating_scale.pack(pady=10)

    save_button = tk.Button(rate_window, text="Save Rating", command=save_rating)
    save_button.pack(pady=10)

def review_movie():
    def save_comment():
        connection = connect_db()
        try:
            with connection.cursor() as cursor:
                sql = "REPLACE INTO Reviews (user_id, movie_id, review_text) VALUES (%s, %s, %s)"
                cursor.execute(sql, (globals.current_user_id, movie_id, comment_text.get("1.0", tk.END).strip()))
                connection.commit()
                messagebox.showinfo('Success', 'Comment saved successfully')
                comment_window.destroy()
        except pymysql.MySQLError as e:
            messagebox.showerror('Error', f"Error: {e}")
        finally:
            connection.close()

    def get_user_comment():
        connection = connect_db()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT review_text FROM Reviews WHERE user_id = %s AND movie_id = %s"
                cursor.execute(sql, (globals.current_user_id, movie_id))
                result = cursor.fetchone()
                if result:
                    return result[0]
                else:
                    return ""
        except pymysql.MySQLError as e:
            messagebox.showerror('Error', f"Error: {e}")
            return ""
        finally:
            connection.close()

    movie_id, movie_title = get_movie()

    #review window GUI
    comment_window = tk.Toplevel(root)
    comment_window.title(f"Comment on {movie_title}")
    comment_window.geometry('400x350+300+300')
    #set no resizable
    comment_window.resizable(False,False)
    tk.Label(comment_window, text=f"Comment on {movie_title}").pack(pady=10)
    current_comment = get_user_comment()
    comment_text = tk.Text(comment_window, width=50, height=16)
    comment_text.pack(pady=10)
    comment_text.insert(tk.END, current_comment)
    #save button
    save_button = ttk.Button(comment_window, text="Save Comment", command=save_comment)
    save_button.pack(pady=10)

def show_review():
    def fetch_reviews():
        connection = connect_db()
        try:
            with connection.cursor() as cursor:
                # search comment and rating
                sql = """
                SELECT Users.username, Reviews.review_text
                FROM Users
                JOIN Reviews ON Users.user_id = Reviews.user_id
                WHERE Reviews.movie_id = %s
                """
                cursor.execute(sql, (movie_id))
                fetched_reviews = cursor.fetchall()

                reviews_tree.delete(*reviews_tree.get_children())
                for data in fetched_reviews:
                    reviews_tree.insert('', tk.END, values=data)

                #search average rating
                sql = """
                SELECT AVG(Ratings.rating)
                FROM Ratings
                WHERE Ratings.movie_id = %s
                """
                cursor.execute(sql, (movie_id,))
                avg_rating = cursor.fetchone()[0]

                if avg_rating is not None:
                    average_rating_label.config(text=f"Average Rating: {avg_rating:.2f}")
                else:
                    average_rating_label.config(text="Average Rating: N/A")

        except pymysql.MySQLError as e:
            messagebox.showerror('Error', f"Error: {e}")
        finally:
            connection.close()

    movie_id, movie_title = get_movie()
    #Reviews GUI
    reviews_window = tk.Toplevel(root)
    reviews_window.title(f"Reviews for {movie_title}")
    reviews_window.geometry('600x400+300+300')
    #set no resizable
    reviews_window.resizable(False,False)
    tk.Label(reviews_window, text=f"Reviews for {movie_title}").pack(pady=10)

    reviews_frame = tk.Frame(reviews_window)
    reviews_frame.pack(pady=10)

    reviews_tree = ttk.Treeview(reviews_frame, columns=("username", "comment"), show="headings")
    reviews_tree.heading("username", text="Username")
    reviews_tree.heading("comment", text="Comment")

    reviews_tree.column("username", width=100)
    reviews_tree.column("comment", width=400)

    reviews_tree.pack()

    average_rating_label = tk.Label(reviews_window, text="Average Rating: N/A")
    average_rating_label.pack(pady=10)
    fetch_reviews()

def iexit():
    result = messagebox.askyesno('Confirm', 'Do yo want to exit?')
    if result:
        root.destroy()
        import login

#GUI Part
root = ttkthemes.ThemedTk()
root.get_themes()
root.set_theme('radiance')
#set title and window size
root.title('Movie Review System')
root.geometry('1174x680+200+200')
#set no resizable
root.resizable(False,False)
root.after(0,show_movies)

#datetime
datetime_label = tk.Label(root, font=('times new roman', 18, 'bold'))
datetime_label.place(x=5, y=5)
clock()

#slider
s='Movie Review System'
slider_label = tk.Label(root, font=('arial', 28, 'italic bold'), width=30)
slider_label.place(x=250, y=0)
slider()

#left frame
left_frame = tk.Frame(root)
left_frame.place(x=50, y=80, width=300, height=600)
#logo image
logo_image = tk.PhotoImage(file='picture/movie_icon.png')
logo_label = tk.Label(left_frame, image=logo_image)
logo_label.image = logo_image  # 保持引用
logo_label.grid(row=0, column=0)
#all button
search_movie_button = ttk.Button(left_frame, text='Search Movie', width=25, command=toplevel_data)
search_movie_button.grid(row=1, column=0, pady=20)

show_movies_button = ttk.Button(left_frame, text='Show Movies', width=25, command=show_movies)
show_movies_button.grid(row=2, column=0, pady=20)

rating_movie_button = ttk.Button(left_frame, text='Rating Movie', width=25, command=rating_movie)
rating_movie_button.grid(row=3, column=0, pady=20)

review_movie_button = ttk.Button(left_frame, text='Review Movie', width=25, command=review_movie)
review_movie_button.grid(row=4, column=0, pady=20)

show_review_button = ttk.Button(left_frame, text='Show Review', width=25, command=show_review)
show_review_button.grid(row=5, column=0, pady=20)

exit_button = ttk.Button(left_frame, text='Exit', width=25, command=iexit)
exit_button.grid(row=6, column=0, pady=20)

#right frame
right_frame = tk.Frame(root)
right_frame.place(x=350, y=80, width=820, height=600)
#scrollbar
scroll_bar_X = tk.Scrollbar(right_frame, orient='horizontal')
scroll_bar_Y = tk.Scrollbar(right_frame, orient='vertical')
#table column
movie_table = ttk.Treeview(right_frame, columns=('Id', 'Title', 'Description','Release Year', 'Director', 'Genre'),
                            xscrollcommand=scroll_bar_X.set, yscrollcommand=scroll_bar_Y.set)
scroll_bar_X.config(command=movie_table.xview)
scroll_bar_Y.config(command=movie_table.yview)
scroll_bar_X.pack(side='bottom', fill='x')
scroll_bar_Y.pack(side='right', fill='y')
movie_table.pack(fill='both',expand=1)
#put column name
movie_table.heading('Id', text='Id')
movie_table.heading('Title', text='Title')
movie_table.heading('Description', text='Description')
movie_table.heading('Release Year', text='Release Year')
movie_table.heading('Director', text='Director')
movie_table.heading('Genre', text='Genre')
movie_table.config(show='headings')
#setting table attribute name position
movie_table.column('Id', width=100, anchor='center')
movie_table.column('Title', width=250, anchor='center')
movie_table.column('Description', width=300, anchor='center')
movie_table.column('Release Year', width=100, anchor='center')
movie_table.column('Director', width=200, anchor='center')
movie_table.column('Genre', width=200, anchor='center')

# 主循環
root.mainloop()