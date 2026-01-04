import tkinter as tk
from tkinter import ttk

class NotificationManager:
    def __init__(self):
        # Keep track of shown notifications to avoid duplicates
        self.shown_notifications = set()
        
        # Active notifications
        self.active_notifications = []
    
    def show_notification(self, title, message, notification_id=None):
        """Show a notification."""
        # Check if this notification was already shown recently
        if notification_id:
            if notification_id in self.shown_notifications:
                return
            self.shown_notifications.add(notification_id)
        
        # Create notification window
        notification = NotificationWindow(title, message)
        self.active_notifications.append(notification)
        
        # Clean up closed notifications
        self.active_notifications = [n for n in self.active_notifications if n.is_active]
    
    def clear_old_notifications(self):
        """Clear the list of shown notifications."""
        self.shown_notifications.clear()


class NotificationWindow:
    """Custom notification window that appears at the bottom-right corner."""
    
    def __init__(self, title, message):
        self.is_active = True
        
        # Create window
        self.window = tk.Toplevel()
        self.window.title("")
        self.window.geometry("300x100+{}+{}".format(
            self.window.winfo_screenwidth() - 320,  # 20px from right edge
            self.window.winfo_screenheight() - 120   # 20px from bottom edge
        ))
        self.window.attributes("-topmost", True)
        self.window.overrideredirect(True)  # No window decorations
        
        # Create frame
        frame = ttk.Frame(self.window, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Style
        style = ttk.Style()
        style.configure("Notification.TLabel", font=("Arial", 10, "bold"))
        
        # Title
        title_label = ttk.Label(frame, text=title, style="Notification.TLabel")
        title_label.pack(anchor=tk.W)
        
        # Message
        message_label = ttk.Label(frame, text=message, wraplength=280)
        message_label.pack(anchor=tk.W, pady=5)
        
        # Close button
        close_button = ttk.Button(frame, text="×", width=2, command=self.close)
        close_button.pack(anchor=tk.SE)
        
        # Auto-close after 5 seconds
        self.window.after(5000, self.close)
        
        # Handle window close
        self.window.protocol("WM_DELETE_WINDOW", self.close)
    
    def close(self):
        """Close the notification window."""
        if self.is_active:
            self.is_active = False
            self.window.destroy()