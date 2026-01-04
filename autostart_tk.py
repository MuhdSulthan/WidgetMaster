import os
import sys
import platform

def toggle_autostart(enable):
    """Enable or disable application autostart."""
    app_path = sys.argv[0]
    
    # Get absolute path to the executable
    app_path = os.path.abspath(app_path)
    
    system = platform.system()
    
    if system == "Windows":
        import winreg
        startup_key = r"Software\Microsoft\Windows\CurrentVersion\Run"
        app_name = "DesktopWidget"
        
        try:
            registry_key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, 
                startup_key, 
                0, 
                winreg.KEY_WRITE
            )
            
            if enable:
                winreg.SetValueEx(
                    registry_key, 
                    app_name, 
                    0, 
                    winreg.REG_SZ, 
                    f'"{app_path}"'
                )
            else:
                try:
                    winreg.DeleteValue(registry_key, app_name)
                except FileNotFoundError:
                    pass  # Key doesn't exist, ignore
            
            winreg.CloseKey(registry_key)
            return True
        except Exception as e:
            print(f"Error configuring autostart: {e}")
            return False
            
    elif system == "Darwin":  # macOS
        launch_agent_dir = os.path.expanduser("~/Library/LaunchAgents")
        plist_path = os.path.join(launch_agent_dir, "com.user.desktopwidget.plist")
        
        if not os.path.exists(launch_agent_dir):
            os.makedirs(launch_agent_dir)
        
        plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.user.desktopwidget</string>
    <key>ProgramArguments</key>
    <array>
        <string>{app_path}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
"""
        
        try:
            if enable:
                with open(plist_path, "w") as f:
                    f.write(plist_content)
                os.chmod(plist_path, 0o644)
                # Load the agent
                os.system(f"launchctl load {plist_path}")
            else:
                if os.path.exists(plist_path):
                    # Unload the agent
                    os.system(f"launchctl unload {plist_path}")
                    os.remove(plist_path)
            return True
        except Exception as e:
            print(f"Error configuring autostart: {e}")
            return False
            
    elif system == "Linux":
        autostart_dir = os.path.expanduser("~/.config/autostart")
        desktop_file = os.path.join(autostart_dir, "desktopwidget.desktop")
        
        if not os.path.exists(autostart_dir):
            os.makedirs(autostart_dir)
        
        desktop_content = f"""[Desktop Entry]
Type=Application
Exec={app_path}
Hidden=false
NoDisplay=false
Name=Desktop Widget
Comment=Desktop Widget with URL launcher and todo list
X-GNOME-Autostart-enabled=true
"""
        
        try:
            if enable:
                with open(desktop_file, "w") as f:
                    f.write(desktop_content)
                os.chmod(desktop_file, 0o755)
            else:
                if os.path.exists(desktop_file):
                    os.remove(desktop_file)
            return True
        except Exception as e:
            print(f"Error configuring autostart: {e}")
            return False
    
    return False