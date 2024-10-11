import hashlib
import os

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = self.hash_password(password)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, input_password):
        return self.password == self.hash_password(input_password)


class Task:
    def __init__(self, task_id, description, status="Pending"):
        self.task_id = task_id
        self.description = description
        self.status = status

    def __str__(self):
        return f"{self.task_id}: {self.description} - {self.status}"


class TaskManager:
    credentials_file = "users.txt"
    tasks_file = "tasks.txt"

    def __init__(self):
        self.current_user = None

    def register(self):
        username = input("Enter a username: ")
        password = input("Enter a password: ")

        if self.username_exists(username):
            print("Username already exists!")
            return

        new_user = User(username, password)
        self.save_user(new_user)
        print("Registration successful!")
    
    def validate_credentials(self, username, password):
        if os.path.exists(self.credentials_file):
            with open(self.credentials_file, 'r') as f:
                for line in f:
                    stored_username, stored_password = line.strip().split(':')
                    if stored_username == username:
                        # Verify password
                        user = User(stored_username, stored_password)
                        return user.verify_password(password)
        return False

    def login(self):
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        if self.validate_credentials(username, password):
            print("Login successful!")
            self.current_user = username
            self.task_menu()
        else:
            print("Invalid username or password!")

    def username_exists(self, username):
        if os.path.exists(self.credentials_file):
            with open(self.credentials_file, 'r') as f:
                for line in f:
                    stored_username, _ = line.strip().split(':')
                    if stored_username == username:
                        return True
        return False
    
    def save_user(self, user):
        with open(self.credentials_file, 'a') as f:
            f.write(f"{user.username}:{user.password}\n")
    
    def add_task(self):
        task_description = input("Enter task description: ")
        task_id = self.get_next_task_id()
        new_task = Task(task_id, task_description)
        with open(self.tasks_file, 'a') as f:
            f.write(f"{self.current_user}:{new_task.task_id}:{new_task.description}:{new_task.status}\n") 
        print("Task added successfully.")

    def get_next_task_id(self):
        if os.path.exists(self.tasks_file):
            with open(self.tasks_file, 'r') as f:
                tasks = [line.strip() for line in f]
            task_ids = [int(task.split(':')[1]) for task in tasks if task.startswith(self.current_user)]
            return max(task_ids) + 1 if task_ids else 1
        return 1
    
    def view_tasks(self):
        tasks = self.get_user_tasks()
        if tasks:
            for task in tasks:
                print(task)
        else:
            print("No tasks found!")
            
    def get_user_tasks(self):
        tasks = []
        if os.path.exists(self.tasks_file):
            with open(self.tasks_file, 'r') as f:
                for line in f:
                    username, task_id, description, status = line.strip().split(':')
                    if username == self.current_user:
                        tasks.append(Task(task_id, description, status))
        return tasks
    
    def mark_task_completed(self):
        tasks = self.get_user_tasks()
        if tasks:
            self.display_tasks(tasks)
            task_num = int(input("Enter the task number to mark as completed: "))
            if 1 <= task_num <= len(tasks):
                tasks[task_num - 1].status = "Completed"
                self.update_tasks_file(tasks)
                print('Task marked as completed!')
            else:
                print('Invalid task number')
        else:
            print('No tasks found.')
    
    def delete_task(self):
        tasks = self.get_user_tasks()
        if tasks:
            self.display_tasks(tasks)
            task_num = int(input("Enter the task number to delete: "))
            if 1 <= task_num <= len(tasks):
                del tasks[task_num - 1]
                self.update_tasks_file(tasks)
                print("Task deleted successfully.")
            else:
                print("Invalid task number")
        else:
            print("No tasks found.")
    
    def display_tasks(self, tasks):
        for idx, task in enumerate(tasks, 1):
            print(f"{idx}. {task}")
    
    def update_tasks_file(self, tasks):
        all_tasks = []
        if os.path.exists(self.tasks_file):
            with open(self.tasks_file, 'r') as f:
                all_tasks = [line.strip() for line in f]
        
        updated_tasks = [f"{self.current_user}:{task.task_id}:{task.description}:{task.status}" for task in tasks]
        all_tasks = [line for line in all_tasks if not line.startswith(self.current_user)]
        all_tasks.extend(updated_tasks)

        with open(self.tasks_file, 'w') as f:
            for task in all_tasks:
                f.write(task + "\n")
    

    def task_menu(self):
        while True:
            print("\nTask Manager Menu:")
            print("1. Add Task")
            print("2. View Tasks")
            print("3. Mark Task as Completed")
            print("4. Delete Task")
            print("5. Logout")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.add_task()
            elif choice == "2":
                self.view_tasks()
            elif choice == "3":
                self.mark_task_completed()
            elif choice == "4":
                self.delete_task()
            elif choice == "5":
                print("Logging out...")
                self.current_user = None
                break
            else:
                print("Invalid choice! Please try again.")

    def main_menu(self):
        while True:
            print("\nWelcome to the Task Manager")
            print("1. Register")
            print("2. Login")
            print("3. Exit")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.register()
            elif choice == "2":
                self.login()
            elif choice == "3":
                print("Exiting...")
                break
            else:
                print("Invalid choice! Please try again.")


if __name__ == "__main__":
    manager = TaskManager()
    manager.main_menu()
