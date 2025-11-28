import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Manager")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Data file to store tasks
        self.data_file = "tasks.json"
        self.tasks = self.load_tasks()
        
        # Create GUI elements
        self.create_widgets()
        self.refresh_task_list()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="To-Do List Manager", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 15))
        
        # Task entry section
        ttk.Label(main_frame, text="Task:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.task_entry = ttk.Entry(main_frame, width=40)
        self.task_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        self.task_entry.bind("<Return>", lambda event: self.add_task())
        
        # Priority selection
        ttk.Label(main_frame, text="Priority:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.priority_var = tk.StringVar(value="Medium")
        priority_combo = ttk.Combobox(main_frame, textvariable=self.priority_var, 
                                     values=["Low", "Medium", "High"], state="readonly")
        priority_combo.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        buttons_frame.columnconfigure(0, weight=1)
        buttons_frame.columnconfigure(1, weight=1)
        buttons_frame.columnconfigure(2, weight=1)
        buttons_frame.columnconfigure(3, weight=1)
        
        # Action buttons
        add_button = ttk.Button(buttons_frame, text="Add Task", command=self.add_task)
        add_button.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        update_button = ttk.Button(buttons_frame, text="Update Task", command=self.update_task)
        update_button.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        delete_button = ttk.Button(buttons_frame, text="Delete Task", command=self.delete_task)
        delete_button.grid(row=0, column=2, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        clear_button = ttk.Button(buttons_frame, text="Clear Completed", command=self.clear_completed)
        clear_button.grid(row=0, column=3, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        # Task list frame
        list_frame = ttk.LabelFrame(main_frame, text="Tasks", padding="5")
        list_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Task list with scrollbar
        self.task_listbox = tk.Listbox(list_frame, height=15, selectmode=tk.SINGLE)
        self.task_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.task_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.task_listbox.configure(yscrollcommand=scrollbar.set)
        
        # Bind double-click to mark task as complete/incomplete
        self.task_listbox.bind("<Double-Button-1>", self.toggle_task_status)
        
        # Status bar
        self.status_var = tk.StringVar(value=f"Total tasks: {len(self.tasks)}")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(5, 0))
    
    def load_tasks(self):
        """Load tasks from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []
    
    def save_tasks(self):
        """Save tasks to JSON file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.tasks, f, indent=2)
        except IOError:
            messagebox.showerror("Error", "Could not save tasks to file.")
    
    def refresh_task_list(self):
        """Refresh the task list display"""
        self.task_listbox.delete(0, tk.END)
        
        for i, task in enumerate(self.tasks):
            status = "✓" if task.get("completed", False) else "○"
            priority = task.get("priority", "Medium")
            task_text = f"{status} [{priority}] {task['task']}"
            
            # Add creation date if available
            if "created" in task:
                task_text += f" (Created: {task['created']})"
            
            self.task_listbox.insert(tk.END, task_text)
            
            # Color code based on priority and completion status
            if task.get("completed", False):
                self.task_listbox.itemconfig(i, {'fg': 'gray'})
            elif priority == "High":
                self.task_listbox.itemconfig(i, {'fg': 'red'})
            elif priority == "Medium":
                self.task_listbox.itemconfig(i, {'fg': 'orange'})
            else:  # Low priority
                self.task_listbox.itemconfig(i, {'fg': 'green'})
        
        # Update status bar
        total_tasks = len(self.tasks)
        completed_tasks = len([t for t in self.tasks if t.get("completed", False)])
        self.status_var.set(f"Total tasks: {total_tasks} | Completed: {completed_tasks} | Pending: {total_tasks - completed_tasks}")
    
    def add_task(self):
        """Add a new task to the list"""
        task_text = self.task_entry.get().strip()
        if not task_text:
            messagebox.showwarning("Warning", "Please enter a task.")
            return
        
        # Create task dictionary
        task = {
            "task": task_text,
            "priority": self.priority_var.get(),
            "completed": False,
            "created": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        
        self.tasks.append(task)
        self.save_tasks()
        self.refresh_task_list()
        
        # Clear the entry field
        self.task_entry.delete(0, tk.END)
        
        messagebox.showinfo("Success", "Task added successfully!")
    
    def update_task(self):
        """Update the selected task"""
        selected_index = self.task_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Warning", "Please select a task to update.")
            return
        
        index = selected_index[0]
        task_text = self.task_entry.get().strip()
        if not task_text:
            messagebox.showwarning("Warning", "Please enter a task.")
            return
        
        # Update the task
        self.tasks[index]["task"] = task_text
        self.tasks[index]["priority"] = self.priority_var.get()
        self.tasks[index]["updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        self.save_tasks()
        self.refresh_task_list()
        
        # Clear the entry field
        self.task_entry.delete(0, tk.END)
        
        messagebox.showinfo("Success", "Task updated successfully!")
    
    def delete_task(self):
        """Delete the selected task"""
        selected_index = self.task_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Warning", "Please select a task to delete.")
            return
        
        index = selected_index[0]
        task_text = self.tasks[index]["task"]
        
        if messagebox.askyesno("Confirm", f"Are you sure you want to delete '{task_text}'?"):
            del self.tasks[index]
            self.save_tasks()
            self.refresh_task_list()
            messagebox.showinfo("Success", "Task deleted successfully!")
    
    def toggle_task_status(self, event):
        """Toggle task completion status on double-click"""
        selected_index = self.task_listbox.curselection()
        if not selected_index:
            return
        
        index = selected_index[0]
        self.tasks[index]["completed"] = not self.tasks[index].get("completed", False)
        
        # Add completion date if task is being marked as complete
        if self.tasks[index]["completed"]:
            self.tasks[index]["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        self.save_tasks()
        self.refresh_task_list()
    
    def clear_completed(self):
        """Remove all completed tasks"""
        completed_count = len([t for t in self.tasks if t.get("completed", False)])
        
        if completed_count == 0:
            messagebox.showinfo("Info", "No completed tasks to clear.")
            return
        
        if messagebox.askyesno("Confirm", f"Are you sure you want to clear {completed_count} completed task(s)?"):
            self.tasks = [t for t in self.tasks if not t.get("completed", False)]
            self.save_tasks()
            self.refresh_task_list()
            messagebox.showinfo("Success", "Completed tasks cleared!")

def main():
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()