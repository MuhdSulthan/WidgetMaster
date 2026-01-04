# Desktop Widget

A minimalist desktop widget application with URL launcher and to-do list functionality that runs offline and starts automatically with the computer.

## Features

- **URL Launcher**: Create groups of URLs that can be opened with a single click
- **To-do List**: Manage tasks with reminders
- **Autostart**: Configure the application to start automatically with the system
- **Dual Mode**: Runs as either a GUI widget or CLI application depending on environment

## Requirements

- Python 3.6 or higher
- Pillow library (for GUI mode)
- Tkinter (included with most Python installations)

## Installation

1. Clone or download this repository to your computer
2. Install required packages:
   ```bash
   pip install pillow
   ```

## Running the Application

### GUI Mode (Desktop Environment)

When run on a system with a graphical interface, the application will automatically launch in GUI mode:

```bash
python main.py
```

The desktop widget will appear as a small rectangular window on your screen, initially displaying just a header. Click the header to expand/collapse the widget.

#### Widget Features:
- **Header**: Click to expand/collapse, drag to move the widget
- **URL Launcher Tab**: Click buttons to open groups of URLs
- **To-do Tab**: Manage your tasks with checkboxes and reminders
- **System Tray Icon**: Access settings and minimize the widget

### CLI Mode (Terminal Environment)

When run in a terminal or headless environment (like Replit), the application automatically switches to CLI mode:

```bash
python main.py
```

Navigate through the menus by entering the corresponding number or letter:

1. **Main Menu**:
   - 1: URL Launcher
   - 2: Todo Manager
   - 3: Settings
   - 4: Exit

2. **URL Launcher Menu**:
   - a: Add URL Group
   - e: Edit URL Group
   - d: Delete URL Group
   - o: Open URL Group
   - b: Back to Main Menu

3. **Todo Manager Menu**:
   - a: Add Todo
   - e: Edit Todo
   - t: Toggle Completed
   - d: Delete Todo
   - b: Back to Main Menu

4. **Settings Menu**:
   - a: Toggle Autostart
   - b: Back to Main Menu

## Autostart Configuration

The application can be configured to start automatically when your computer boots:

- **In GUI Mode**: Use the system tray menu option "Start with computer"
- **In CLI Mode**: Use Settings menu option to toggle autostart

Autostart configuration works differently based on your operating system:
- Windows: Uses registry key
- macOS: Creates a LaunchAgent
- Linux: Creates a desktop entry in ~/.config/autostart

## Data Storage

All application data is stored in the `data` directory:
- `urls.json`: Saved URL groups
- `todos.json`: To-do items
- `settings.json`: Application settings and widget position

## License

This project is open source and available for personal or commercial use.