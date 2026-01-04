#!/usr/bin/env python3
import sys
import os
import json
import webbrowser
from datetime import datetime
from settings import ensure_data_directories, get_data_path

def run_cli_version():
    """Run a command-line interface version of the application when GUI is not available."""
    print("\n===== DESKTOP WIDGET - CLI VERSION =====\n")
    
    while True:
        print("\nMain Menu:")
        print("1. URL Launcher")
        print("2. Todo Manager")
        print("3. Settings")
        print("4. Exit")
        
        choice = input("\nSelect an option (1-4): ")
        
        if choice == "1":
            url_launcher_menu()
        elif choice == "2":
            todo_manager_menu()
        elif choice == "3":
            settings_menu()
        elif choice == "4":
            print("\nExiting Desktop Widget. Goodbye!")
            break
        else:
            print("\nInvalid choice. Please try again.")

def url_launcher_menu():
    """CLI menu for URL launcher."""
    # Load URLs
    urls_file = get_data_path("urls.json")
    if os.path.exists(urls_file):
        with open(urls_file, 'r') as f:
            url_groups = json.load(f)
    else:
        url_groups = []
    
    while True:
        print("\n----- URL LAUNCHER -----")
        
        # Display URL groups
        if not url_groups:
            print("\nNo URL groups defined.")
        else:
            print("\nURL Groups:")
            for i, group in enumerate(url_groups):
                print(f"{i+1}. {group['name']}")
        
        print("\nOptions:")
        print("a. Add URL Group")
        print("e. Edit URL Group")
        print("d. Delete URL Group")
        print("o. Open URL Group")
        print("b. Back to Main Menu")
        
        choice = input("\nSelect an option: ")
        
        if choice == "a":
            # Add URL group
            name = input("Enter group name: ")
            if not name.strip():
                print("Group name cannot be empty.")
                continue
            
            urls = []
            print("Enter URLs (one per line, empty line to finish):")
            while True:
                url = input("> ")
                if not url.strip():
                    break
                urls.append(url.strip())
            
            if not urls:
                print("URL group must contain at least one URL.")
                continue
            
            url_groups.append({"name": name, "urls": urls})
            with open(urls_file, 'w') as f:
                json.dump(url_groups, f, indent=2)
            print(f"URL group '{name}' added successfully.")
            
        elif choice == "e":
            if not url_groups:
                print("No URL groups to edit.")
                continue
            
            idx = input("Enter the number of the group to edit: ")
            try:
                idx = int(idx) - 1
                if idx < 0 or idx >= len(url_groups):
                    print("Invalid group number.")
                    continue
                
                group = url_groups[idx]
                print(f"Editing group: {group['name']}")
                
                name = input(f"Enter new name (or press enter to keep '{group['name']}'): ")
                if name.strip():
                    group['name'] = name
                
                print("Current URLs:")
                for i, url in enumerate(group['urls']):
                    print(f"{i+1}. {url}")
                
                print("\nOptions:")
                print("a. Add URL")
                print("d. Delete URL")
                print("k. Keep current URLs")
                
                url_choice = input("Select an option: ")
                
                if url_choice == "a":
                    urls = list(group['urls'])
                    print("Enter new URLs (one per line, empty line to finish):")
                    while True:
                        url = input("> ")
                        if not url.strip():
                            break
                        urls.append(url.strip())
                    
                    group['urls'] = urls
                    
                elif url_choice == "d":
                    idx_to_delete = input("Enter the number of the URL to delete: ")
                    try:
                        idx_to_delete = int(idx_to_delete) - 1
                        if idx_to_delete < 0 or idx_to_delete >= len(group['urls']):
                            print("Invalid URL number.")
                        else:
                            del group['urls'][idx_to_delete]
                            print("URL deleted.")
                    except ValueError:
                        print("Invalid input.")
                
                with open(urls_file, 'w') as f:
                    json.dump(url_groups, f, indent=2)
                print("URL group updated successfully.")
                
            except ValueError:
                print("Invalid input.")
            
        elif choice == "d":
            if not url_groups:
                print("No URL groups to delete.")
                continue
            
            idx = input("Enter the number of the group to delete: ")
            try:
                idx = int(idx) - 1
                if idx < 0 or idx >= len(url_groups):
                    print("Invalid group number.")
                    continue
                
                confirm = input(f"Are you sure you want to delete '{url_groups[idx]['name']}'? (y/n): ")
                if confirm.lower() == 'y':
                    del url_groups[idx]
                    with open(urls_file, 'w') as f:
                        json.dump(url_groups, f, indent=2)
                    print("URL group deleted successfully.")
                
            except ValueError:
                print("Invalid input.")
            
        elif choice == "o":
            if not url_groups:
                print("No URL groups to open.")
                continue
            
            idx = input("Enter the number of the group to open: ")
            try:
                idx = int(idx) - 1
                if idx < 0 or idx >= len(url_groups):
                    print("Invalid group number.")
                    continue
                
                group = url_groups[idx]
                print(f"Opening URLs for group: {group['name']}")
                
                for url in group['urls']:
                    try:
                        print(f"Opening: {url}")
                        webbrowser.open(url)
                    except Exception as e:
                        print(f"Error opening URL {url}: {e}")
                
            except ValueError:
                print("Invalid input.")
            
        elif choice == "b":
            break
        else:
            print("Invalid choice. Please try again.")

