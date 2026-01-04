import os
import json
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk, messagebox
from settings import get_data_path

class TodoManager:
    def __init__(self):
        self.todos = self.load_todos()
        self._tooltip = None  # Initialize tooltip attribute
    
    def load_todos(self):
        """Load todos from the JSON file."""
        todos_file = get_data_path("todos.json")
        
        if os.path.exists(todos_file):
            try:
                with open(todos_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []
    
    def save_todos(self):
        """Save todos to the JSON file."""
        todos_file = get_data_path("todos.json")
        
        with open(todos_file, 'w') as f:
            json.dump(self.todos, f, indent=2)
    
    def create_widget(self, parent):
        """Create and return the todo manager widget."""
        # Create main frame
        frame = ttk.Frame(parent, padding=10)
        
        # Todo list frame
        self.todo_frame = ttk.Frame(frame)
        self.todo_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Scrollable container for todos
        self.canvas = tk.Canvas(self.todo_frame, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.todo_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Add todos
        self.refresh_todos()
        
        # Input frame
        input_frame = ttk.Frame(frame)
        input_frame.pack(fill=tk.X)
        
        self.todo_entry = ttk.Entry(input_frame)
        self.todo_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.todo_entry.bind("<Return>", lambda e: self.add_todo())
        
        add_button = ttk.Button(input_frame, text="+", width=3, command=self.add_todo)
        add_button.pack(side=tk.RIGHT)
        
        return frame
    
    def refresh_todos(self):
        """Refresh the todo list display."""
        # Clear existing todos
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Add todos to the layout
        for todo in self.todos:
            self.add_todo_item(todo)
    
    def add_todo_item(self, todo):
        """Add a todo item to the layout."""
        # Create frame for this todo item
        todo_frame = ttk.Frame(self.scrollable_frame)
        todo_frame.pack(fill=tk.X, pady=2)
        
        # Checkbox
        completed_var = tk.BooleanVar(value=todo.get("completed", False))
        checkbox = ttk.Checkbutton(
            todo_frame, 
            text=todo["text"],
            variable=completed_var,
            command=lambda t=todo, v=completed_var: self.toggle_todo_completed(t, v)
        )
        checkbox.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Apply strikethrough style if completed
        if todo.get("completed", False):
            checkbox.state(["selected"])
            # Tkinter doesn't support strikethrough directly, we'd need 
            # additional libraries like customtkinter for that
        
        # Reminder indicator
        if "reminder" in todo and todo["reminder"]:
            reminder_time = datetime.fromisoformat(todo["reminder"])
            now = datetime.now()
            
            # Choose color based on due state
            color = "black"
            if reminder_time < now:
                color = "red"  # Overdue
            elif reminder_time < now + timedelta(hours=24):
                color = "orange"  # Due soon
            
            reminder_label = ttk.Label(todo_frame, text="🔔", foreground=color)
            reminder_label.pack(side=tk.LEFT, padx=2)
            
            # Add tooltip
            self.create_tooltip(reminder_label, 
                              f"Reminder: {reminder_time.strftime('%Y-%m-%d %H:%M')}")
        
        # Edit button
        edit_button = ttk.Button(
            todo_frame, 
            text="✎", 
            width=3,
            command=lambda t=todo: self.edit_todo(t)
        )
        edit_button.pack(side=tk.LEFT, padx=2)
        
        # Delete button
        delete_button = ttk.Button(
            todo_frame, 
            text="×", 
            width=3,
            command=lambda t=todo: self.delete_todo(t)
        )
        delete_button.pack(side=tk.LEFT)
    
    def create_tooltip(self, widget, text):
        """Create a simple tooltip for a widget."""
        # Store tooltip window as attribute of the widget instead of self
        tooltip_window = None
        
        def enter(event):
            nonlocal tooltip_window
            x = widget.winfo_rootx() + widget.winfo_width() // 2
            y = widget.winfo_rooty() + widget.winfo_height()
            
            # Create a toplevel window
            tooltip_window = tk.Toplevel(widget)
            tooltip_window.wm_overrideredirect(True)
            tooltip_window.wm_geometry(f"+{x}+{y}")
            
            label = ttk.Label(tooltip_window, text=text, justify='left',
                            background="#ffffe0", relief='solid', borderwidth=1)
            label.pack(ipadx=1)
            
            # Store tooltip reference in widget
            widget.tooltip_window = tooltip_window
        
        def leave(event):
            nonlocal tooltip_window
            if tooltip_window:
                tooltip_window.destroy()
                tooltip_window = None
                if hasattr(widget, "tooltip_window"):
                    delattr(widget, "tooltip_window")
        
        widget.bind("<Enter>", enter)
        widget.bind("<Leave>", leave)
    
    def add_todo(self):
        """Add a new todo item."""
        text = self.todo_entry.get().strip()
        if text:
            todo = {
                "id": str(len(self.todos) + 1),  # Simple ID generation
                "text": text,
                "completed": False,
                "created": datetime.now().isoformat()
            }
            
            self.todos.append(todo)
            self.save_todos()
            
            # Add to UI
            self.add_todo_item(todo)
            
            # Clear input
            self.todo_entry.delete(0, tk.END)
    
    def edit_todo(self, todo):
        """Edit a todo item."""
        # Create dialog window
        dialog = tk.Toplevel()
        dialog.title("Edit Task")
        dialog.geometry("300x200")
        dialog.resizable(False, False)
        dialog.grab_set()
        
        # Add some padding
        frame = ttk.Frame(dialog, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Task text
        ttk.Label(frame, text="Task:").pack(anchor=tk.W, pady=(0, 2))
        text_var = tk.StringVar(value=todo["text"])
        text_entry = ttk.Entry(frame, textvariable=text_var)
        text_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Reminder
        ttk.Label(frame, text="Reminder:").pack(anchor=tk.W, pady=(0, 2))
        
        reminder_frame = ttk.Frame(frame)
        reminder_frame.pack(fill=tk.X, pady=(0, 10))
        
        reminder_var = tk.BooleanVar(value="reminder" in todo and todo["reminder"])
        reminder_check = ttk.Checkbutton(reminder_frame, text="Set reminder", variable=reminder_var)
        reminder_check.pack(side=tk.LEFT)
        
        # Date picker frame
        date_frame = ttk.Frame(frame)
        date_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Create date and time spinboxes
        current_datetime = datetime.now()
        if "reminder" in todo and todo["reminder"]:
            current_datetime = datetime.fromisoformat(todo["reminder"])
        
        # Date entry with format YYYY-MM-DD
        ttk.Label(date_frame, text="Date (YYYY-MM-DD):").pack(anchor=tk.W, pady=(0, 2))
        date_var = tk.StringVar(value=current_datetime.strftime("%Y-%m-%d"))
        date_entry = ttk.Entry(date_frame, textvariable=date_var)
        date_entry.pack(fill=tk.X, pady=(0, 5))
        
        # Time entry with format HH:MM
        ttk.Label(date_frame, text="Time (HH:MM):").pack(anchor=tk.W, pady=(0, 2))
        time_var = tk.StringVar(value=current_datetime.strftime("%H:%M"))
        time_entry = ttk.Entry(date_frame, textvariable=time_var)
        time_entry.pack(fill=tk.X)
        
        # Enable/disable date entry based on reminder checkbox
        def toggle_date_entry():
            if reminder_var.get():
                date_entry.configure(state="normal")
                time_entry.configure(state="normal")
            else:
                date_entry.configure(state="disabled")
                time_entry.configure(state="disabled")
        
        reminder_check.config(command=toggle_date_entry)
        toggle_date_entry()  # Initial state
        
        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        def save():
            new_text = text_var.get().strip()
            if not new_text:
                messagebox.showerror("Error", "Task text cannot be empty.")
                return
            
            # Update todo
            todo["text"] = new_text
            
            # Update reminder
            if reminder_var.get():
                try:
                    # Validate date format
                    date_str = date_var.get()
                    time_str = time_var.get()
                    reminder_datetime = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
                    todo["reminder"] = reminder_datetime.isoformat()
                except ValueError:
                    messagebox.showerror("Error", "Invalid date or time format.")
                    return
            else:
                if "reminder" in todo:
                    del todo["reminder"]
            
            # Save and refresh
            self.save_todos()
            self.refresh_todos()
            
            dialog.destroy()
        
        save_button = ttk.Button(button_frame, text="Save", command=save)
        save_button.pack(side=tk.LEFT, padx=(0, 5))
        
        cancel_button = ttk.Button(button_frame, text="Cancel", command=dialog.destroy)
        cancel_button.pack(side=tk.LEFT)
        
        # Focus on text entry
        text_entry.focus_set()
    
    def delete_todo(self, todo):
        """Delete a todo item."""
        if messagebox.askyesno("Confirm Deletion", 
                              f"Are you sure you want to delete this task?\n\n{todo['text']}"):
            self.todos.remove(todo)
            self.save_todos()
            self.refresh_todos()
    
    def toggle_todo_completed(self, todo, var):
        """Toggle the completed state of a todo item."""
        todo["completed"] = var.get()
        self.save_todos()
        self.refresh_todos()
    
    def check_due_reminders(self):
        """Check for reminders that are due and return them."""
        now = datetime.now()
        due_reminders = []
        
        for todo in self.todos:
            if "reminder" in todo and todo["reminder"] and not todo.get("notified", False):
                reminder_time = datetime.fromisoformat(todo["reminder"])
                
                # If reminder time is within the last minute and not already notified
                if reminder_time <= now and reminder_time > now - timedelta(minutes=1):
                    todo["notified"] = True
                    due_reminders.append(todo)
        
        # Save changes to notified status
        if due_reminders:
            self.save_todos()
            
        return due_reminders