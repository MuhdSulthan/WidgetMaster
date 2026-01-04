#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, font
import time
import datetime
import os
import sys
import json
import webbrowser
from PIL import Image, ImageTk

class MinimalTheme:
    """Theme colors and styling for the modern minimal widget."""
    def __init__(self, is_dark=True):
        # Base colors
        if is_dark:
            self.bg_color = "#1a1e2e"  # Dark navy background
            self.card_bg = "#242842"   # Slightly lighter navy for cards
            self.text_color = "#ffffff"  # White text
            self.secondary_text = "#8f96dd"  # Light purple/blue for secondary text
            self.accent_color = "#6978ff"  # Bright purple accent
            self.hover_color = "#535db2"  # Darker purple for hover
            self.border_color = "#323761"  # Border color for cards
            self.highlight_color = "#535db2"  # Highlight color for selected items
            self.error_color = "#ff5f5f"  # Red for errors/alerts
            self.success_color = "#5fd587"  # Green for success indicators
        else:
            self.bg_color = "#f8f9fa"  # Light background
            self.card_bg = "#ffffff"   # White for cards
            self.text_color = "#1a1e2e"  # Dark navy text
            self.secondary_text = "#5f63aa"  # Darker purple/blue for secondary text
            self.accent_color = "#6978ff"  # Same purple accent
            self.hover_color = "#535db2"  # Darker purple for hover
            self.border_color = "#e9ecef"  # Light gray border
            self.highlight_color = "#d8dbff"  # Light purple highlight
            self.error_color = "#ff5f5f"  # Red for errors/alerts
            self.success_color = "#5fd587"  # Green for success indicators

        # Derived colors
        self.shadow_color = "#101425" if is_dark else "#e1e4e8"
        
        # Fonts
        self.font_family = "Helvetica"
        self.title_size = 18
        self.large_text_size = 16
        self.normal_text_size = 12
        self.small_text_size = 10
        
        # Styling
        self.corner_radius = 15
        
        # Styling and animation settings
        self.card_padding = 15
        self.item_spacing = 10
        self.shadow_size = 15 if is_dark else 10
        self.opacity = 0.95  # Slight transparency for glass effect
        self.animation_speed = 10  # ms between animation frames
        self.animation_steps = 15  # number of steps in animations
    
    def get_font(self, size, bold=False):
        """Get font with the specified size and weight."""
        weight = "bold" if bold else "normal"
        return (self.font_family, size, weight)

class GlassFrame(tk.Canvas):
    """A canvas that creates a glass-like frame with rounded corners."""
    def __init__(self, parent, theme, width=300, height=200, **kwargs):
        self.theme = theme
        self.width = width
        self.height = height
        self.radius = theme.corner_radius
        
        super().__init__(
            parent,
            width=width,
            height=height,
            bg=theme.bg_color,
            highlightthickness=0,
            **kwargs
        )
        
        # Create the glass effect
        self.draw_glass_background()
        
        # Bind resize event
        self.bind("<Configure>", self.on_resize)
    
    def draw_glass_background(self):
        """Draw the glass-like background with rounded corners."""
        self.delete("glass_bg")
        
        # Create rounded rectangle
        self.rounded_rect(
            0, 0, self.width, self.height,
            radius=self.radius,
            fill=self.theme.card_bg,
            outline=self.theme.border_color,
            width=1,
            tags="glass_bg"
        )
    
    def rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        """Draw a rounded rectangle."""
        # Draw the main rectangle
        rect = self.create_rectangle(
            x1 + radius, y1,
            x2 - radius, y2,
            **kwargs
        )
        
        # Draw the four corner rectangles
        rect_top_left = self.create_rectangle(
            x1, y1 + radius,
            x1 + radius, y2 - radius,
            **kwargs
        )
        
        rect_top_right = self.create_rectangle(
            x2 - radius, y1 + radius,
            x2, y2 - radius,
            **kwargs
        )
        
        # Draw the four corner arcs
        arc_top_left = self.create_arc(
            x1, y1,
            x1 + 2 * radius, y1 + 2 * radius,
            start=90, extent=90,
            **kwargs
        )
        
        arc_top_right = self.create_arc(
            x2 - 2 * radius, y1,
            x2, y1 + 2 * radius,
            start=0, extent=90,
            **kwargs
        )
        
        arc_bottom_left = self.create_arc(
            x1, y2 - 2 * radius,
            x1 + 2 * radius, y2,
            start=180, extent=90,
            **kwargs
        )
        
        arc_bottom_right = self.create_arc(
            x2 - 2 * radius, y2 - 2 * radius,
            x2, y2,
            start=270, extent=90,
            **kwargs
        )
        
        return [rect, rect_top_left, rect_top_right, 
                arc_top_left, arc_top_right, arc_bottom_left, arc_bottom_right]
    
    def on_resize(self, event):
        """Handle resize events."""
        # Update dimensions
        self.width = event.width
        self.height = event.height
        
        # Redraw the background
        self.draw_glass_background()

