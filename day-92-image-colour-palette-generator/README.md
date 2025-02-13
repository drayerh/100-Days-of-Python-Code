# Image Color Palette Generator

This project is a web application that analyzes the dominant colors in an uploaded image and displays the top 10 colors with their respective percentages.

## Features

- Upload an image and analyze its color palette
- Display the top 10 dominant colors with their hex codes and percentages
- Supports multiple image formats: PNG, JPG, JPEG, WEBP

## Requirements

- Python 3.8+
- Flask 3.0.0
- Pillow 10.0.0
- numpy 1.24.3
- colorthief 0.2.1
- gunicorn 20.1.0

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/drayerh/100-Days-of-Python-Code.git
    cd day-92-image-color-palette-generator
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the application:
    ```sh
    python app.py
    ```

2. Open your web browser and go to `http://localhost:5000`.

3. Upload an image to analyze its color palette.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.