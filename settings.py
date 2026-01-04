import os
import json

def get_data_path(filename):
    """Get the full path to a data file."""
    # Get the data directory
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    
    # Ensure the directory exists
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    # Return the full path to the file
    return os.path.join(data_dir, filename)

def ensure_data_directories():
    """Ensure all required directories exist."""
    # Data directory
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    # Assets directory
    assets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)

def load_settings():
    """Load settings from file."""
    settings_file = get_data_path("settings.json")
    
    if os.path.exists(settings_file):
        try:
            with open(settings_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}

def save_settings(settings):
    """Save settings to file."""
    settings_file = get_data_path("settings.json")
    
    with open(settings_file, 'w') as f:
        json.dump(settings, f, indent=2)
