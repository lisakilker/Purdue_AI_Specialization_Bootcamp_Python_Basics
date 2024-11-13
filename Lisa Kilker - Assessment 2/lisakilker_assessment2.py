#Task Manager - Assessment 2

#Imports Libraries
import hashlib
import os

#File paths for storing data
#Stores username/password
USER_FILE = 'users.txt'
#Stores tasks
TASK_FILE = 'tasks.txt'

#Helper function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

#Ensures files exist and add headers if the task file is empty
def initialize_files():
    #Create USER_FILE if it doesn't exist
    open(USER_FILE, 'a').close()
    
    #Check if TASK_FILE exists and is empty, and if so, adds headers
    if not os.path.exists(TASK_FILE) or os.path.getsize(TASK_FILE) == 0:
        with open(TASK_FILE, 'w') as file:
            file.write("username,task ID,description,status\n")

#Generates a unique task ID by finding the maximum existing ID and incrementing it
def generate_task_id():
    max_id = 0
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, 'r') as file:
            #Skips the header line
            next(file)
            for line in file:
                _, task_id, _, _ = line.strip().split(',')
                max_id = max(max_id, int(task_id))
    return str(max_id + 1)

#User Authentication Functions with Validations

#Registration with validation
def register_user():
    while True:
        username = input("\nEnter a username: ").strip()
        password = input("Enter a password: ").strip()
        
        #Checks if username or password is empty
        if not username or not password:
            print("Username and password cannot be empty. Please try again.")
            continue

        #Checks if username is unique
        with open(USER_FILE, 'r') as file:
            for line in file:
                stored_username, _ = line.strip().split(',')
                if stored_username == username:
                    print("\nUsername already exists. Please try a different one.")
                    return
        
        #Hashes and stores the password in USERS.TXT file
        hashed_password = hash_password(password)
        with open(USER_FILE, 'a') as file:
            file.write(f"{username},{hashed_password}\n")
        print("\nRegistration successful! Please select an option:")
        break

#Login with validation
def login_user():
    while True:
        #Asks user for existing username
        username = input("\nEnter your username: ").strip()
        #Asks user for password
        password = input("Enter your password: ").strip()
        
        if not username or not password:
            print("\nUsername and password cannot be empty.")
            continue
        
        #Checks the validity of the username/password against the USERS.TXT file
        hashed_password = hash_password(password)
        with open(USER_FILE, 'r') as file:
            for line in file:
                stored_username, stored_password = line.strip().split(',')
                if stored_username == username and stored_password == hashed_password:
                    print("\nLogin successful!")
                    return username
        #If either username or password is invalid, prints this:
        print("\nInvalid credentials. Please try again. (Note: Username and password are CASE SENSITIVE.)")
        return None

#Task ID validation helper function
def validate_task_id(task_id, tasks):
    return any(task_id == tid for tid, _, _ in tasks)

#Task Management Functions with Task ID Validation

#Add a task with unique ID
def add_task(username):
    #Generates a new, unique task ID
    task_id = generate_task_id()
    #Asks user to enter task description and validates
    task_description = input("\nEnter task description: ").strip()
    if not task_description:
        print("\nTask description cannot be empty.")
        return
    
    #Default task status always set to "pending"
    task_status = "Pending"
    with open(TASK_FILE, 'a') as file:
        file.write(f"{username},{task_id},{task_description},{task_status}\n")
    print("\nTask added successfully!")

#View tasks
def view_tasks(username):
    tasks = []
    with open(TASK_FILE, 'r') as file:
        #Skips the header line
        next(file)
        for line in file:
            data = line.strip().split(',')
            #Ensures line has all fields
            if len(data) == 4: 
                task_user, task_id, task_description, task_status = data
                if task_user == username:
                    tasks.append((task_id, task_description, task_status))
                    print(f"\nTask ID: {task_id} | Description: {task_description} | Status: {task_status}")
            else:
                print("\nOops! Task data format is incorrect.")
    if not tasks:
        print("\nNo tasks found. Create new task.")
    return tasks

#Mark task as completed with validation
def mark_task_completed(username):
    print("\nHere are your current tasks:")
    tasks = view_tasks(username)
    if not tasks:
        print("\nNo tasks to complete.")
        return
    
    task_id = input("\nEnter the task ID to mark as completed: ").strip()
    if not validate_task_id(task_id, tasks):
        print(f"\nTask ID {task_id} does not exist. Please try again.")
        return
    
    updated_tasks = []
    with open(TASK_FILE, 'r') as file:
        #Skips the header line
        header = file.readline()
        updated_tasks.append(header)
        
        for line in file:
            task_user, tid, desc, status = line.strip().split(',')
            if task_user == username and tid == task_id:
                status = "Completed"
            updated_tasks.append(f"{task_user},{tid},{desc},{status}\n")
    
    with open(TASK_FILE, 'w') as file:
        file.writelines(updated_tasks)
    print(f"\nTask {task_id} marked as completed.")

#Deletes task with validation
def delete_task(username):
    print("\nHere are your current tasks:")
    tasks = view_tasks(username)
    if not tasks:
        print("\nNo tasks to delete.")
        return

    task_id = input("\nEnter the task ID to delete: ").strip()
    if not validate_task_id(task_id, tasks):
        print(f"\nTask ID {task_id} does not exist. Please try again.")
        return

    updated_tasks = []
    with open(TASK_FILE, 'r') as file:
        #Skips the header line
        header = file.readline()
        updated_tasks.append(header)
        
        for line in file:
            task_user, tid, desc, status = line.strip().split(',')
            if not (task_user == username and tid == task_id):
                updated_tasks.append(f"{task_user},{tid},{desc},{status}\n")

    with open(TASK_FILE, 'w') as file:
        file.writelines(updated_tasks)
    print(f"\nTask {task_id} deleted.")

#Main program loop with validation
def main():
    initialize_files()
    #Header
    print("\nWelcome to the Task Manager!")
    while True:
        #Asks the user for input
        action = input("\nSelect action: \n1: Register \n2: Login \n3: Exit \nWhich option would you like? ").strip()
        if action == '1':
            register_user()
        elif action == '2':
            username = login_user()
            if username:
                while True:
                    #Asks the user for input
                    task_action = input("\nSelect action: \n1: Add Task \n2: View Tasks \n3: Complete Task \n4: Delete Task \n5: Logout \nWhich option would you like?: ").strip()
                    if task_action == '1':
                        add_task(username)
                    elif task_action == '2':
                        view_tasks(username)
                    elif task_action == '3':
                        mark_task_completed(username)
                    elif task_action == '4':
                        delete_task(username)
                    elif task_action == '5':
                        print("\nLogging out...")
                        break
                    else:
                        print("\nInvalid option. Please try again.")
        elif action == '3':
            #Exists program
            print("\nGoodbye!")
            break
        else:
            print("\nInvalid option. Please try again.")

if __name__ == "__main__":
    main()