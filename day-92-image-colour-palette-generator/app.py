import logging
import os
from io import BytesIO
from flask import Flask, render_template, request, redirect, url_for, flash
import numpy as np
from collections import Counter
from PIL import Image
from colorthief import ColorThief
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration
app = Flask(__name__)
app.config.update({
    'SECRET_KEY': os.getenv('SECRET_KEY', 'dev-key-123'),  # Fallback to 'dev-key-123' if not set in .env
    'UPLOAD_FOLDER': 'uploads',
    'ALLOWED_EXTENSIONS': {'png', 'jpg', 'jpeg', 'webp'},
    'MAX_CONTENT_LENGTH': 10 * 1024 * 1024,  # 10MB
    'COLOR_COUNT': 10,
    'IMG_RESIZE_DIM': (500, 500),
    'CACHE_CONTROL': 'no-store, max-age=0'
})

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ColorAnalysisError(Exception):
    """Custom exception for color analysis errors"""
    pass


def allowed_file(filename):
    """
    Check if the uploaded file has an allowed extension.

    Args:
        filename (str): The name of the file.

    Returns:
        bool: True if the file has an allowed extension, False otherwise.
    """
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def get_dominant_colors(img_data):
    """
    Extract dominant colors using ColorThief with error handling.

    Args:
        img_data (BytesIO): The image data in a file-like object.

    Returns:
        list: A list of dominant colors as RGB tuples.

    Raises:
        ColorAnalysisError: If color extraction fails.
    """
    try:
        color_thief = ColorThief(img_data)
        return color_thief.get_palette(
            color_count=app.config['COLOR_COUNT'] + 3,
            quality=1
        )[:app.config['COLOR_COUNT']]
    except Exception as e:
        logger.error(f"Color extraction failed: {str(e)}")
        raise ColorAnalysisError("Failed to analyze image colors") from e


def rgb_to_hex(rgb):
    """
    Convert RGB tuple to hexadecimal representation.

    Args:
        rgb (tuple): The RGB color tuple.

    Returns:
        str: The hexadecimal representation of the color.
    """
    return '#{:02x}{:02x}{:02x}'.format(*rgb)


def analyze_image_colors(file):
    """
    Main analysis workflow with proper resource management.

    Args:
        file (FileStorage): The uploaded image file.

    Returns:
        list: A list of dictionaries containing color information.

    Raises:
        Exception: If image processing fails.
    """
    try:
        # Convert to in-memory file-like object
        img_bytes = BytesIO(file.read())

        # Validate image format
        img = Image.open(img_bytes)
        img.verify()
        img = Image.open(img_bytes)  # Reopen verified image

        # Convert to RGB and resize
        img = img.convert('RGB').resize(app.config['IMG_RESIZE_DIM'])
        img_bytes = BytesIO()
        img.save(img_bytes, format='JPEG')
        img_bytes.seek(0)

        # Extract color palette
        colors = get_dominant_colors(img_bytes)

        # Calculate percentages
        total = sum(1 for _ in img.getdata())
        color_counts = Counter(map(tuple, np.array(img).reshape(-1, 3)))

        # Match colors to percentages
        results = []
        for color in colors:
            hex_code = rgb_to_hex(color)
            percentage = color_counts.get(tuple(color), 0) / total * 100
            results.append({
                'hex': hex_code,
                'percentage': round(percentage, 2),
                'rgb': color
            })

        return sorted(results, key=lambda x: x['percentage'], reverse=True)

    except Exception as e:
        logger.error(f"Image processing error: {str(e)}")
        raise


@app.route('/', methods=['GET', 'POST'])
def upload_image():
    """
    Handle the file upload process and analyze the image colors.

    Returns:
        Response: The rendered template or a redirect response.
    """
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)

        if not allowed_file(file.filename):
            flash('Invalid file type')
            return redirect(request.url)

        if file.content_length > app.config['MAX_CONTENT_LENGTH']:
            flash('File size exceeds the maximum limit')
            return redirect(request.url)

        try:
            results = analyze_image_colors(file)
            return render_template('results.html', colors=results)
        except ColorAnalysisError:
            flash('Error analyzing image colors')
            return redirect(request.url)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            flash('Server error processing image')
            return redirect(request.url)

    return render_template('upload.html')


if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(host='0.0.0.0', port=5000)