class MinimalButton(tk.Canvas):
    """A minimal style button with an optional icon."""
    def __init__(self, parent, text="", icon_path=None, command=None, 
                 width=40, height=40, theme=None, text_only=False, **kwargs):
        self.theme = theme if theme else MinimalTheme()
        self.text = text
        self.icon_path = icon_path
        self.command = command
        self.width = width
        self.height = height
        self.text_only = text_only
        self.state = "normal"  # normal, hover, active
        
        # Get parent bg color safely
        try:
            parent_bg = parent.cget("bg")
        except:
            parent_bg = self.theme.bg_color
            
        super().__init__(
            parent,
            width=width,
            height=height,
            bg=parent_bg,
            highlightthickness=0,
            **kwargs
        )
        
        # Load icon if provided
        self.icon_image = None
        if icon_path and os.path.exists(icon_path):
            try:
                self.icon = Image.open(icon_path).convert("RGBA")
                # Scale icon to fit
                icon_size = min(width, height) - 16
                self.icon = self.icon.resize((icon_size, icon_size), Image.LANCZOS)
                self.icon_image = ImageTk.PhotoImage(self.icon)
            except Exception as e:
                print(f"Error loading icon {icon_path}: {e}")
        
        # Draw initial button
        self.draw_button()
        
        # Bind events
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_press)
        self.bind("<ButtonRelease-1>", self.on_release)
    
    def draw_button(self):
        """Draw the button based on current state."""
        self.delete("all")
        
        # Determine colors based on state
        if self.state == "normal":
            bg_color = self.theme.bg_color if self.text_only else self.theme.card_bg
            fg_color = self.theme.accent_color if self.text_only else self.theme.secondary_text
        elif self.state == "hover":
            bg_color = self.theme.bg_color if self.text_only else self.theme.card_bg
            fg_color = self.theme.accent_color
        else:  # active
            bg_color = self.theme.bg_color if self.text_only else self.theme.card_bg
            fg_color = self.theme.accent_color
        
        # Draw background (only for non-text buttons)
        if not self.text_only:
            if self.state == "active":
                # Add pressed effect
                self.create_rounded_rect(2, 2, self.width-2, self.height-2, 
                                      self.theme.corner_radius-2,
                                      fill=bg_color, outline=self.theme.border_color)
            else:
                self.create_rounded_rect(0, 0, self.width, self.height, 
                                      self.theme.corner_radius,
                                      fill=bg_color, outline=self.theme.border_color)
        
        # Draw icon
        if self.icon_image:
            # Center the icon
            icon_x = self.width // 2
            icon_y = self.height // 2
            
            # Adjust for text if needed
            if self.text and not self.text_only:
                icon_y = self.height // 3
            
            # Adjust coordinates if pressed
            if self.state == "active" and not self.text_only:
                icon_x += 1
                icon_y += 1
            
            self.create_image(icon_x, icon_y, image=self.icon_image)
        
        # Draw text
        if self.text:
            text_x = self.width // 2
            text_y = self.height // 2
            
            # Adjust for icon
            if self.icon_image and not self.text_only:
                text_y = self.height * 3 // 4
            
            # Adjust coordinates if pressed
            if self.state == "active" and not self.text_only:
                text_x += 1
                text_y += 1
            
            self.create_text(
                text_x, text_y,
                text=self.text,
                fill=fg_color,
                font=self.theme.get_font(
                    self.theme.normal_text_size if not self.text_only else self.theme.normal_text_size
                )
            )
    
    def create_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        """Create a rounded rectangle on the canvas."""
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)
    
    def on_enter(self, event):
        """Handle mouse enter event."""
        if self.state != "active":
            self.state = "hover"
            self.draw_button()
    
    def on_leave(self, event):
        """Handle mouse leave event."""
        if self.state != "active":
            self.state = "normal"
            self.draw_button()
    
    def on_press(self, event):
        """Handle mouse press event."""
        self.state = "active"
        self.draw_button()
    
    def on_release(self, event):
        """Handle mouse release event."""
        was_active = (self.state == "active")
        
        # Reset state
        if self.winfo_containing(event.x_root, event.y_root) == self:
            self.state = "hover"
        else:
            self.state = "normal"
        
        self.draw_button()
        
        # Execute command if button was active
        if was_active and self.command:
            self.command()

