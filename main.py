import firebase_admin
from firebase_admin import credentials, db
import tkinter as tk

cred = credentials.Certificate("interactive-davetagacay-firebase-adminsdk-m4sbj-2bd3ebd5f5.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://interactive-davetagacay-default-rtdb.asia-southeast1.firebasedatabase.app/'
})
root_ref = db.reference()

def show_search_results(search_isbn):
    result_window = tk.Toplevel(window)
    result_window.title(f"Search Results for ISBN {search_isbn}")

    result_text = tk.Text(result_window, height=10, width=75)
    result_text.pack(pady=15)


    result_text.tag_configure("title", font=("Helvetica", 20, "bold"), foreground="violet")
    result_text.tag_configure("author", font=("Helvetica", 20, "bold"), foreground="green")
    result_text.tag_configure("year", font=("Helvetica", 20, "bold"), foreground="red")
    result_text.tag_configure("publisher", font=("Helvetica", 20, "bold"), foreground="blue")

    scrollbar = tk.Scrollbar(result_window, command=result_text.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    result_text.config(yscrollcommand=scrollbar.set)

    book_ref = root_ref.child(search_isbn.strip())
    try:
        book_data = book_ref.get()

        if book_data:
            result_text.insert(tk.END, f"Title: {book_data.get('title')}\n", "title")
            result_text.insert(tk.END, f"Author: {book_data.get('author')}\n", "author")
            result_text.insert(tk.END, f"Year: {book_data.get('year')}\n", "year")
            result_text.insert(tk.END, f"Publisher: {book_data.get('publisher')}\n", "publisher")
            result_text.insert(tk.END, "------------------------\n", "other")
        else:
            result_text.insert(tk.END, f"No data found for ISBN {search_isbn}\n")

    except Exception as e:
        result_text.insert(tk.END, f"Error retrieving data for ISBN {search_isbn}: {e}\n")

def show_insert_success():
    success_window = tk.Toplevel(window)
    success_window.title("Insert Successful")

    success_label = tk.Label(success_window, text="Data inserted successfully!", font=("Helvetica", 16))
    success_label.pack(pady=20)

    ok_button = tk.Button(success_window, text="OK", command=success_window.destroy)
    ok_button.pack(pady=10)


def show_insert_failure(error_message):
    duplicate_failure_window = tk.Toplevel(window)
    duplicate_failure_window.title("Duplicate ISBN")

    duplicate_failure_label = tk.Label(duplicate_failure_window, text="Duplicate ISBN. Failed to insert data", font=("Helvetica", 16))
    duplicate_failure_label.pack(pady=20)

    ok_button = tk.Button(duplicate_failure_window, text="OK", command=duplicate_failure_window.destroy)
    ok_button.pack(pady=10)

def search_books():
    search_isbns = isbn_entry.get().split(',')

    for search_isbn in search_isbns:
        show_search_results(search_isbn.strip())

def insert_data():
    isbn = isbn_entry.get().strip()


    if root_ref.child(isbn).get() is not None:
        show_insert_failure(f"Duplicate ISBN {isbn}. Failed to insert data.")
        return

    title = title_entry.get().strip()
    author = author_entry.get().strip()
    year = year_entry.get().strip()
    publisher = publisher_entry.get().strip()

    data = {
        'title': title,
        'author': author,
        'year': year,
        'publisher': publisher
    }

    try:
        root_ref.child(isbn).set(data)
        print(f"Data inserted successfully for ISBN {isbn}")
        show_insert_success()
    except Exception as e:
        print(f"Error inserting data for ISBN {isbn}: {e}")
        show_insert_failure(str(e))


window = tk.Tk()
window.title("Marlo James Ballaran")


search_label = tk.Label(window, text="Final Exam/Output for AppDev", font=("Arial", 30))
search_label.pack(pady=5)

isbn_label = tk.Label(window, text="ISBN:", font="Arial")
isbn_label.pack(pady=5)
isbn_entry = tk.Entry(window, width=50)
isbn_entry.pack(pady=5)

title_label = tk.Label(window, text="Title:", font="Arial")
title_label.pack(pady=5)
title_entry = tk.Entry(window, width=50)
title_entry.pack(pady=5)

author_label = tk.Label(window, text="Author:", font="Arial")
author_label.pack(pady=5)
author_entry = tk.Entry(window, width=50)
author_entry.pack(pady=5)

year_label = tk.Label(window, text="Year:", font="Arial")
year_label.pack(pady=5)
year_entry = tk.Entry(window, width=50)
year_entry.pack(pady=5)

publisher_label = tk.Label(window, text="Publisher:", font="Arial")
publisher_label.pack(pady=5)
publisher_entry = tk.Entry(window, width=50)
publisher_entry.pack(pady=5)

search_button = tk.Button(window, text="Search", command=search_books, bg="red", font="Arial")
search_button.pack(pady=5)

insert_button = tk.Button(window, text="Add Data", command=insert_data, bg="green", font="Arial")
insert_button.pack(pady=5)


window.mainloop()