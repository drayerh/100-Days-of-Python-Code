# Disappearing Text Writing App

This is a simple web application built with Flask and JavaScript that deletes the text in a textarea if the user stops writing for a specified duration.

## Features

- Timer that resets when the user types
- Deletes text if the user stops typing
- Alerts the user when the text is deleted

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/drayerh/100-Days-of-Python-Code.git
    cd day-90-Disappearing-Text-Writing-App
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the Flask application:
    ```sh
    python main.py
    ```

2. Open your web browser and go to `http://127.0.0.1:5000/`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.