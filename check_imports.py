#!/usr/bin/env python3
import os
import sys
import importlib.util

def check_module_exists(module_name):
    """Check if a module exists and can be imported."""
    try:
        spec = importlib.util.find_spec(module_name)
        return spec is not None
    except ModuleNotFoundError:
        return False

def print_result(module_name, exists):
    """Print a formatted result."""
    status = "✅ Found" if exists else "❌ Not found"
    print(f"{status}: {module_name}")

def main():
    print("=== MODULE AVAILABILITY CHECK ===")
    
    # Check tkinter
    print_result("tkinter", check_module_exists("tkinter"))
    
    # Check our application modules
    print_result("widget_tk", check_module_exists("widget_tk"))
    print_result("widget", check_module_exists("widget"))
    print_result("url_manager_tk", check_module_exists("url_manager_tk"))
    print_result("todo_manager_tk", check_module_exists("todo_manager_tk"))
    print_result("notification_manager_tk", check_module_exists("notification_manager_tk"))
    print_result("autostart_tk", check_module_exists("autostart_tk"))
    print_result("settings", check_module_exists("settings"))
    
    # Check dependencies
    print_result("PIL", check_module_exists("PIL"))
    
    # Print Python path
    print("\nPython Path:")
    for path in sys.path:
        print(f"  - {path}")
    
    # List Python files in current directory
    print("\nPython files in current directory:")
    for file in os.listdir('.'):
        if file.endswith('.py'):
            print(f"  - {file}")

if __name__ == "__main__":
    main()