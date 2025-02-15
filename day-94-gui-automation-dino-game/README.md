# GUI Automation Dino Game

This project automates the Chrome Dino game using Python and the `pyautogui` library.

## Requirements

- Python 3.x
- `pyautogui` library

## Installation

1. Clone the repository:
    ```sh
    git clone clone https://github.com/drayerh/100-Days-of-Python-Code.git
    cd day-94-gui-automation-dino-game
    ```

2. Install the required dependencies:
    ```sh
    pip install pyautogui
    ```

## Usage

1. Run the script:
    ```sh
    python main.py
    ```

2. Follow the on-screen instructions to set up the detection area.

## How It Works

The script captures a region of the screen where obstacles appear and checks for non-white pixels to detect obstacles. When an obstacle is detected, it presses the space bar to make the dino jump.

## License

This project is licensed under the MIT License.