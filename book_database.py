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
              ''') # Create the table if it doesn't exist already
    
    Books = [
        (3001,'A Tale of Two Cities', 'Charles Dickens',30),
        (3002,"Harry Potter and the Philosopher's stone","J.K. Rowling",40),
        (3003,"The Lion, the Witch and the Wardrobe","C.S. Lewis",25),
        (3004,"The Lord of the Rings","J.R.R Tolkien",37),
        (3005,"Alice in Wonderland","Lewis Carroll",12) # add books,titles,authors and quantities
    ]

    cursor.executemany('''INSERT OR REPLACE INTO book_database(id, title, author, qty) VALUES (?, ?, ?, ?)''', Books) # Insert the books into the database

    db.commit()# Commit the changes to the database
    db.close() # Close the database connection

""" Add a new book to the database """
def enter_book():
    try:
        book_title = input("Please enter the title of the book: ").lower() # Ask the user to enter the book title
        book_author = input("Please enter the name and surname of the author of the book: ").lower() # Ask the user to enter the book author
        book_quantity = int(input("Please enter the quantity of this book: "))# Ask the user to enter the book quantity 
        if book_quantity <= 0:# Check if the book quantity is valid
            raise ValueError("Book quantity must be a positive integer.")# Raise an exception if the book quantity is invalid

        db = sqlite3.connect('book_database')# Connect to the database
        cursor = db.cursor()# Get a cursor object

        try:# Try to insert the book into the database
            cursor.execute('''INSERT INTO book_database(title, author, qty) VALUES (?, ?, ?)''', (book_title, book_author, book_quantity))# Insert the book into the database
            
            db.commit()# Commit the changes to the database
        
            print("The new book has been added.")# Print a success message

        except sqlite3.IntegrityError as e:# If the book already exists in the database
            if "UNIQUE constraint failed: book_database.title" in str(e):# Check if the book title already exists in the database
                print("Error: This book title already exists in the database.")# Print an error message

        except sqlite3.Error as e:# If there was any other error
            print("Error:", str(e))# Print the error message
    
    except ValueError as ve:# If there was an error with the user input
        print("Error:", str(ve))# Print the error message

    db.close()# Close the database connection

""" Update an existing book in the database """
def update_book():# define the function update_book
    try:# try to update the book
        book_id = int(input("Enter book ID to update: "))# ask the user to enter the book ID
        if book_id <= 0:# check if the book ID is valid
            raise ValueError("Book ID must be a positive integer.")# raise an exception if the book ID is invalid

        db = sqlite3.connect('book_database')# connect to the database
        cursor = db.cursor()# get a cursor object

        cursor.execute('''SELECT * FROM book_database WHERE id=?''', (book_id,))# select the book from the database
        existing_book = cursor.fetchone()# fetch the book details

        if existing_book:# if the book exists in the database
                print("Current Book Details:")# print the book details
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
                db.commit()# commit the changes to the database

                print("The book details were updated successfully.")# print a success message

        else:
                print("Error: Book ID not found.")# print an error message

    except ValueError as ve:# if there was an error with the user input
        print("Error:", str(ve))# print the error message

    except sqlite3.Error as e:# if there was any other error
        print("Error:", str(e))# print the error message


        db.close()# close the database connection

""" Delete an existing book from the database """
def delete_book():# define the function delete_book
    try:    
        book_id = int(input("Enter book ID you wish to delete: "))# ask the user to enter the book ID
        if book_id <= 0:# check if the book ID is valid
                raise ValueError("Book ID must be a positive integer.")# raise an exception if the book ID is invalid

        db = sqlite3.connect('book_database')# connect to the database
        cursor = db.cursor()# get a cursor object

        cursor.execute('''SELECT * FROM book_database WHERE id=?''', (book_id,))# select the book from the database
        deleted_book = cursor.fetchone()# fetch the book details

        if deleted_book:# if the book exists in the database
            cursor.execute('''DELETE FROM book_database WHERE id=?''', (book_id,))# delete the book from the database
            db.commit()# commit the changes to the database
            db.close()# close the database connection
                
            print(f"The following book was deleted successfully:")# print a success message
            print(f"ID: {deleted_book[0]}, Title: {deleted_book[1]}, Author: {deleted_book[2]}, Quantity: {deleted_book[3]}")# print the book details
        else:
            print(f"No book with the title '{book_id}' found.")# print an error message

    except ValueError as ve:# if there was an error with the user input
        print("Error:", str(ve))# print the error message

    db.close()# close the database connection

""" Search for books in the database """
def search_books():# define the function search_books
    keyword = input("Enter search keyword (title or author): ")# ask the user to enter the search keyword

    db = sqlite3.connect('book_database')# connect to the database
    cursor = db.cursor()# get a cursor object

    cursor.execute('''SELECT * FROM book_database WHERE title LIKE ? OR author LIKE ?''', ('%' + keyword + '%', '%' + keyword + '%'))# search for the book in the database

    books = cursor.fetchall()# fetch the book details

    if not books:# if the book doesn't exist in the database
        print("No matching books found.")# print an error message
    else:
        for book in books:# if the book exists in the database
            print(book)# print the book details

    db.close()# close the database connection

""" Display all books in the database """
def print_books():# define the function print_books
    db = sqlite3.connect('book_database')# connect to the database
    cursor = db.cursor()# get a cursor object

    cursor.execute('''SELECT * FROM book_database''')# select all the books from the database
    books = cursor.fetchall()# fetch the book details

    if not books:# if the book doesn't exist in the database
        print("No books found.")# print an error message
    else:
        for book in books:# if the book exists in the database
            print(book)# print the book details

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
: ''') # Ask the user to select an option

    if menu == '1':# if the user selects option 1
        enter_book() # call the enter_book function

    elif menu == '2': # if the user selects option 2
        update_book()# call the update_book function
        
    elif menu == '3': # if the user selects option 3
        delete_book()# call the delete_book function
    
    elif menu == '4':# if the user selects option 4
        search_books()# call the search_books function

    elif menu == '5': # if the user selects option 5
        print_books()
        
    elif menu == '0': # if the user selects option 0
        print('You are exiting the database, goodbye!!!') # print a goodbye message
        exit() # exit the program

    else: 
        print("You have made an invalid selection. Please try again") # print an error message