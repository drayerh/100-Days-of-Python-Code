import os
import re
import fitz
import boto3
import argparse
from pdf2image import convert_from_path
from pytesseract import image_to_string
from pydub import AudioSegment
from io import BytesIO
import tempfile

# Set the FFMPEG_BINARY and FFPROBE_BINARY environment variables to the path of the ffmpeg and ffprobe executables
os.environ["FFMPEG_BINARY"] = "ffmpeg"
os.environ["FFPROBE_BINARY"] = "ffprobe"

class PDFToSpeechConverter:
    def __init__(self, region='us-east-1'):
        # Initialize the Amazon Polly client with the specified region
        self.polly = boto3.client('polly', region_name=region)
        # Get the temporary directory path
        self.temp_dir = tempfile.gettempdir()

    def _extract_text_with_ocr(self, pdf_path):
        """Convert PDF to images and perform OCR, page by page"""
        # Convert PDF pages to images
        images = convert_from_path(pdf_path, dpi=300)
        text_pages = []

        # Perform OCR on each image and clean the extracted text
        for image in images:
            text = image_to_string(image, lang='eng')
            cleaned_text = re.sub(r'\s+', ' ', text).strip()
            text_pages.append(cleaned_text)

        return text_pages

    def _extract_text(self, pdf_path, force_ocr=False):
        """Extract text with OCR fallback, page by page"""
        text_pages = []
        if not force_ocr:
            try:
                # Open the PDF document
                doc = fitz.open(pdf_path)
                # Extract text from each page
                for page in doc:
                    text_pages.append(page.get_text())
                return text_pages
            except:
                pass
        # Fallback to OCR if text extraction fails
        return self._extract_text_with_ocr(pdf_path)

    def _process_text(self, text):
        """Clean and prepare text for synthesis"""
        # Remove extra whitespace and unwanted characters
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s.,;:!?\-()\']', '', text)
        return text[:300000]  # Polly character limit

    def _split_text(self, text, chunk_size=3000):
        """Split text into Polly-compatible chunks"""
        # Split text into chunks of specified size
        return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

    def _synthesize_speech(self, text, voice='Matthew', engine='neural'):
        """Convert text to speech using Amazon Polly"""
        # Synthesize speech using Amazon Polly
        response = self.polly.synthesize_speech(
            Text=text,
            OutputFormat='mp3',
            VoiceId=voice,
            Engine=engine,
            TextType='text'
        )
        # Return the audio stream as a BytesIO object
        return BytesIO(response['AudioStream'].read())

    def convert(self, pdf_path, output_file='output.mp3', voice='Matthew', force_ocr=False):
        """Main conversion method"""
        # Extract text from the PDF
        text_pages = self._extract_text(pdf_path, force_ocr)
        if not text_pages:
            raise ValueError("No text extracted from PDF")

        # Process and synthesize each page
        combined = AudioSegment.empty()
        for i, text in enumerate(text_pages):
            processed_text = self._process_text(text)
            if processed_text:
                print(f"Processing page {i + 1}/{len(text_pages)}")
                audio_stream = self._synthesize_speech(processed_text, voice)
                combined += AudioSegment.from_mp3(audio_stream)

        # Export the combined audio to the output file
        combined.export(output_file, format="mp3")
        return output_file


if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Convert PDF to Speech with OCR and Amazon Polly')
    parser.add_argument('pdf_path', help='Path to input PDF file')
    parser.add_argument('output_path', help='Path to output MP3 file')
    parser.add_argument('--voice', default='Matthew',
                        help='Polly voice name (e.g., Matthew, Joanna, Enrique)')
    parser.add_argument('--force-ocr', action='store_true',
                        help='Force OCR even for text-based PDFs')

    args = parser.parse_args()

    # Create an instance of the converter and perform the conversion
    converter = PDFToSpeechConverter()
    try:
        output = converter.convert(
            args.pdf_path,
            args.output_path,
            voice=args.voice,
            force_ocr=args.force_ocr
        )
        print(f"Successfully created audio file: {output}")
    except Exception as e:
        print(f"Error: {str(e)}")