import sqlite3
""" Create a database table to store books """
def create_table():# Define the function
    db = sqlite3.connect('book_database')# Connect to the database
    cursor = db.cursor()# Get a cursor object

    cursor.execute('''
              CREATE TABLE IF NOT EXISTS book_database(
                  id INTEGER PRIMARY KEY,
                  title TEXT,
                  author TEXT,
                  qty INTEGER
              )
              ''') 
    
    Books = [
        (3001,'A Tale of Two Cities', 'Charles Dickens',30),
        (3002,"Harry Potter and the Philosopher's stone","J.K. Rowling",40),
        (3003,"The Lion, the Witch and the Wardrobe","C.S. Lewis",25),
        (3004,"The Lord of the Rings","J.R.R Tolkien",37),
        (3005,"Alice in Wonderland","Lewis Carroll",12) 
    ]

    cursor.executemany('''INSERT OR REPLACE INTO book_database(id, title, author, qty) VALUES (?, ?, ?, ?)''', Books) # Insert the books into the database

    db.commit()
    db.close() 

""" Add a new book to the database using the function defined below """
def enter_book():
    try:
        book_title = input("Please enter the title of the book: ").lower() # Ask the user to enter the book title
        book_author = input("Please enter the name and surname of the author of the book: ").lower() # Ask the user to enter the book author
        book_quantity = int(input("Please enter the quantity of this book: "))# Ask the user to enter the book quantity 
        if book_quantity <= 0:# Check if the book quantity is valid
            raise ValueError("Book quantity must be a positive integer.")# Raise an exception if the book quantity is invalid

        db = sqlite3.connect('book_database')
        cursor = db.cursor()

        try:
            cursor.execute('''INSERT INTO book_database(title, author, qty) VALUES (?, ?, ?)''', (book_title, book_author, book_quantity))# Insert the book into the database
            
            db.commit()
        
            print("The new book has been added.")

        except sqlite3.IntegrityError as e:# If the book already exists in the database
            if "UNIQUE constraint failed: book_database.title" in str(e):# Check if the book title already exists in the database
                print("Error: This book title already exists in the database.")

        except sqlite3.Error as e:# If there was any other error
            print("Error:", str(e))
    
    except ValueError as ve:# If there was an error with the user input
        print("Error:", str(ve))

    db.close()

""" Update an existing book in the database using the function defined below """
def update_book():
    try:
        book_id = int(input("Enter book ID to update: "))# ask the user to enter the book ID
        if book_id <= 0:# check if the book ID is valid
            raise ValueError("Book ID must be a positive integer.")# raise an exception if the book ID is invalid

        db = sqlite3.connect('book_database')
        cursor = db.cursor()

        cursor.execute('''SELECT * FROM book_database WHERE id=?''', (book_id,))# select the book from the database
        existing_book = cursor.fetchone()# fetch the book details

        if existing_book:# if the book exists in the database
                print("Current Book Details:")
                print(f"ID: {existing_book[0]}, Title: {existing_book[1]}, Author: {existing_book[2]}, Quantity: {existing_book[3]}")# print the book details

                update_title = input("Enter new title (press Enter to keep current): ").lower()# ask the user if they want to update the book title
                update_author = input("Enter new author (press Enter to keep current): ").lower()# ask the user if they want to update the book author
                update_quantity_str = input("Enter new quantity (press Enter to keep current): ")
            
                if update_quantity_str == '':
                    update_quantity = existing_book[3]  # Keep the current quantity
                else:
                    update_quantity = int(update_quantity_str)
                    if update_quantity <= 0:
                        raise ValueError("Book quantity must be a positive integer.")
                    
                cursor.execute('''UPDATE book_database SET title=?, author=?, qty=? WHERE id=?''',# update the book details
                            (update_title or existing_book[1], update_author or existing_book[2], update_quantity or existing_book[3], book_id))# update the book details
                db.commit()

                print("The book details were updated successfully.")

        else:
                print("Error: Book ID not found.")
    except ValueError as ve:# if there was an error with the user input
        print("Error:", str(ve))

    except sqlite3.Error as e:# if there was any other error
        print("Error:", str(e))

        db.close()

""" Delete an existing book from the database using the function below """
def delete_book():
    try:    
        book_id = int(input("Enter book ID you wish to delete: "))# ask the user to enter the book ID
        if book_id <= 0:# check if the book ID is valid
                raise ValueError("Book ID must be a positive integer.")# raise an exception if the book ID is invalid

        db = sqlite3.connect('book_database')
        cursor = db.cursor()

        cursor.execute('''SELECT * FROM book_database WHERE id=?''', (book_id,))# select the book from the database
        deleted_book = cursor.fetchone()# fetch the book details

        if deleted_book:# if the book exists in the database
            cursor.execute('''DELETE FROM book_database WHERE id=?''', (book_id,))# delete the book from the database
            db.commit()
            db.close()
                
            print(f"The following book was deleted successfully:")# print a success message
            print(f"ID: {deleted_book[0]}, Title: {deleted_book[1]}, Author: {deleted_book[2]}, Quantity: {deleted_book[3]}")# print the book details
        else:
            print(f"No book with the title '{book_id}' found.")

    except ValueError as ve:# if there was an error with the user input
        print("Error:", str(ve))

    db.close()

""" Search for books in the database using the function below """
def search_books():
    keyword = input("Enter search keyword (title or author): ")# ask the user to enter the search keyword

    db = sqlite3.connect('book_database')
    cursor = db.cursor()

    cursor.execute('''SELECT * FROM book_database WHERE title LIKE ? OR author LIKE ?''', ('%' + keyword + '%', '%' + keyword + '%'))# search for the book in the database

    books = cursor.fetchall()# fetch the book details

    if not books:# if the book doesn't exist in the database
        print("No matching books found.")
    else:
        for book in books:# if the book exists in the database
            print(book)

    db.close()

""" Display all books in the database using the function below """
def print_books():
    db = sqlite3.connect('book_database')
    cursor = db.cursor()

    cursor.execute('''SELECT * FROM book_database''')# select all the books from the database
    books = cursor.fetchall()# fetch the book details

    if not books:# if the book doesn't exist in the database
        print("No books found.")
    else:
        for book in books:# if the book exists in the database
            print(book)

    db.close()# close the database connection

"""Main Menu"""  
if __name__ == '__main__':# if the user runs the program directly
    create_table()# call the create_table function

while True:# while the program is running

    menu = input('''Select one of the following options:
1. - Enter book
2. - Update book
3. - Delete book
4. - Search books
5. - Display all books
0. = Exit
: ''') # Ask the user to select an option, the option will call the corresponding function

    if menu == '1':1
        enter_book() 

    elif menu == '2': 
        update_book()
        
    elif menu == '3': 
        delete_book()
    
    elif menu == '4':
        search_books()

    elif menu == '5': 
        print_books()
        
    elif menu == '0': 
        print('You are exiting the database, goodbye!!!')
        exit()

    else: 
        print("You have made an invalid selection. Please try again") 
