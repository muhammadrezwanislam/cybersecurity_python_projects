
import time
from PIL import ImageGrab
import os

# Create directory if it doesn't exist
save_dir = ""
os.makedirs(save_dir, exist_ok=True)

while True:
    # Take screenshot every 5 seconds
    time.sleep(5)
    
    # Create timestamp (using underscore instead of colon for filename compatibility)
    date_string = time.strftime("%Y-%m-%d_%H-%M-%S")
    
    # Capture the entire screen
    screenshot = ImageGrab.grab()
    
    # Save the screenshot to a file
    filepath = os.path.join(save_dir, f"{date_string}_screenshot.png")
    screenshot.save(filepath)
    
    # Close the screenshot
    screenshot.close()
    
    print(f'Screenshot taken: {filepath}')