class TodoItem(tk.Frame):
    """A single todo item with checkbox, text, and action buttons."""
    def __init__(self, parent, todo, theme, toggle_callback=None, 
                 edit_callback=None, delete_callback=None):
        self.theme = theme
        self.todo = todo
        self.toggle_callback = toggle_callback
        self.edit_callback = edit_callback
        self.delete_callback = delete_callback
        
        super().__init__(
            parent,
            bg=theme.card_bg,
            padx=theme.card_padding,
            pady=theme.card_padding // 2
        )
        
        # Create container frame with rounded corners
        self.container = GlassFrame(
            self, theme, 
            height=60,
            width=parent.winfo_width() - 2 * theme.card_padding
        )
        self.container.pack(fill=tk.BOTH, expand=True)
        
        # Checkbox image
        checkbox_path = f"assets/minimal_checkbox_{'checked' if todo.get('completed', False) else 'empty'}_icon_dark.png"
        
        # Create frames for layout
        self.left_frame = tk.Frame(self.container, bg=theme.card_bg)
        self.left_frame.place(relx=0.02, rely=0.5, anchor="w")
        
        self.middle_frame = tk.Frame(self.container, bg=theme.card_bg)
        self.middle_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        self.right_frame = tk.Frame(self.container, bg=theme.card_bg)
        self.right_frame.place(relx=0.98, rely=0.5, anchor="e")
        
        # Checkbox
        self.checkbox_btn = MinimalButton(
            self.left_frame,
            icon_path=checkbox_path,
            command=self.toggle_completed,
            width=30, height=30,
            theme=theme
        )
        self.checkbox_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Todo text
        text_color = theme.secondary_text if todo.get('completed', False) else theme.text_color
        self.todo_text = tk.Label(
            self.middle_frame,
            text=todo.get('title', 'Untitled Todo'),
            bg=theme.card_bg,
            fg=text_color,
            font=theme.get_font(theme.normal_text_size),
            wraplength=200
        )
        self.todo_text.pack(side=tk.LEFT)
        
        # Due date if present
        if 'due_date' in todo and todo['due_date']:
            date_color = theme.error_color if self.is_due_soon() else theme.secondary_text
            self.due_date = tk.Label(
                self.middle_frame,
                text=f" ({todo['due_date']})",
                bg=theme.card_bg,
                fg=date_color,
                font=theme.get_font(theme.small_text_size)
            )
            self.due_date.pack(side=tk.LEFT)
        
        # Reminder icon if needed
        if self.is_due_soon():
            self.remind_icon = MinimalButton(
                self.right_frame,
                icon_path="assets/minimal_remind_icon_dark.png",
                width=24, height=24,
                theme=theme
            )
            self.remind_icon.pack(side=tk.LEFT, padx=5)
        
        # Edit button
        self.edit_btn = MinimalButton(
            self.right_frame,
            icon_path="assets/minimal_edit_icon_dark.png",
            command=self.edit_todo,
            width=24, height=24,
            theme=theme
        )
        self.edit_btn.pack(side=tk.LEFT, padx=5)
        
        # Menu button (for delete)
        self.menu_btn = MinimalButton(
            self.right_frame,
            icon_path="assets/minimal_menu_icon_dark.png",
            command=self.show_menu,
            width=24, height=24,
            theme=theme
        )
        self.menu_btn.pack(side=tk.LEFT, padx=5)
        
        # Apply strikethrough for completed todos
        if todo.get('completed', False):
            self._add_strikethrough()
    
    def _add_strikethrough(self):
        """Add strikethrough to the todo text."""
        self.todo_text.configure(fg=self.theme.secondary_text)
        # Note: tkinter doesn't support true strikethrough,
        # so we're using color change to indicate completion
    
    def toggle_completed(self):
        """Toggle the completed state of the todo."""
        self.todo['completed'] = not self.todo.get('completed', False)
        
        # Update checkbox image
        checkbox_path = f"assets/minimal_checkbox_{'checked' if self.todo['completed'] else 'empty'}_icon_dark.png"
        self.checkbox_btn.icon_path = checkbox_path
        
        # Reload the icon
        if os.path.exists(checkbox_path):
            try:
                icon = Image.open(checkbox_path).convert("RGBA")
                icon = icon.resize((24, 24), Image.LANCZOS)
                self.checkbox_btn.icon_image = ImageTk.PhotoImage(icon)
                self.checkbox_btn.draw_button()
            except Exception as e:
                print(f"Error loading icon {checkbox_path}: {e}")
        
        # Update text styling
        if self.todo['completed']:
            self._add_strikethrough()
        else:
            self.todo_text.configure(fg=self.theme.text_color)
        
        # Call callback if provided
        if self.toggle_callback:
            self.toggle_callback(self.todo)
    
    def edit_todo(self):
        """Edit this todo item."""
        if self.edit_callback:
            self.edit_callback(self.todo)
    
    def delete_todo(self):
        """Delete this todo item."""
        if self.delete_callback:
            self.delete_callback(self.todo)
    
    def is_due_soon(self):
        """Check if the todo is due soon (within 24 hours)."""
        if 'due_date' not in self.todo or not self.todo['due_date']:
            return False
        
        try:
            # Parse due date from string
            due_datetime = datetime.datetime.strptime(
                self.todo['due_date'], 
                "%I:%M %p" if ":" in self.todo['due_date'] else "%m/%d/%Y"
            )
            
            # If only time was provided, assume it's for today
            if ":" in self.todo['due_date']:
                now = datetime.datetime.now()
                due_datetime = due_datetime.replace(
                    year=now.year, month=now.month, day=now.day
                )
            
            # Check if due within the next 24 hours
            time_diff = due_datetime - datetime.datetime.now()
            return time_diff.total_seconds() < 24 * 60 * 60 and time_diff.total_seconds() > 0
        except Exception:
            # If parsing fails, assume not due soon
            return False
    
    def show_menu(self):
        """Show a popup menu with delete option."""
        menu = tk.Menu(self, tearoff=0, bg=self.theme.card_bg, fg=self.theme.text_color,
                      activebackground=self.theme.accent_color, activeforeground=self.theme.text_color)
        menu.add_command(label="Delete", command=self.delete_todo)
        
        # Get position relative to the button
        x = self.menu_btn.winfo_rootx()
        y = self.menu_btn.winfo_rooty() + self.menu_btn.winfo_height()
        
        # Display the menu
        menu.tk_popup(x, y)

class URLItem(tk.Frame):
    """A single URL group button."""
    def __init__(self, parent, url_group, theme, edit_callback=None, open_callback=None):
        self.theme = theme
        self.url_group = url_group
        self.edit_callback = edit_callback
        self.open_callback = open_callback
        
        super().__init__(
            parent,
            bg=theme.accent_color,
            padx=theme.card_padding,
            pady=theme.card_padding // 2
        )
        
        # Create container with rounded corners
        self.container = tk.Canvas(
            self,
            bg=theme.accent_color,
            highlightthickness=0,
            height=70,
            width=parent.winfo_width() - 2 * theme.card_padding
        )
        self.container.pack(fill=tk.BOTH, expand=True)
        
        # Add rounded rectangle drawing method
        def create_rounded_rect(canvas, x1, y1, x2, y2, radius, **kwargs):
            points = [
                x1 + radius, y1,
                x2 - radius, y1,
                x2, y1,
                x2, y1 + radius,
                x2, y2 - radius,
                x2, y2,
                x2 - radius, y2,
                x1 + radius, y2,
                x1, y2,
                x1, y2 - radius,
                x1, y1 + radius,
                x1, y1
            ]
            return canvas.create_polygon(points, smooth=True, **kwargs)
        
        # Draw rounded rectangle background
        self.rounded_rect = create_rounded_rect(
            self.container, 
            0, 0, 
            self.container.winfo_width(), 
            self.container.winfo_height(),
            theme.corner_radius,
            fill=theme.accent_color,
            outline=theme.border_color,
            width=1
        )
        
        # URL icon
        self.icon = MinimalButton(
            self.container,
            icon_path="assets/minimal_link_icon_dark.png",
            width=36, height=36,
            theme=theme
        )
        self.icon.place(relx=0.05, rely=0.5, anchor="w")
        
        # URL group name
        self.name_label = tk.Label(
            self.container,
            text=url_group.get('name', 'Unnamed Group'),
            bg=theme.accent_color,
            fg=theme.text_color,
            font=theme.get_font(theme.normal_text_size, bold=True)
        )
        self.name_label.place(relx=0.15, rely=0.5, anchor="w")
        
        # Make the whole item clickable
        self.container.bind("<Button-1>", self.open_urls)
        self.name_label.bind("<Button-1>", self.open_urls)
    
    def open_urls(self, event=None):
        """Open all URLs in this group."""
        if self.open_callback:
            self.open_callback(self.url_group)

