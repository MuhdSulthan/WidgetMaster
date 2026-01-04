#!/usr/bin/env python3
import tkinter as tk
import calendar
import datetime
from PIL import Image, ImageTk

class ModernCalendarView(tk.Frame):
    """A modern calendar widget with todo item integration."""
    def __init__(self, parent, theme, todos=None, callback=None):
        self.theme = theme
        self.todos = todos if todos else []
        self.callback = callback  # Called when a day with todos is clicked
        
        super().__init__(
            parent,
            bg=theme.card_bg,
            padx=theme.card_padding,
            pady=theme.card_padding
        )
        
        # Initialize date to current date
        self.current_date = datetime.date.today()
        
        # Create the calendar UI
        self.create_widgets()
        
        # Render the calendar
        self.render_calendar()
        
        # Create todo preview
        self.create_todo_preview()
    
    def create_widgets(self):
        """Create the calendar widgets."""
        # Create container with rounded corners
        self.container = tk.Canvas(
            self,
            bg=self.theme.card_bg,
            highlightthickness=0,
            height=350,
            width=400
        )
        self.container.pack(fill=tk.BOTH, expand=True)
        
        # Frame for the month/year header
        self.header_frame = tk.Frame(
            self.container,
            bg=self.theme.card_bg
        )
        self.header_frame.place(relx=0.05, rely=0.05, relwidth=0.9, height=30)
        
        # Month/Year label
        self.month_year_label = tk.Label(
            self.header_frame,
            text="",
            bg=self.theme.card_bg,
            fg=self.theme.text_color,
            font=self.theme.get_font(self.theme.large_text_size, bold=True)
        )
        self.month_year_label.pack(side=tk.LEFT)
        
        # Navigation buttons
        self.prev_btn = tk.Label(
            self.header_frame,
            text="<",
            bg=self.theme.card_bg,
            fg=self.theme.secondary_text,
            font=self.theme.get_font(self.theme.large_text_size)
        )
        self.prev_btn.pack(side=tk.RIGHT, padx=(0, 10))
        self.prev_btn.bind("<Button-1>", self.previous_month)
        
        self.next_btn = tk.Label(
            self.header_frame,
            text=">",
            bg=self.theme.card_bg,
            fg=self.theme.secondary_text,
            font=self.theme.get_font(self.theme.large_text_size)
        )
        self.next_btn.pack(side=tk.RIGHT)
        self.next_btn.bind("<Button-1>", self.next_month)
        
        # Frame for the day headers
        self.days_header_frame = tk.Frame(
            self.container,
            bg=self.theme.card_bg
        )
        self.days_header_frame.place(relx=0.05, rely=0.15, relwidth=0.9, height=20)
        
        # Day headers
        days = ["S", "M", "T", "W", "T", "F", "S"]
        for i, day in enumerate(days):
            day_label = tk.Label(
                self.days_header_frame,
                text=day,
                bg=self.theme.card_bg,
                fg=self.theme.secondary_text,
                font=self.theme.get_font(self.theme.small_text_size)
            )
            day_label.place(relx=i/7, rely=0, relwidth=1/7, relheight=1)
        
        # Frame for the calendar days
        self.calendar_frame = tk.Frame(
            self.container,
            bg=self.theme.card_bg
        )
        self.calendar_frame.place(relx=0.05, rely=0.2, relwidth=0.9, relheight=0.5)
        
        # Create day buttons
        self.day_buttons = []
        for row in range(6):
            for col in range(7):
                day_frame = tk.Frame(
                    self.calendar_frame,
                    bg=self.theme.card_bg
                )
                day_frame.place(
                    relx=col/7, rely=row/6,
                    relwidth=1/7, relheight=1/6
                )
                
                day_button = tk.Label(
                    day_frame,
                    text="",
                    bg=self.theme.card_bg,
                    fg=self.theme.text_color,
                    font=self.theme.get_font(self.theme.normal_text_size)
                )
                day_button.place(relx=0.5, rely=0.5, anchor="center")
                day_button.bind("<Button-1>", lambda e, r=row, c=col: self.day_clicked(r, c))
                
                self.day_buttons.append(day_button)
    
    def create_todo_preview(self):
        """Create a preview of todos for the selected date."""
        self.todo_preview_frame = tk.Frame(
            self.container,
            bg=self.theme.card_bg
        )
        self.todo_preview_frame.place(relx=0.5, rely=0.8, relwidth=0.9, relheight=0.3, anchor="n")
        
        # Date label
        self.selected_date_label = tk.Label(
            self.todo_preview_frame,
            text="",
            bg=self.theme.card_bg,
            fg=self.theme.text_color,
            font=self.theme.get_font(self.theme.large_text_size, bold=True),
            anchor="w"
        )
        self.selected_date_label.pack(fill=tk.X)
        
        # Todos for selected date
        self.todo_list_frame = tk.Frame(
            self.todo_preview_frame,
            bg=self.theme.card_bg
        )
        self.todo_list_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Initially hide
        self.selected_date_label.config(text="")
    
    def render_calendar(self):
        """Render the calendar for the current month/year."""
        # Update the month/year label
        month_name = self.current_date.strftime("%B %Y")
        self.month_year_label.config(text=month_name)
        
        # Get calendar for current month
        cal = calendar.monthcalendar(self.current_date.year, self.current_date.month)
        
        # Clear all day buttons
        for button in self.day_buttons:
            button.config(text="", fg=self.theme.text_color, bg=self.theme.card_bg)
        
        # Fill in the days
        day_index = 0
        for week in cal:
            for day in week:
                if day == 0:
                    # Empty cell
                    self.day_buttons[day_index].config(text="")
                else:
                    # Day cell
                    self.day_buttons[day_index].config(text=str(day))
                    
                    # Highlight current day
                    if (day == self.current_date.day and 
                        datetime.date.today().month == self.current_date.month and 
                        datetime.date.today().year == self.current_date.year):
                        
                        self.day_buttons[day_index].config(
                            bg=self.theme.accent_color,
                            fg=self.theme.text_color
                        )
                    
                    # Highlight days with todos
                    elif self.has_todos_on_date(day):
                        self.day_buttons[day_index].config(
                            fg=self.theme.accent_color,
                            font=self.theme.get_font(self.theme.normal_text_size, bold=True)
                        )
                
                day_index += 1
    
    def has_todos_on_date(self, day):
        """Check if there are todos for the given day."""
        if not self.todos:
            return False
        
        date_str = f"{self.current_date.month}/{day}/{self.current_date.year}"
        
        for todo in self.todos:
            # Check for date formats MM/DD/YYYY
            if 'due_date' in todo and todo['due_date']:
                if date_str in todo['due_date']:
                    return True
        
        return False
    
    def get_todos_for_date(self, day):
        """Get todos for the given day."""
        if not self.todos:
            return []
        
        date_str = f"{self.current_date.month}/{day}/{self.current_date.year}"
        todos_for_date = []
        
        for todo in self.todos:
            # Check for date formats MM/DD/YYYY
            if 'due_date' in todo and todo['due_date']:
                if date_str in todo['due_date']:
                    todos_for_date.append(todo)
        
        return todos_for_date
    
    def next_month(self, event=None):
        """Go to next month."""
        year, month = self.current_date.year, self.current_date.month
        
        if month == 12:
            month = 1
            year += 1
        else:
            month += 1
        
        self.current_date = self.current_date.replace(year=year, month=month, day=1)
        self.render_calendar()
    
    def previous_month(self, event=None):
        """Go to previous month."""
        year, month = self.current_date.year, self.current_date.month
        
        if month == 1:
            month = 12
            year -= 1
        else:
            month -= 1
        
        self.current_date = self.current_date.replace(year=year, month=month, day=1)
        self.render_calendar()
    
    def day_clicked(self, row, col):
        """Handle day click event."""
        day_index = row * 7 + col
        day_button = self.day_buttons[day_index]
        
        if day_button['text']:
            day = int(day_button['text'])
            
            # Update selected date
            selected_date = self.current_date.replace(day=day)
            
            # Update preview
            self.update_todo_preview(selected_date)
            
            # Call callback if provided
            if self.callback:
                self.callback(selected_date)
    
    def update_todo_preview(self, date):
        """Update the todo preview for the selected date."""
        # Clear existing preview
        for widget in self.todo_list_frame.winfo_children():
            widget.destroy()
        
        # Update date label
        date_str = date.strftime("%B %d")
        self.selected_date_label.config(text=date_str)
        
        # Get todos for this date
        todos = self.get_todos_for_date(date.day)
        
        # Add todos to preview
        for todo in todos:
            if 'due_date' in todo and ':' in todo['due_date']:
                # Has time component
                time_str = todo['due_date'].split(' ')[0]  # Extract time part
                label_text = f"{todo['title']}\n{time_str}"
            else:
                label_text = todo['title']
            
            # Todo item with time
            todo_frame = tk.Frame(
                self.todo_list_frame,
                bg=self.theme.card_bg,
                padx=5, pady=5
            )
            todo_frame.pack(fill=tk.X, pady=2)
            
            # Title
            title_label = tk.Label(
                todo_frame,
                text=todo['title'],
                bg=self.theme.card_bg,
                fg=self.theme.text_color,
                font=self.theme.get_font(self.theme.normal_text_size),
                anchor="w",
                justify="left"
            )
            title_label.pack(fill=tk.X)
            
            # Time (if available)
            if 'due_date' in todo and ':' in todo['due_date']:
                time_str = todo['due_date'].split(' ')[0]  # Extract time part
                time_label = tk.Label(
                    todo_frame,
                    text=time_str,
                    bg=self.theme.card_bg,
                    fg=self.theme.secondary_text,
                    font=self.theme.get_font(self.theme.small_text_size),
                    anchor="w"
                )
                time_label.pack(fill=tk.X)
        
        # If no todos, show a message
        if not todos:
            no_todos_label = tk.Label(
                self.todo_list_frame,
                text="No tasks for this day",
                bg=self.theme.card_bg,
                fg=self.theme.secondary_text,
                font=self.theme.get_font(self.theme.small_text_size)
            )
            no_todos_label.pack(fill=tk.X, pady=10)
    
    def set_todos(self, todos):
        """Update the todos list."""
        self.todos = todos
        self.render_calendar()
        
        # Update preview if showing
        if self.selected_date_label['text']:
            # Extract day from label
            date_parts = self.selected_date_label['text'].split(' ')
            if len(date_parts) > 1:
                try:
                    day = int(date_parts[1])
                    selected_date = self.current_date.replace(day=day)
                    self.update_todo_preview(selected_date)
                except:
                    pass

# Example usage
if __name__ == "__main__":
    from modern_widget_tk import MinimalTheme
    
    root = tk.Tk()
    root.title("Calendar Test")
    root.geometry("400x500")
    root.configure(bg="#1a1e2e")
    
    # Sample todos
    todos = [
        {"title": "Finish report", "due_date": "4/14/2024", "completed": False},
        {"title": "Call dentist", "due_date": "10:00 AM", "completed": False},
        {"title": "Buy groceries", "due_date": "4/15/2024", "completed": True}
    ]
    
    # Create calendar
    calendar_view = ModernCalendarView(root, MinimalTheme(), todos)
    calendar_view.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    root.mainloop()