def todo_manager_menu():
    """CLI menu for todo manager."""
    # Load todos
    todos_file = get_data_path("todos.json")
    if os.path.exists(todos_file):
        with open(todos_file, 'r') as f:
            todos = json.load(f)
    else:
        todos = []
    
    while True:
        print("\n----- TODO MANAGER -----")
        
        # Display todos
        if not todos:
            print("\nNo todos defined.")
        else:
            print("\nTodos:")
            for i, todo in enumerate(todos):
                status = "[x]" if todo.get("completed", False) else "[ ]"
                reminder = ""
                if "reminder" in todo and todo["reminder"]:
                    reminder_time = datetime.fromisoformat(todo["reminder"])
                    reminder = f" (🔔 {reminder_time.strftime('%Y-%m-%d %H:%M')})"
                print(f"{i+1}. {status} {todo['text']}{reminder}")
        
        print("\nOptions:")
        print("a. Add Todo")
        print("e. Edit Todo")
        print("t. Toggle Completed")
        print("d. Delete Todo")
        print("b. Back to Main Menu")
        
        choice = input("\nSelect an option: ")
        
        if choice == "a":
            # Add todo
            text = input("Enter todo text: ")
            if not text.strip():
                print("Todo text cannot be empty.")
                continue
            
            has_reminder = input("Add a reminder? (y/n): ")
            reminder = None
            
            if has_reminder.lower() == 'y':
                date_str = input("Enter date (YYYY-MM-DD): ")
                time_str = input("Enter time (HH:MM): ")
                
                try:
                    reminder_datetime = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
                    reminder = reminder_datetime.isoformat()
                except ValueError:
                    print("Invalid date or time format.")
                    continue
            
            todo = {
                "id": str(len(todos) + 1),
                "text": text,
                "completed": False,
                "created": datetime.now().isoformat()
            }
            
            if reminder:
                todo["reminder"] = reminder
            
            todos.append(todo)
            with open(todos_file, 'w') as f:
                json.dump(todos, f, indent=2)
            print("Todo added successfully.")
            
        elif choice == "e":
            if not todos:
                print("No todos to edit.")
                continue
            
            idx = input("Enter the number of the todo to edit: ")
            try:
                idx = int(idx) - 1
                if idx < 0 or idx >= len(todos):
                    print("Invalid todo number.")
                    continue
                
                todo = todos[idx]
                print(f"Editing todo: {todo['text']}")
                
                text = input(f"Enter new text (or press enter to keep '{todo['text']}'): ")
                if text.strip():
                    todo['text'] = text
                
                has_reminder = input("Change reminder? (y/n): ")
                
                if has_reminder.lower() == 'y':
                    add_reminder = input("Add a reminder? (y/n): ")
                    
                    if add_reminder.lower() == 'y':
                        date_str = input("Enter date (YYYY-MM-DD): ")
                        time_str = input("Enter time (HH:MM): ")
                        
                        try:
                            reminder_datetime = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
                            todo["reminder"] = reminder_datetime.isoformat()
                        except ValueError:
                            print("Invalid date or time format.")
                            continue
                    else:
                        if "reminder" in todo:
                            del todo["reminder"]
                
                with open(todos_file, 'w') as f:
                    json.dump(todos, f, indent=2)
                print("Todo updated successfully.")
                
            except ValueError:
                print("Invalid input.")
            
        elif choice == "t":
            if not todos:
                print("No todos to toggle.")
                continue
            
            idx = input("Enter the number of the todo to toggle: ")
            try:
                idx = int(idx) - 1
                if idx < 0 or idx >= len(todos):
                    print("Invalid todo number.")
                    continue
                
                todo = todos[idx]
                todo["completed"] = not todo.get("completed", False)
                
                with open(todos_file, 'w') as f:
                    json.dump(todos, f, indent=2)
                
                status = "completed" if todo["completed"] else "not completed"
                print(f"Todo marked as {status}.")
                
            except ValueError:
                print("Invalid input.")
            
        elif choice == "d":
            if not todos:
                print("No todos to delete.")
                continue
            
            idx = input("Enter the number of the todo to delete: ")
            try:
                idx = int(idx) - 1
                if idx < 0 or idx >= len(todos):
                    print("Invalid todo number.")
                    continue
                
                confirm = input(f"Are you sure you want to delete '{todos[idx]['text']}'? (y/n): ")
                if confirm.lower() == 'y':
                    del todos[idx]
                    with open(todos_file, 'w') as f:
                        json.dump(todos, f, indent=2)
                    print("Todo deleted successfully.")
                
            except ValueError:
                print("Invalid input.")
            
        elif choice == "b":
            break
        else:
            print("Invalid choice. Please try again.")

