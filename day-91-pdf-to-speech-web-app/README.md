# PDF to Speech Web App

This project is a PDF to Speech converter that uses OCR (Optical Character Recognition) and Amazon Polly to convert PDF documents into speech. The application extracts text from PDF files, processes it, and synthesizes speech for each page, combining the audio into a single MP3 file. It handles both text-based and image-based PDFs, with an option to force OCR.

## Features

- Extracts text from PDF files page by page.
- Uses OCR for image-based PDFs.
- Synthesizes speech using Amazon Polly.
- Combines audio from each page into a single MP3 file.
- Supports multiple Polly voices.
- Command-line interface for easy usage.

## Requirements

- Python 3.7+
- pip (Python package installer)
- Amazon Web Services (AWS) account with access to Amazon Polly
- ffmpeg (for audio processing)

## Installation
                                                                                                    
1. **Clone the repository:**

    ```sh
    git clone https://github.com/drayerh/100-Days-of-Python-Code.git
    cd day-91-pdf-to-speech-web-app
    ```

2. **Create and activate a virtual environment:**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Install ffmpeg:**

    - On macOS:

        ```sh
        brew install ffmpeg
        ```

    - On Ubuntu:

        ```sh
        sudo apt update
        sudo apt install ffmpeg
        ```

    - On Windows:

        Download and install ffmpeg from [ffmpeg.org](https://ffmpeg.org/download.html).

## Usage

To convert a PDF to speech, use the command-line interface:

```sh
python main.py <pdf_path> <output_path> [--voice <voice_name>] [--force-ocr]