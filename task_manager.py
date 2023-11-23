"""importing libraries"""
import os
import datetime

"""Login Section"""
username = ""  # Define the username variable outside of the function
def load_user_info(file_name):# Define the function
    user_info = [] # Create an empty list to store the user info
    with open(os.path.join(os.path.dirname(__file__), file_name), "r") as open_file: # Open the file
        for line in open_file: # Loop through each line in the file
            username, password = line.strip().split(", ") # Split the line into username and password removing comma and spaces
            user_info.append((username, password)) # Append the username and password to the user_info list
    return user_info # Return the user_info list

def login(): # Define the function
    user_info = load_user_info('user.txt') # Load the user info from the file

    while True: # Loop until the user enters a valid username
        username = input("Please enter your username: ").lower() # Ask the user to enter a username and convert it to lower case

        valid_username = False # Define a flag variable to check if the username is valid
        for stored_username, _ in user_info: # Loop through the user info
            if username == stored_username.lower(): # Check if the username is valid
                valid_username = True # Set the flag to True
                break # Break out of the loop

        if valid_username: # Check if the username is valid
            password = input("Please enter your password: ") # Ask the user to enter a password
            for stored_username, stored_password in user_info: # Loop through the user info
                if username == stored_username.lower() and password == stored_password: # Check if the username and password are valid
                    print("Login successful. Welcome, {}!".format(username)) # Print a welcome message
                    return username  # Return the username
            print("Invalid password. Please try again.") # Print an error message
        else: # If the username is not valid
            print("Invalid username. Please try again.") # Print an error message

def add_task(): # Define the function
    assigned_to = input("Please enter the username of the person the task is assigned to: ").lower() # Ask the user to enter the username of the person the task is assigned to
    task = input("Please enter the title of the task: ") # Ask the user to enter the title of the task
    task_description = input("Please enter the description of the task: ") # Ask the user to enter the description of the task
    due_date = input("Please enter the due date of the task: ") # Ask the user to enter the due date of the task

    current_date = datetime.date.today().strftime("%d %b %Y") # Get the current date

    task_completed = "No" # Set the task completed status to "No"

    file_name = 'tasks.txt' # Define the file name

    with open(os.path.join(os.path.dirname(__file__), file_name), "a") as open_file: # Open the file
         open_file.write(f"\n{assigned_to}, {task}, {task_description}, {due_date}, {current_date}, {task_completed}") # Write the task to the file
    print("Your new task has been added.") # tell user task has been added

def view_all_tasks():# Define the function
        file_name = 'tasks.txt' # Define the file name
        with open(os.path.join(os.path.dirname(__file__), file_name), "r") as open_file: # Open the file
            for line in open_file: # Loop through each line in the file
                assigned_to, task, task_description, due_date, current_date, task_completed = line.strip().split(", ") # Split the line into the task details
                print(f"Assigned to: {assigned_to}\nTask: {task}\nTask Description: {task_description}\nDue Date: {due_date}\nDate Assigned: {current_date}\nTask Completed: {task_completed}\n") # Print the task details

def view_my_tasks(): # Define the function
    found_tasks = False  # Define a flag variable to check if the user has any tasks
    file_name = 'tasks.txt' # Define the file name
    with open(os.path.join(os.path.dirname(__file__), file_name), "r") as open_file: # Open the file
        for line in open_file: # Loop through each line in the file
            assigned_to, task, task_description, due_date, current_date, task_completed = line.strip().split(", ") # Split the line into the task details
            if username == assigned_to: # Check if the task is assigned to the logged-in user
                    
                found_tasks = True # Set the flag to True
                print(f"Assigned to: {assigned_to}") # Print the task details
                print(f"Task: {task}") # Print the task details
                print(f"Task Description: {task_description}") # Print the task details
                print(f"Due Date: {due_date}") # Print the task details
                print(f"Date Assigned: {current_date}") # Print the task details
                print(f"Task Completed: {task_completed}\n") # Print the task details

        if not found_tasks: # Check if the user has any tasks
            print("You have no tasks assigned to you.") # Print a message

def register_user(): # Define the function
    admin_username = "admin"  # Define the admin username
    admin_password = "admin_password"  # Define the admin password

    # Check if the logged-in user is the admin
    if username != admin_username: # Check if the logged-in user is the admin
        print("Only the admin can register new users.") # Print an error message
        return # Go back to the start of the loop

    new_username = input("Please enter a new username: ").lower() # Ask the user to enter a new username
    new_password = input("Please enter a new password: ") # Ask the user to enter a new password
    confirm_password = input("Please confirm your password: ") # Ask the user to confirm their password

    if new_password == confirm_password: # Check if the passwords match
        file_name = 'user.txt' # Define the file name
        with open(os.path.join(os.path.dirname(__file__), file_name), "a") as open_file: # Open the file
            open_file.write(f"\n{new_username}, {new_password}") # Write the new username and password to the file
        print("New user has been successfully registered.") # Print a success message
    else: # If the passwords do not match
        print("Passwords do not match. Please try again.") # Print an error message   

def statistics():# Define the function
    admin_username = "admin"  # Define the admin username
    
    if username != admin_username: # Check if the logged-in user is the admin
        print("Only the admin can view statistics.") # Print an error message
        return # Go back to the start of the loop

    user_info = load_user_info('user.txt') # Load the user info from the file
    total_users = len(user_info) # Get the total number of users

    file_name = 'tasks.txt' # Define the file name
    with open(os.path.join(os.path.dirname(__file__), file_name), "r") as open_file: # Open the file
        total_tasks = 0 # Define a variable to store the total number of tasks
        for line in open_file: # Loop through each line in the file
            total_tasks += 1 # Increment the total number of tasks
            assigned_to, task, task_description, due_date, current_date, task_completed = line.strip().split(", ") # Split the line into the task details

    print(f"Total number of tasks: {total_tasks}") # Print the total number of tasks
    print(f"Total number of users: {total_users}") # Print the total number of users

"""Main Menu"""  
if __name__ == '__main__': # Check if the file is being run directly
    username = login()  # Store the username from login

while True: # Loop until the user exits the program

    menu = input('''Select one of the following options:
a - add task
va - view all tasks
vm - view my tasks
r - register a user (admin only)
s = display statistics (admin only)
e - exit
: ''') # Ask the user to select an option

    if menu == 'a': # Check if the user selected option 'a'
        pass
        add_task() # Call the add_task function

    elif menu == 'va': # Check if the user selected option 'va'
        pass 
        view_all_tasks()
        
    elif menu == 'vm': # Check if the user selected option 'vm'
        pass
        view_my_tasks()
    
    elif menu == 'r':
        pass
        register_user()

    elif menu == 's': # Check if the user selected option 's'
        pass
        statistics()
        
    elif menu == 'e': # Check if the user selected option 'e'
        print('Goodbye!!!') # Print a goodbye message
        exit() # Exit the program

    else: # If the user entered an invalid input
        print("You have entered an invalid input. Please try again") # Print an error message