def settings_menu():
    """CLI menu for settings."""
    # Load settings
    settings_file = get_data_path("settings.json")
    if os.path.exists(settings_file):
        with open(settings_file, 'r') as f:
            settings = json.load(f)
    else:
        settings = {}
    
    while True:
        print("\n----- SETTINGS -----")
        
        # Display current settings
        autostart = settings.get("autostart", False)
        print(f"Autostart: {'Enabled' if autostart else 'Disabled'}")
        
        print("\nOptions:")
        print("a. Toggle Autostart")
        print("b. Back to Main Menu")
        
        choice = input("\nSelect an option: ")
        
        if choice == "a":
            new_autostart = not autostart
            settings["autostart"] = new_autostart
            
            with open(settings_file, 'w') as f:
                json.dump(settings, f, indent=2)
            
            status = "enabled" if new_autostart else "disabled"
            print(f"Autostart {status}.")
            
            # In CLI mode, we just update the setting but don't actually
            # configure the system to run at startup
            print("Note: System autostart configuration is only applied in GUI mode.")
            
        elif choice == "b":
            break
        else:
            print("Invalid choice. Please try again.")

def main():
    """Main entry point for the desktop widget application."""
    # Ensure data directories exist
    ensure_data_directories()
    
    # Check if we can use a GUI
    try:
        # Try to import tkinter to see if it works
        import tkinter as tk
        
        # Try to create a test window to see if we have a display
        root = tk.Tk()
        root.title("Desktop Widget")
        root.destroy()  # We'll create a new window later
        
        # Check for assets/minimal icons - if not present, create them
        if not os.path.exists('assets/minimal_link_icon_dark.png'):
            print("Creating minimal icons...")
            try:
                import create_minimal_icons
                create_minimal_icons.main()
            except Exception as e:
                print(f"Error creating icons: {e}")
        
        # If we get here, GUI is available, import and run the GUI version
        try:
            # First try to use the new modern widget
            try:
                # Import the new modern implementation
                from modern_widget_tk import ModernDesktopWidget
                
                # Create and show modern widget (standalone window)
                widget = ModernDesktopWidget()
                widget.mainloop()
                
                # Exit after window is closed
                sys.exit(0)
                
            except Exception as e:
                # If modern widget fails, fall back to classic widget
                print(f"Error starting modern widget: {e}")
                print("Using modern widget with basic UI...")
                
                # Create new root window
                classic_root = tk.Tk()
                classic_root.wm_title("DesktopWidget")
                
                # Create and show simple widget - basic UI with core functionality
                from modern_widget_tk import ModernDesktopWidget
                widget = ModernDesktopWidget()
                
                # Start application event loop
                classic_root.mainloop()
                
        except Exception as e:
            # If all GUI attempts fail, fallback to CLI
            print(f"Error starting GUI: {e}")
            run_cli_version()
            
    except Exception as e:
        # If tkinter or display is not available, run CLI version
        print(f"GUI not available: {e}")
        run_cli_version()

if __name__ == "__main__":
    main()
