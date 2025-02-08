from flask import Flask, render_template

# Create a Flask application instance
app = Flask(__name__)

@app.route('/')
def home():
    """
    Handle requests to the root URL ('/') and render the 'index.html' template.

    Returns:
        str: The rendered HTML content of 'index.html'.
    """
    return render_template('index.html')

if __name__ == '__main__':
    # Run the Flask application in debug mode
    app.run(debug=True)