class TabButton(tk.Canvas):
    """A tab button for switching between views."""
    def __init__(self, parent, text, active=False, command=None, theme=None, width=150, height=40):
        self.theme = theme if theme else MinimalTheme()
        self.text = text
        self.active = active
        self.command = command
        self.width = width
        self.height = height
        
        super().__init__(
            parent,
            width=width,
            height=height,
            bg=self.theme.bg_color,
            highlightthickness=0
        )
        
        # Draw the tab
        self.draw_tab()
        
        # Bind events
        self.bind("<Button-1>", self.on_click)
    
    def draw_tab(self):
        """Draw the tab based on active state."""
        self.delete("all")
        
        # Determine colors based on active state
        bg_color = self.theme.accent_color if self.active else self.theme.card_bg
        text_color = self.theme.text_color if self.active else self.theme.secondary_text
        
        # Draw rounded rectangle for tab
        self.create_rounded_rect(
            0, 0, self.width, self.height,
            self.theme.corner_radius,
            fill=bg_color
        )
        
        # Draw text
        self.create_text(
            self.width // 2, self.height // 2,
            text=self.text,
            fill=text_color,
            font=self.theme.get_font(self.theme.normal_text_size, bold=self.active)
        )
    
    def create_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        """Create a rounded rectangle on the canvas."""
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)
    
    def set_active(self, active):
        """Set the active state of the tab."""
        if self.active != active:
            self.active = active
            self.draw_tab()
    
    def on_click(self, event):
        """Handle click event."""
        if not self.active and self.command:
            self.command()

