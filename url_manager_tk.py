import os
import json
import webbrowser
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from settings import get_data_path

class URLManager:
    def __init__(self):
        self.urls = self.load_urls()
        self._tooltip = None  # Initialize tooltip attribute
    
    def load_urls(self):
        """Load URLs from the JSON file."""
        urls_file = get_data_path("urls.json")
        
        if os.path.exists(urls_file):
            try:
                with open(urls_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []
    
    def save_urls(self):
        """Save URLs to the JSON file."""
        urls_file = get_data_path("urls.json")
        
        with open(urls_file, 'w') as f:
            json.dump(self.urls, f, indent=2)
    
    def create_widget(self, parent):
        """Create and return the URL manager widget."""
        # Create main frame
        frame = ttk.Frame(parent, padding=10)
        
        # Button frame for URL launchers
        self.button_frame = ttk.Frame(frame)
        self.button_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Scrollable container for buttons
        self.canvas = tk.Canvas(self.button_frame, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.button_frame, orient="vertical", command=self.canvas.yview)
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
        
        # Add URL buttons
        self.refresh_url_buttons()
        
        # Control buttons
        control_frame = ttk.Frame(frame)
        control_frame.pack(fill=tk.X, pady=(0, 5))
        
        add_button = ttk.Button(control_frame, text="Add URL Group", command=self.add_url_group)
        add_button.pack(side=tk.LEFT, padx=(0, 5))
        
        manage_button = ttk.Button(control_frame, text="Manage URLs", command=self.manage_urls)
        manage_button.pack(side=tk.LEFT)
        
        return frame
    
    def refresh_url_buttons(self):
        """Refresh all URL buttons."""
        # Clear existing buttons
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Add URL buttons
        for i, url_group in enumerate(self.urls):
            button = ttk.Button(
                self.scrollable_frame, 
                text=url_group["name"],
                command=lambda urls=url_group["urls"]: self.open_urls(urls)
            )
            button.pack(fill=tk.X, pady=2)
            
            # Add tooltip
            self.create_tooltip(button, "\n".join(url_group["urls"]))
    
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
    
    def open_urls(self, urls):
        """Open a list of URLs in the default browser."""
        for url in urls:
            try:
                webbrowser.open(url)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open URL: {url}\nError: {str(e)}")
    
    def add_url_group(self):
        """Add a new URL group."""
        self.show_url_dialog()
    
    def show_url_dialog(self, edit_index=None):
        """Show dialog to add or edit a URL group."""
        # Create dialog window
        dialog = tk.Toplevel()
        dialog.title("Add URL Group" if edit_index is None else "Edit URL Group")
        dialog.geometry("300x250")
        dialog.resizable(False, False)
        dialog.grab_set()
        
        # Add some padding
        frame = ttk.Frame(dialog, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Group name
        ttk.Label(frame, text="Group Name:").pack(anchor=tk.W, pady=(0, 2))
        name_var = tk.StringVar()
        name_entry = ttk.Entry(frame, textvariable=name_var)
        name_entry.pack(fill=tk.X, pady=(0, 10))
        
        # URLs
        ttk.Label(frame, text="URLs (one per line):").pack(anchor=tk.W, pady=(0, 2))
        url_text = tk.Text(frame, height=6)
        url_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Fill with existing data if editing
        if edit_index is not None:
            url_group = self.urls[edit_index]
            name_var.set(url_group["name"])
            url_text.insert("1.0", "\n".join(url_group["urls"]))
        
        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X)
        
        def save():
            name = name_var.get().strip()
            urls = [url.strip() for url in url_text.get("1.0", tk.END).split('\n') if url.strip()]
            
            if not name:
                messagebox.showerror("Error", "Please enter a group name.")
                return
            
            if not urls:
                messagebox.showerror("Error", "Please enter at least one URL.")
                return
            
            # Create new group or update existing one
            url_group = {"name": name, "urls": urls}
            
            if edit_index is not None:
                self.urls[edit_index] = url_group
            else:
                self.urls.append(url_group)
            
            # Save to file
            self.save_urls()
            
            # Update UI
            self.refresh_url_buttons()
            
            dialog.destroy()
        
        def cancel():
            dialog.destroy()
        
        save_button = ttk.Button(button_frame, text="Save", command=save)
        save_button.pack(side=tk.LEFT, padx=(0, 5))
        
        cancel_button = ttk.Button(button_frame, text="Cancel", command=cancel)
        cancel_button.pack(side=tk.LEFT)
        
        # Focus on name entry
        name_entry.focus_set()
    
    def manage_urls(self):
        """Show the URL manager dialog."""
        # Create dialog window
        dialog = tk.Toplevel()
        dialog.title("Manage URL Groups")
        dialog.geometry("400x300")
        dialog.resizable(True, True)
        dialog.grab_set()
        
        # Add some padding
        frame = ttk.Frame(dialog, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # URL list
        ttk.Label(frame, text="URL Groups:").pack(anchor=tk.W, pady=(0, 5))
        
        list_frame = ttk.Frame(frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.url_listbox = tk.Listbox(list_frame)
        self.url_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        listbox_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.url_listbox.yview)
        listbox_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.url_listbox.config(yscrollcommand=listbox_scrollbar.set)
        
        # Fill listbox with URL groups
        for url_group in self.urls:
            self.url_listbox.insert(tk.END, url_group["name"])
        
        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X)
        
        def edit():
            selected = self.url_listbox.curselection()
            if selected:
                index = selected[0]
                self.show_url_dialog(edit_index=index)
                # Update listbox
                self.url_listbox.delete(index)
                self.url_listbox.insert(index, self.urls[index]["name"])
                self.url_listbox.selection_set(index)
        
        def delete():
            selected = self.url_listbox.curselection()
            if selected:
                index = selected[0]
                name = self.urls[index]["name"]
                
                if messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete '{name}'?"):
                    del self.urls[index]
                    self.save_urls()
                    self.url_listbox.delete(index)
                    self.refresh_url_buttons()
        
        edit_button = ttk.Button(button_frame, text="Edit", command=edit)
        edit_button.pack(side=tk.LEFT, padx=(0, 5))
        
        delete_button = ttk.Button(button_frame, text="Delete", command=delete)
        delete_button.pack(side=tk.LEFT, padx=(0, 5))
        
        close_button = ttk.Button(button_frame, text="Close", command=dialog.destroy)
        close_button.pack(side=tk.LEFT)
        
        # Double-click to edit
        self.url_listbox.bind("<Double-1>", lambda e: edit())