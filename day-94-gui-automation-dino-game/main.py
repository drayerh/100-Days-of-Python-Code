import pyautogui
import time

print("Position the Chrome Dino game window and make sure it's focused.")
print("You have 5 seconds to click on the game window...")
time.sleep(5)

# Press space to start the game
pyautogui.press('space')
time.sleep(1)

print("Click on the top-left corner of the detection area (just in front of the dino where obstacles appear).")
time.sleep(3)
x1, y1 = pyautogui.position()

print("Now click on the bottom-right corner of the detection area.")
time.sleep(3)
x2, y2 = pyautogui.position()

x = x1
y = y1
width = x2 - x1
height = y2 - y1

print(f"Detection region set to: x={x}, y={y}, width={width}, height={height}")

try:
    while True:
        # Capture the specified region
        screenshot = pyautogui.screenshot(region=(x, y, width, height))

        obstacle_detected = False

        # Check every 5th pixel to balance speed and accuracy
        for i in range(0, width, 5):
            for j in range(0, height, 5):
                # Get pixel color (RGB)
                pixel = screenshot.getpixel((i, j))
                # Check if pixel is not white (adjust threshold if necessary)
                if pixel[0] < 240 or pixel[1] < 240 or pixel[2] < 240:
                    obstacle_detected = True
                    break
            if obstacle_detected:
                break

        if obstacle_detected:
            pyautogui.press('space')
            time.sleep(0.1)  # Debounce to prevent multiple jumps

        time.sleep(0.01)  # Reduce CPU usage

except KeyboardInterrupt:
    print("\nExiting the bot...")