class ModernDesktopWidget(tk.Tk):
    """Modern minimal desktop widget with dark theme."""
    def __init__(self):
        super().__init__()
        
        # Set window properties
        self.title("Desktop Widget")
        self.overrideredirect(True)  # Remove window decorations
        self.attributes("-topmost", True)  # Keep on top of other windows
        self.attributes("-alpha", 0.97)  # Slight transparency
        
        # Initialize theme
        self.theme = MinimalTheme(is_dark=True)
        
        # Set window size and position
        self.width = 400
        self.height = 70  # Collapsed height
        self.expanded_height = 500  # Expanded height
        self.expanded = False
        
        # Set position to bottom-right of screen
        self.set_position_bottom_right()
        
        # Initialize UI
        self.init_ui()
        
        # Track drag state
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.dragging = False
        
        # Set window background color
        self.configure(bg=self.theme.bg_color)
        
        # Load data
        self.load_data()
        
        # Set up animation variables
        self.animating = False
        self.animation_progress = 0
        self.target_height = self.height
        
        # Start ticking for clock updates
        self.tick()
    
    def set_position_bottom_right(self):
        """Position the widget at the bottom-right of the screen."""
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Calculate position
        x = screen_width - self.width - 20
        y = screen_height - self.height - 40  # Above taskbar
        
        self.geometry(f"{self.width}x{self.height}+{x}+{y}")
    
    def init_ui(self):
        """Initialize the UI components."""
        # Main container that holds everything
        self.main_container = GlassFrame(
            self, self.theme,
            width=self.width - 20,
            height=self.height - 20
        )
        self.main_container.place(relx=0.5, rely=0.5, anchor="center")
        
        # Create the collapsed view (always visible)
        self.create_collapsed_view()
        
        # Create the expanded view (initially hidden)
        self.create_expanded_view()
        
        # Bind events
        self.bind_events()
    
    def create_collapsed_view(self):
        """Create the collapsed view with date/time and buttons."""
        # Collapsed view frame
        self.collapsed_frame = tk.Frame(
            self.main_container,
            bg=self.theme.card_bg
        )
        self.collapsed_frame.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Left side: Date and time
        self.date_label = tk.Label(
            self.collapsed_frame,
            text=time.strftime("%b %d, %Y"),
            bg=self.theme.card_bg,
            fg=self.theme.text_color,
            font=self.theme.get_font(self.theme.large_text_size, bold=True)
        )
        self.date_label.place(relx=0.05, rely=0.3, anchor="w")
        
        self.time_label = tk.Label(
            self.collapsed_frame,
            text=time.strftime("%I:%M %p"),
            bg=self.theme.card_bg,
            fg=self.theme.secondary_text,
            font=self.theme.get_font(self.theme.title_size)
        )
        self.time_label.place(relx=0.05, rely=0.7, anchor="w")
        
        # Right side: Function buttons
        btn_spacing = 15
        btn_size = 36
        btn_y = self.height // 2
        
        # Link button
        self.link_btn = MinimalButton(
            self.collapsed_frame,
            icon_path="assets/minimal_link_icon_dark.png",
            command=self.toggle_expand,
            width=btn_size, height=btn_size,
            theme=self.theme
        )
        self.link_btn.place(relx=0.7, rely=0.5, anchor="center")
        
        # Todo button
        self.todo_btn = MinimalButton(
            self.collapsed_frame,
            icon_path="assets/minimal_todo_icon_dark.png",
            command=lambda: self.toggle_expand(tab="todo"),
            width=btn_size, height=btn_size,
            theme=self.theme
        )
        self.todo_btn.place(relx=0.8, rely=0.5, anchor="center")
        
        # Edit button
        self.edit_btn = MinimalButton(
            self.collapsed_frame,
            icon_path="assets/minimal_edit_icon_dark.png",
            command=self.show_settings,
            width=btn_size, height=btn_size,
            theme=self.theme
        )
        self.edit_btn.place(relx=0.9, rely=0.5, anchor="center")
    
    def create_expanded_view(self):
        """Create the expanded view with tabs and content."""
        # Expanded view frame
        self.expanded_frame = tk.Frame(
            self.main_container,
            bg=self.theme.card_bg
        )
        
        # Initially hide the expanded view
        # It will be shown when toggling expand
        
        # Top bar with close button
        self.top_bar = tk.Frame(
            self.expanded_frame,
            bg=self.theme.card_bg,
            height=40
        )
        self.top_bar.pack(fill=tk.X, pady=(10, 5))
        
        # URL shortcut button
        self.shortcut_btn = MinimalButton(
            self.top_bar,
            icon_path="assets/minimal_link_icon_dark.png",
            width=36, height=36,
            theme=self.theme
        )
        self.shortcut_btn.pack(side=tk.LEFT, padx=15)
        
        # Close button
        self.close_btn = MinimalButton(
            self.top_bar,
            icon_path="assets/minimal_close_icon_dark.png",
            command=self.toggle_expand,
            width=36, height=36,
            theme=self.theme
        )
        self.close_btn.pack(side=tk.RIGHT, padx=15)
        
        # Tab bar
        self.tab_bar = tk.Frame(
            self.expanded_frame,
            bg=self.theme.card_bg,
            height=50
        )
        self.tab_bar.pack(fill=tk.X, padx=15, pady=10)
        
        # URL tab
        self.url_tab = TabButton(
            self.tab_bar,
            text="URLs",
            active=True,
            command=lambda: self.switch_tab("url"),
            theme=self.theme,
            width=150, height=40
        )
        self.url_tab.pack(side=tk.LEFT, padx=(0, 5))
        
        # Todo tab
        self.todo_tab = TabButton(
            self.tab_bar,
            text="To-Do",
            active=False,
            command=lambda: self.switch_tab("todo"),
            theme=self.theme,
            width=150, height=40
        )
        self.todo_tab.pack(side=tk.LEFT, padx=(5, 0))
        
        # Content frame (holds URL or Todo content)
        self.content_frame = tk.Frame(
            self.expanded_frame,
            bg=self.theme.card_bg
        )
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Create URL content
        self.url_frame = tk.Frame(
            self.content_frame,
            bg=self.theme.card_bg
        )
        self.url_frame.pack(fill=tk.BOTH, expand=True)
        
        # URL list
        self.url_list = tk.Frame(
            self.url_frame,
            bg=self.theme.card_bg
        )
        self.url_list.pack(fill=tk.BOTH, expand=True)
        
        # Add URL button
        self.add_url_btn = MinimalButton(
            self.url_frame,
            text="Add URL Group",
            command=self.add_url_group,
            width=150, height=40,
            theme=self.theme
        )
        self.add_url_btn.pack(pady=15)
        
        # Create Todo content (initially hidden)
        self.todo_frame = tk.Frame(
            self.content_frame,
            bg=self.theme.card_bg
        )
        # Will be packed when tab is selected
        
        # Todo list
        self.todo_list = tk.Frame(
            self.todo_frame,
            bg=self.theme.card_bg
        )
        self.todo_list.pack(fill=tk.BOTH, expand=True)
        
        # Add Todo button
        self.add_todo_btn = MinimalButton(
            self.todo_frame,
            text="Add To-Do",
            command=self.add_todo,
            width=150, height=40,
            theme=self.theme
        )
        self.add_todo_btn.pack(pady=15)
    
    def bind_events(self):
        """Bind events for drag and resize."""
        # Make the entire widget draggable from the collapsed view
        # Also make sure buttons and interactive elements don't trigger drag
        for widget in [self.collapsed_frame, self.top_bar, self.date_label, self.time_label, self.main_container]:
            widget.bind("<Button-1>", self.on_drag_start)
            widget.bind("<B1-Motion>", self.on_drag_motion)
            widget.bind("<ButtonRelease-1>", self.on_drag_stop)
        
        # Set cursor to indicate draggable areas
        self.collapsed_frame.config(cursor="fleur")  # "fleur" is the move cursor
        self.top_bar.config(cursor="fleur")
        
        # Add special styling to indicate the widget is draggable
        self.collapsed_frame.bind("<Enter>", lambda e: self.collapsed_frame.config(relief="raised"))
        self.collapsed_frame.bind("<Leave>", lambda e: self.collapsed_frame.config(relief="flat"))
        self.top_bar.bind("<Enter>", lambda e: self.top_bar.config(relief="raised"))
        self.top_bar.bind("<Leave>", lambda e: self.top_bar.config(relief="flat"))
    
    def on_drag_start(self, event):
        """Start dragging the widget."""
        # Don't start dragging from buttons or interactive elements
        if isinstance(event.widget, MinimalButton) or event.widget == self.todo_list or event.widget == self.url_list:
            return
            
        if not self.dragging:
            self.drag_start_x = event.x_root - self.winfo_x()
            self.drag_start_y = event.y_root - self.winfo_y()
            self.dragging = True
            
            # Visual feedback that we're dragging
            self.config(cursor="fleur")
    
    def on_drag_motion(self, event):
        """Move the widget during dragging."""
        if self.dragging:
            x = event.x_root - self.drag_start_x
            y = event.y_root - self.drag_start_y
            
            # Ensure the widget stays within screen boundaries
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()
            
            # Make sure at least 40px of the widget is always visible
            x = max(min(x, screen_width - 40), -self.width + 40)
            y = max(min(y, screen_height - 40), 0)
            
            self.geometry(f"+{x}+{y}")
    
    def on_drag_stop(self, event):
        """Stop dragging the widget."""
        self.dragging = False
        self.config(cursor="")
    
    def tick(self):
        """Update time and check for animations."""
        # Update time
        current_time = time.strftime("%I:%M %p")
        current_date = time.strftime("%b %d, %Y")
        
        self.time_label.config(text=current_time)
        self.date_label.config(text=current_date)
        
        # Check for animations
        if self.animating:
            self.animate_resize()
        
        # Schedule next tick
        self.after(1000, self.tick)
    
    def animate_resize(self):
        """Animate the widget resizing."""
        if self.animation_progress < self.theme.animation_steps:
            # Calculate the new height
            start_height = self.height if self.expanded else self.expanded_height
            end_height = self.expanded_height if self.expanded else self.height
            
            progress_ratio = self.animation_progress / self.theme.animation_steps
            current_height = int(start_height + (end_height - start_height) * progress_ratio)
            
            # Update window height
            self.geometry(f"{self.width}x{current_height}+{self.winfo_x()}+{self.winfo_y()}")
            
            # Resize the main container
            self.main_container.config(height=current_height - 20)
            
            # Increment progress
            self.animation_progress += 1
            
            # Schedule next frame
            self.after(self.theme.animation_speed, self.animate_resize)
        else:
            # Animation complete
            self.animating = False
            self.animation_progress = 0
            
            # Final resize to exact target
            self.geometry(f"{self.width}x{self.target_height}+{self.winfo_x()}+{self.winfo_y()}")
            self.main_container.config(height=self.target_height - 20)
            
            # Show/hide appropriate frames
            if self.expanded:
                self.expanded_frame.place(x=0, y=0, relwidth=1, relheight=1)
                self.collapsed_frame.place_forget()
            else:
                self.collapsed_frame.place(x=0, y=0, relwidth=1, relheight=1)
                self.expanded_frame.place_forget()
    
    def toggle_expand(self, tab=None):
        """Toggle between expanded and collapsed views."""
        if self.animating:
            return
        
        self.expanded = not self.expanded
        
        # Switch to the specified tab if provided
        if tab and tab.lower() == "todo" and self.expanded:
            self.switch_tab("todo")
        else:
            self.switch_tab("url")
        
        # Set target height for animation
        self.target_height = self.expanded_height if self.expanded else self.height
        
        # Start animation
        self.animating = True
        self.animation_progress = 0
        self.animate_resize()
    
    def switch_tab(self, tab):
        """Switch between URL and Todo tabs."""
        if tab.lower() == "url":
            self.url_tab.set_active(True)
            self.todo_tab.set_active(False)
            self.todo_frame.pack_forget()
            self.url_frame.pack(fill=tk.BOTH, expand=True)
        else:  # todo tab
            self.url_tab.set_active(False)
            self.todo_tab.set_active(True)
            self.url_frame.pack_forget()
            self.todo_frame.pack(fill=tk.BOTH, expand=True)
        
        # Refresh content
        self.refresh_content()
    
    def refresh_content(self):
        """Refresh the content of the current tab."""
        if self.url_tab.active:
            self.refresh_url_list()
        else:
            self.refresh_todo_list()
    
    def refresh_url_list(self):
        """Refresh the URL list."""
        # Clear existing items
        for widget in self.url_list.winfo_children():
            widget.destroy()
        
        # Add URL groups
        for url_group in self.urls:
            url_item = URLItem(
                self.url_list,
                url_group,
                self.theme,
                edit_callback=self.edit_url_group,
                open_callback=self.open_urls
            )
            url_item.pack(fill=tk.X, pady=5)
    
    def refresh_todo_list(self):
        """Refresh the todo list."""
        # Clear existing items
        for widget in self.todo_list.winfo_children():
            widget.destroy()
        
        # Add todos
        for todo in self.todos:
            todo_item = TodoItem(
                self.todo_list,
                todo,
                self.theme,
                toggle_callback=self.toggle_todo_completed,
                edit_callback=self.edit_todo,
                delete_callback=self.delete_todo
            )
            todo_item.pack(fill=tk.X, pady=5)
    
    def load_data(self):
        """Load URLs and todos from JSON files."""
        # URLs
        self.urls = []
        try:
            if os.path.exists("data/urls.json"):
                with open("data/urls.json", "r") as file:
                    self.urls = json.load(file)
        except Exception as e:
            print(f"Error loading URLs: {e}")
        
        # Todos
        self.todos = []
        try:
            if os.path.exists("data/todos.json"):
                with open("data/todos.json", "r") as file:
                    self.todos = json.load(file)
        except Exception as e:
            print(f"Error loading todos: {e}")
        
        # Create data directory if it doesn't exist
        os.makedirs("data", exist_ok=True)
        
        # Refresh content
        self.refresh_content()
    
    def save_urls(self):
        """Save URLs to JSON file."""
        try:
            with open("data/urls.json", "w") as file:
                json.dump(self.urls, file, indent=4)
        except Exception as e:
            print(f"Error saving URLs: {e}")
    
    def save_todos(self):
        """Save todos to JSON file."""
        try:
            with open("data/todos.json", "w") as file:
                json.dump(self.todos, file, indent=4)
        except Exception as e:
            print(f"Error saving todos: {e}")
    
    def add_url_group(self):
        """Add a new URL group."""
        # Create a dialog
        dialog = tk.Toplevel(self)
        dialog.title("Add URL Group")
        dialog.geometry("400x300")
        dialog.configure(bg=self.theme.bg_color)
        dialog.grab_set()  # Make dialog modal
        
        # Name entry
        name_frame = tk.Frame(dialog, bg=self.theme.bg_color)
        name_frame.pack(fill=tk.X, padx=20, pady=10)
        
        name_label = tk.Label(
            name_frame,
            text="Group Name:",
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.get_font(self.theme.normal_text_size)
        )
        name_label.pack(anchor="w")
        
        name_entry = tk.Entry(
            name_frame,
            bg=self.theme.card_bg,
            fg=self.theme.text_color,
            insertbackground=self.theme.text_color,
            font=self.theme.get_font(self.theme.normal_text_size),
            relief=tk.FLAT,
            bd=10
        )
        name_entry.pack(fill=tk.X, pady=5)
        
        # URLs entry
        urls_frame = tk.Frame(dialog, bg=self.theme.bg_color)
        urls_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        urls_label = tk.Label(
            urls_frame,
            text="URLs (one per line):",
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.get_font(self.theme.normal_text_size)
        )
        urls_label.pack(anchor="w")
        
        urls_text = tk.Text(
            urls_frame,
            bg=self.theme.card_bg,
            fg=self.theme.text_color,
            insertbackground=self.theme.text_color,
            font=self.theme.get_font(self.theme.normal_text_size),
            relief=tk.FLAT,
            bd=10,
            height=6
        )
        urls_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Buttons
        button_frame = tk.Frame(dialog, bg=self.theme.bg_color)
        button_frame.pack(fill=tk.X, padx=20, pady=15)
        
        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            command=dialog.destroy,
            bg=self.theme.card_bg,
            fg=self.theme.text_color,
            activebackground=self.theme.accent_color,
            activeforeground=self.theme.text_color,
            font=self.theme.get_font(self.theme.normal_text_size),
            relief=tk.FLAT,
            padx=15, pady=5
        )
        cancel_btn.pack(side=tk.LEFT)
        
        save_btn = tk.Button(
            button_frame,
            text="Save",
            command=lambda: self.save_new_url_group(name_entry.get(), urls_text.get("1.0", tk.END), dialog),
            bg=self.theme.accent_color,
            fg=self.theme.text_color,
            activebackground=self.theme.hover_color,
            activeforeground=self.theme.text_color,
            font=self.theme.get_font(self.theme.normal_text_size),
            relief=tk.FLAT,
            padx=15, pady=5
        )
        save_btn.pack(side=tk.RIGHT)
    
    def save_new_url_group(self, name, urls_text, dialog):
        """Save a new URL group."""
        if not name.strip():
            return  # Require a name
        
        # Parse URLs
        urls = [url.strip() for url in urls_text.split("\n") if url.strip()]
        
        # Create the URL group
        url_group = {
            "name": name,
            "urls": urls
        }
        
        # Add to the list
        self.urls.append(url_group)
        
        # Save to file
        self.save_urls()
        
        # Close the dialog
        dialog.destroy()
        
        # Refresh the URL list
        self.refresh_url_list()
    
    def edit_url_group(self, url_group):
        """Edit an existing URL group."""
        # Similar to add_url_group, but populate fields with existing data
        pass
    
    def open_urls(self, url_group):
        """Open all URLs in the group."""
        for url in url_group.get("urls", []):
            try:
                # Add http:// if not present
                if not url.startswith(("http://", "https://")):
                    url = "http://" + url
                webbrowser.open(url)
            except Exception as e:
                print(f"Error opening URL {url}: {e}")
    
    def add_todo(self):
        """Add a new todo item."""
        # Create a dialog
        dialog = tk.Toplevel(self)
        dialog.title("Add To-Do")
        dialog.geometry("400x250")
        dialog.configure(bg=self.theme.bg_color)
        dialog.grab_set()  # Make dialog modal
        
        # Title entry
        title_frame = tk.Frame(dialog, bg=self.theme.bg_color)
        title_frame.pack(fill=tk.X, padx=20, pady=10)
        
        title_label = tk.Label(
            title_frame,
            text="Title:",
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.get_font(self.theme.normal_text_size)
        )
        title_label.pack(anchor="w")
        
        title_entry = tk.Entry(
            title_frame,
            bg=self.theme.card_bg,
            fg=self.theme.text_color,
            insertbackground=self.theme.text_color,
            font=self.theme.get_font(self.theme.normal_text_size),
            relief=tk.FLAT,
            bd=10
        )
        title_entry.pack(fill=tk.X, pady=5)
        
        # Due date entry
        due_frame = tk.Frame(dialog, bg=self.theme.bg_color)
        due_frame.pack(fill=tk.X, padx=20, pady=10)
        
        due_var = tk.BooleanVar()
        due_check = tk.Checkbutton(
            due_frame,
            text="Set Due Date/Time",
            variable=due_var,
            command=lambda: toggle_due_entry(),
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            selectcolor=self.theme.card_bg,
            activebackground=self.theme.bg_color,
            activeforeground=self.theme.text_color,
            font=self.theme.get_font(self.theme.normal_text_size)
        )
        due_check.pack(anchor="w")
        
        due_entry_frame = tk.Frame(due_frame, bg=self.theme.bg_color)
        
        due_entry = tk.Entry(
            due_entry_frame,
            bg=self.theme.card_bg,
            fg=self.theme.text_color,
            insertbackground=self.theme.text_color,
            font=self.theme.get_font(self.theme.normal_text_size),
            relief=tk.FLAT,
            bd=10
        )
        due_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        due_format = tk.Label(
            due_entry_frame,
            text="Format: 10:00 AM or MM/DD/YYYY",
            bg=self.theme.bg_color,
            fg=self.theme.secondary_text,
            font=self.theme.get_font(self.theme.small_text_size)
        )
        due_format.pack(anchor="w", pady=(2, 0))
        
        def toggle_due_entry():
            if due_var.get():
                due_entry_frame.pack(fill=tk.X, pady=5)
            else:
                due_entry_frame.pack_forget()
        
        # Initially hide due entry
        toggle_due_entry()
        
        # Buttons
        button_frame = tk.Frame(dialog, bg=self.theme.bg_color)
        button_frame.pack(fill=tk.X, padx=20, pady=15)
        
        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            command=dialog.destroy,
            bg=self.theme.card_bg,
            fg=self.theme.text_color,
            activebackground=self.theme.accent_color,
            activeforeground=self.theme.text_color,
            font=self.theme.get_font(self.theme.normal_text_size),
            relief=tk.FLAT,
            padx=15, pady=5
        )
        cancel_btn.pack(side=tk.LEFT)
        
        save_btn = tk.Button(
            button_frame,
            text="Save",
            command=lambda: self.save_new_todo(title_entry.get(), due_entry.get() if due_var.get() else "", dialog),
            bg=self.theme.accent_color,
            fg=self.theme.text_color,
            activebackground=self.theme.hover_color,
            activeforeground=self.theme.text_color,
            font=self.theme.get_font(self.theme.normal_text_size),
            relief=tk.FLAT,
            padx=15, pady=5
        )
        save_btn.pack(side=tk.RIGHT)
    
    def save_new_todo(self, title, due_date, dialog):
        """Save a new todo item."""
        if not title.strip():
            return  # Require a title
        
        # Create the todo item
        todo = {
            "title": title,
            "completed": False
        }
        
        # Add due date if provided
        if due_date.strip():
            todo["due_date"] = due_date.strip()
        
        # Add to the list
        self.todos.append(todo)
        
        # Save to file
        self.save_todos()
        
        # Close the dialog
        dialog.destroy()
        
        # Refresh the todo list
        self.refresh_todo_list()
    
    def edit_todo(self, todo):
        """Edit an existing todo item."""
        # Similar to add_todo, but populate fields with existing data
        pass
    
    def delete_todo(self, todo):
        """Delete a todo item."""
        # Remove from list
        if todo in self.todos:
            self.todos.remove(todo)
            
            # Save to file
            self.save_todos()
            
            # Refresh the todo list
            self.refresh_todo_list()
    
    def toggle_todo_completed(self, todo):
        """Toggle the completed state of a todo item."""
        # Update the todo
        todo["completed"] = not todo.get("completed", False)
        
        # Save to file
        self.save_todos()
    
    def show_settings(self):
        """Show the settings dialog."""
        # Create a dialog
        dialog = tk.Toplevel(self)
        dialog.title("Settings")
        dialog.geometry("400x300")
        dialog.configure(bg=self.theme.bg_color)
        dialog.grab_set()  # Make dialog modal
        
        # Theme selection
        theme_frame = tk.Frame(dialog, bg=self.theme.bg_color)
        theme_frame.pack(fill=tk.X, padx=20, pady=10)
        
        theme_label = tk.Label(
            theme_frame,
            text="Theme:",
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            font=self.theme.get_font(self.theme.normal_text_size)
        )
        theme_label.pack(anchor="w")
        
        theme_var = tk.StringVar(value="dark")
        dark_radio = tk.Radiobutton(
            theme_frame,
            text="Dark",
            variable=theme_var,
            value="dark",
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            selectcolor=self.theme.card_bg,
            activebackground=self.theme.bg_color,
            activeforeground=self.theme.text_color,
            font=self.theme.get_font(self.theme.normal_text_size)
        )
        dark_radio.pack(anchor="w", padx=20)
        
        light_radio = tk.Radiobutton(
            theme_frame,
            text="Light",
            variable=theme_var,
            value="light",
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            selectcolor=self.theme.card_bg,
            activebackground=self.theme.bg_color,
            activeforeground=self.theme.text_color,
            font=self.theme.get_font(self.theme.normal_text_size)
        )
        light_radio.pack(anchor="w", padx=20)
        
        # Autostart option
        autostart_frame = tk.Frame(dialog, bg=self.theme.bg_color)
        autostart_frame.pack(fill=tk.X, padx=20, pady=10)
        
        autostart_var = tk.BooleanVar(value=False)
        autostart_check = tk.Checkbutton(
            autostart_frame,
            text="Start with system",
            variable=autostart_var,
            bg=self.theme.bg_color,
            fg=self.theme.text_color,
            selectcolor=self.theme.card_bg,
            activebackground=self.theme.bg_color,
            activeforeground=self.theme.text_color,
            font=self.theme.get_font(self.theme.normal_text_size)
        )
        autostart_check.pack(anchor="w")
        
        # Buttons
        button_frame = tk.Frame(dialog, bg=self.theme.bg_color)
        button_frame.pack(fill=tk.X, padx=20, pady=15)
        
        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            command=dialog.destroy,
            bg=self.theme.card_bg,
            fg=self.theme.text_color,
            activebackground=self.theme.accent_color,
            activeforeground=self.theme.text_color,
            font=self.theme.get_font(self.theme.normal_text_size),
            relief=tk.FLAT,
            padx=15, pady=5
        )
        cancel_btn.pack(side=tk.LEFT)
        
        save_btn = tk.Button(
            button_frame,
            text="Save",
            command=lambda: self.save_settings(theme_var.get(), autostart_var.get(), dialog),
            bg=self.theme.accent_color,
            fg=self.theme.text_color,
            activebackground=self.theme.hover_color,
            activeforeground=self.theme.text_color,
            font=self.theme.get_font(self.theme.normal_text_size),
            relief=tk.FLAT,
            padx=15, pady=5
        )
        save_btn.pack(side=tk.RIGHT)
    
    def save_settings(self, theme, autostart, dialog):
        """Save settings and apply them."""
        # Save settings to file
        settings = {
            "theme": theme,
            "autostart": autostart
        }
        
        try:
            with open("data/settings.json", "w") as file:
                json.dump(settings, file, indent=4)
        except Exception as e:
            print(f"Error saving settings: {e}")
        
        # Apply settings
        # Changing theme would require restarting the application
        # Setting autostart would require platform-specific code
        
        # Close the dialog
        dialog.destroy()
    
    def quit_app(self):
        """Quit the application."""
        self.destroy()

def main():
    """Main entry point for the application."""
    app = ModernDesktopWidget()
    app.mainloop()

if __name__ == "__main__":
    main()