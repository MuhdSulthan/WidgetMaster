#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import math

# Create directories if they don't exist
os.makedirs("assets", exist_ok=True)

def create_minimal_icon(size=(64, 64), icon_type="link", theme="dark"):
    """Create a minimal icon for the widget."""
    # Define colors based on theme
    if theme == "dark":
        bg_color = (27, 30, 46, 0)  # Transparent dark navy
        icon_color = (149, 155, 220)  # Light purple/blue
    else:
        bg_color = (240, 240, 245, 0)  # Transparent light background
        icon_color = (95, 100, 170)  # Darker purple/blue
    
    # Create base image with transparent background
    img = Image.new('RGBA', size, bg_color)
    draw = ImageDraw.Draw(img)
    
    width, height = size
    center_x, center_y = width // 2, height // 2
    radius = min(width, height) // 2 - 4
    stroke_width = max(2, int(radius * 0.15))
    
    # Draw different icons based on type
    if icon_type == "link":
        # Chain link icon
        link_size = radius * 0.7
        offset = radius * 0.3
        
        # Left circle
        draw.ellipse(
            [center_x - offset - link_size/2, center_y - link_size/3,
             center_x - offset + link_size/2, center_y + link_size/3],
            outline=icon_color,
            width=stroke_width
        )
        
        # Right circle
        draw.ellipse(
            [center_x + offset - link_size/2, center_y - link_size/3,
             center_x + offset + link_size/2, center_y + link_size/3],
            outline=icon_color,
            width=stroke_width
        )
        
        # Connection line
        draw.rectangle(
            [center_x - offset/2, center_y - stroke_width/2,
             center_x + offset/2, center_y + stroke_width/2],
            fill=icon_color
        )
        
    elif icon_type == "todo":
        # Checklist icon
        list_width = radius * 1.4
        list_height = radius * 1.4
        
        # Rounded rectangle outline
        draw.rounded_rectangle(
            [center_x - list_width/2, center_y - list_height/2,
             center_x + list_width/2, center_y + list_height/2],
            radius=list_width * 0.1,
            outline=icon_color,
            width=stroke_width
        )
        
        # Three horizontal lines
        line_spacing = list_height / 4
        line_width = list_width * 0.6
        for i in range(3):
            y_pos = center_y - list_height/4 + i * line_spacing
            draw.line(
                [center_x - line_width/2, y_pos,
                 center_x + line_width/2, y_pos],
                fill=icon_color,
                width=max(1, stroke_width // 2)
            )
            
    elif icon_type == "edit":
        # Pencil icon
        pencil_length = radius * 1.4
        pencil_width = radius * 0.4
        angle = 45  # Angle in degrees
        
        # Rotate point function
        def rotate_point(x, y, angle_deg):
            angle_rad = math.radians(angle_deg)
            return (
                x * math.cos(angle_rad) - y * math.sin(angle_rad),
                x * math.sin(angle_rad) + y * math.cos(angle_rad)
            )
        
        # Calculate pencil points
        top_left = rotate_point(-pencil_width/2, -pencil_length/2, angle)
        top_right = rotate_point(pencil_width/2, -pencil_length/2, angle)
        bottom_right = rotate_point(pencil_width/2, pencil_length/2, angle)
        bottom_left = rotate_point(-pencil_width/2, pencil_length/2, angle)
        
        # Adjust points to center
        points = [
            (center_x + top_left[0], center_y + top_left[1]),
            (center_x + top_right[0], center_y + top_right[1]),
            (center_x + bottom_right[0], center_y + bottom_right[1]),
            (center_x + bottom_left[0], center_y + bottom_left[1])
        ]
        
        # Draw pencil body
        draw.polygon(points, outline=icon_color, width=stroke_width)
        
        # Draw pencil tip
        tip_length = pencil_length * 0.2
        tip_point = rotate_point(0, -pencil_length/2 - tip_length, angle)
        tip_point = (center_x + tip_point[0], center_y + tip_point[1])
        
        draw.line(
            [points[0], tip_point],
            fill=icon_color,
            width=stroke_width
        )
        draw.line(
            [points[1], tip_point],
            fill=icon_color,
            width=stroke_width
        )
        
    elif icon_type == "close":
        # X icon
        offset = radius * 0.7
        
        draw.line(
            [center_x - offset, center_y - offset,
             center_x + offset, center_y + offset],
            fill=icon_color,
            width=stroke_width
        )
        
        draw.line(
            [center_x - offset, center_y + offset,
             center_x + offset, center_y - offset],
            fill=icon_color,
            width=stroke_width
        )
        
    elif icon_type == "checkbox_empty":
        # Empty circle checkbox
        draw.ellipse(
            [center_x - radius, center_y - radius,
             center_x + radius, center_y + radius],
            outline=icon_color,
            width=stroke_width
        )
        
    elif icon_type == "checkbox_checked":
        # Filled circle with checkmark
        # Circle
        draw.ellipse(
            [center_x - radius, center_y - radius,
             center_x + radius, center_y + radius],
            outline=icon_color,
            width=stroke_width
        )
        
        # Checkmark
        check_size = radius * 0.6
        check_offset = radius * 0.2
        
        draw.line(
            [center_x - check_size/2, center_y,
             center_x - check_offset, center_y + check_size/2],
            fill=icon_color,
            width=stroke_width
        )
        
        draw.line(
            [center_x - check_offset, center_y + check_size/2,
             center_x + check_size/2, center_y - check_size/2],
            fill=icon_color,
            width=stroke_width
        )
        
    elif icon_type == "calendar":
        # Calendar icon
        calendar_width = radius * 1.6
        calendar_height = radius * 1.6
        
        # Calendar outline
        draw.rounded_rectangle(
            [center_x - calendar_width/2, center_y - calendar_height/2,
             center_x + calendar_width/2, center_y + calendar_height/2],
            radius=calendar_width * 0.1,
            outline=icon_color,
            width=stroke_width
        )
        
        # Top bar
        top_bar_height = calendar_height * 0.2
        draw.rectangle(
            [center_x - calendar_width/2 + stroke_width/2, 
             center_y - calendar_height/2 + stroke_width/2,
             center_x + calendar_width/2 - stroke_width/2, 
             center_y - calendar_height/2 + top_bar_height],
            outline=icon_color,
            width=max(1, stroke_width // 2)
        )
        
        # Grid lines
        h_spacing = calendar_width / 4
        for i in range(1, 4):
            x = center_x - calendar_width/2 + i * h_spacing
            draw.line(
                [x, center_y - calendar_height/2 + top_bar_height + stroke_width,
                 x, center_y + calendar_height/2 - stroke_width],
                fill=icon_color,
                width=max(1, stroke_width // 2)
            )
            
        v_spacing = (calendar_height - top_bar_height) / 3
        for i in range(1, 3):
            y = center_y - calendar_height/2 + top_bar_height + i * v_spacing
            draw.line(
                [center_x - calendar_width/2 + stroke_width, y,
                 center_x + calendar_width/2 - stroke_width, y],
                fill=icon_color,
                width=max(1, stroke_width // 2)
            )
    
    elif icon_type == "remind":
        # Reminder/alert icon
        # Circle with exclamation mark
        draw.ellipse(
            [center_x - radius, center_y - radius,
             center_x + radius, center_y + radius],
            outline=icon_color,
            width=stroke_width
        )
        
        # Exclamation mark - vertical line
        mark_height = radius * 1.0
        dot_radius = max(2, stroke_width // 2)
        
        draw.line(
            [center_x, center_y - mark_height/2,
             center_x, center_y + mark_height/5],
            fill=icon_color,
            width=stroke_width
        )
        
        # Exclamation mark - dot
        draw.ellipse(
            [center_x - dot_radius, center_y + mark_height/2 - dot_radius,
             center_x + dot_radius, center_y + mark_height/2 + dot_radius],
            fill=icon_color
        )
    
    elif icon_type == "menu":
        # Hamburger menu (three lines)
        line_width = radius * 1.2
        line_spacing = radius * 0.6
        
        for i in range(3):
            y_pos = center_y - line_spacing + i * line_spacing
            draw.line(
                [center_x - line_width/2, y_pos,
                 center_x + line_width/2, y_pos],
                fill=icon_color,
                width=stroke_width
            )
    
    # Apply a slight blur for smoother edges
    img = img.filter(ImageFilter.GaussianBlur(0.5))
    
    # Save high-quality icon
    output_file = f"assets/minimal_{icon_type}_icon_{theme}.png"
    img.save(output_file, quality=95)
    print(f"Created minimal {icon_type} icon ({theme}): {output_file}")
    return output_file

def main():
    """Create all minimal icons."""
    # Create all minimal icons
    icon_types = ["link", "todo", "edit", "close", "checkbox_empty", 
                "checkbox_checked", "calendar", "remind", "menu"]
    
    for theme in ["dark", "light"]:
        for icon_type in icon_types:
            create_minimal_icon(size=(64, 64), icon_type=icon_type, theme=theme)
            
    print("All minimal icons created successfully!")

if __name__ == "__main__":
    main()