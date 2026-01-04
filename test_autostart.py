import os
import sys
import platform
from autostart_tk import toggle_autostart
from settings import load_settings, save_settings, get_data_path

def test_autostart_configuration():
    """Test if autostart is correctly configured for the current platform."""
    print("Testing autostart configuration...")
    
    # Enable autostart
    result = toggle_autostart(True)
    if not result:
        print("❌ Failed to enable autostart")
        return False
    
    # Check if autostart files/registry entries exist
    system = platform.system()
    app_path = os.path.abspath(sys.argv[0])
    
    if system == "Windows":
        import winreg
        startup_key = r"Software\Microsoft\Windows\CurrentVersion\Run"
        app_name = "DesktopWidget"
        
        try:
            registry_key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, 
                startup_key, 
                0, 
                winreg.KEY_READ
            )
            
            value, _ = winreg.QueryValueEx(registry_key, app_name)
            winreg.CloseKey(registry_key)
            
            if f'"{app_path}"' == value:
                print("✅ Windows autostart configuration verified")
                return True
            else:
                print("❌ Windows autostart path mismatch")
                print(f"Expected: '{app_path}'")
                print(f"Found: '{value}'")
                return False
        except Exception as e:
            print(f"❌ Windows registry error: {e}")
            return False
            
    elif system == "Darwin":  # macOS
        launch_agent_path = os.path.expanduser("~/Library/LaunchAgents/com.user.desktopwidget.plist")
        if os.path.exists(launch_agent_path):
            print("✅ macOS autostart configuration verified")
            
            # Optionally, check content
            with open(launch_agent_path, 'r') as f:
                content = f.read()
                if app_path in content:
                    print("✅ macOS autostart path verified")
                    return True
                else:
                    print("❌ macOS autostart path mismatch")
                    print(f"Expected path '{app_path}' not found in plist file")
                    return False
        else:
            print(f"❌ macOS plist file not found at {launch_agent_path}")
            return False
            
    elif system == "Linux":
        desktop_file = os.path.expanduser("~/.config/autostart/desktopwidget.desktop")
        if os.path.exists(desktop_file):
            print("✅ Linux autostart configuration verified")
            
            # Check content
            with open(desktop_file, 'r') as f:
                content = f.read()
                if app_path in content:
                    print("✅ Linux autostart path verified")
                    return True
                else:
                    print("❌ Linux autostart path mismatch")
                    print(f"Expected path '{app_path}' not found in desktop file")
                    return False
        else:
            print(f"❌ Linux desktop file not found at {desktop_file}")
            return False
    
    print(f"❌ Unsupported platform: {system}")
    return False

def test_settings_persistence():
    """Test if autostart setting is correctly saved in settings file."""
    print("\nTesting settings persistence...")
    
    # Load current settings
    settings = load_settings()
    
    # Enable autostart in settings
    settings["autostart"] = True
    save_settings(settings)
    
    # Reload settings and check
    reloaded = load_settings()
    if reloaded.get("autostart") == True:
        print("✅ Autostart setting saved correctly")
    else:
        print("❌ Autostart setting not saved correctly")
        return False
    
    # Check actual settings file content
    settings_path = get_data_path("settings.json")
    if os.path.exists(settings_path):
        try:
            import json
            with open(settings_path, 'r') as f:
                raw_settings = json.load(f)
            
            if raw_settings.get("autostart") == True:
                print(f"✅ Settings file at {settings_path} contains correct autostart value")
                return True
            else:
                print(f"❌ Settings file at {settings_path} has wrong autostart value: {raw_settings.get('autostart')}")
                return False
        except Exception as e:
            print(f"❌ Error reading settings file: {e}")
            return False
    else:
        print(f"❌ Settings file not found at {settings_path}")
        return False

def cleanup():
    """Clean up by disabling autostart."""
    print("\nCleaning up...")
    toggle_autostart(False)
    
    # Also reset settings
    settings = load_settings()
    settings["autostart"] = False
    save_settings(settings)
    print("✅ Cleanup completed")

if __name__ == "__main__":
    print("=== AUTOSTART CONFIGURATION TEST ===")
    
    try:
        # Run tests
        config_result = test_autostart_configuration()
        settings_result = test_settings_persistence()
        
        # Show overall result
        print("\n=== TEST SUMMARY ===")
        if config_result and settings_result:
            print("✅ All tests passed! The app should work correctly on autostart.")
            print("When you select 'Start with computer' in the app, it will be configured to start automatically.")
        else:
            print("❌ Some tests failed. The app may not work correctly on autostart.")
            print("Check the detailed messages above for troubleshooting.")
    finally:
        # Always clean up at the end
        cleanup()