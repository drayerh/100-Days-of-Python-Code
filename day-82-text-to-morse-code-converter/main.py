import click
import data
import logging
import json
from colorama import init, Fore

# Initialize colorama
init(autoreset=True)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('error.log')
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logging.getLogger().addHandler(file_handler)

def load_custom_dict(file_path=data.MORSE_CODE_DICT):
    """
    Load a custom Morse Code dictionary from a JSON file.

    Args:
        file_path (str): The path to the custom dictionary file.

    Returns:
        dict: The custom Morse Code dictionary.
    """
    try:
        with open(file_path, 'r') as file:
            custom_dict = json.load(file)
        logging.info(f"Loaded custom Morse Code dictionary from {file_path}")
        return custom_dict
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Error loading custom dictionary: {e}")
        raise ValueError(f"Error loading custom dictionary: {e}")

def text_to_morse(text, morse_dict):
    """
    Convert text to Morse Code.

    Args:
        text (str): The text to convert.
        morse_dict (dict): The Morse Code dictionary to use.

    Returns:
        str: The converted Morse Code.
    """
    if not text:
        return ""

    valid_chars = set(morse_dict.keys())
    morse_code = []
    invalid_chars = []

    for char in text.upper():
        if char in valid_chars:
            morse_code.append(morse_dict[char])
        else:
            invalid_chars.append(char)

    if invalid_chars:
        logging.error(f"Invalid characters in input text: {invalid_chars}")
        raise ValueError(f"Invalid characters in input text: {invalid_chars}")

    logging.info(f"Converted text to Morse Code: {text} -> {' '.join(morse_code)}")
    return ' '.join(morse_code)

def morse_to_text(morse, morse_dict):
    """
    Convert Morse Code to text.

    Args:
        morse (str): The Morse Code to convert.
        morse_dict (dict): The Morse Code dictionary to use.

    Returns:
        str: The converted text.
    """
    if not morse:
        return ""

    morse_dict_reversed = {v: k for k, v in morse_dict.items()}
    valid_codes = set(morse_dict_reversed.keys())
    text = []
    invalid_codes = []

    for code in morse.split(' '):
        if code in valid_codes:
            text.append(morse_dict_reversed[code])
        else:
            invalid_codes.append(code)

    if invalid_codes:
        logging.error(f"Invalid Morse Code sequences: {invalid_codes}")
        raise ValueError(f"Invalid Morse Code sequences: {invalid_codes}")

    logging.info(f"Converted Morse Code to text: {morse} -> {''.join(text)}")
    return ''.join(text)

@click.command()
@click.argument('text', required=False)
@click.option('--reverse', is_flag=True, help="Convert Morse Code to text.")
@click.option('--save', type=click.Path(), help="Save the output to a file.")
@click.option('--read', type=click.Path(), help="Read input from a file.")
@click.option('--custom-dict', type=click.Path(), help="Path to a custom Morse Code dictionary file.")
def main(text, reverse, save, read, custom_dict):
    """
    Command line tool to convert text to Morse Code and vice versa.

    Args:
        text (str): The text to convert.
        reverse (bool): Flag to indicate conversion from Morse Code to text.
        save (str): Path to save the output to a file.
        read (str): Path to read input from a file.
        custom_dict (str): Path to a custom Morse Code dictionary file.
    """
    try:
        morse_dict = data.MORSE_CODE_DICT
        if custom_dict:
            morse_dict = load_custom_dict(custom_dict)

        if read:
            with open(read, 'r') as file:
                text = file.read().strip()
            logging.info(f"Read input from file: {read}")

        if text is None:
            click.echo(Fore.RED + "No input text provided.")
            return

        if reverse:
            result = morse_to_text(text, morse_dict)
        else:
            result = text_to_morse(text, morse_dict)

        if save:
            with open(save, 'w') as file:
                file.write(result)
            logging.info(f"Output saved to file: {save}")
            click.echo(Fore.GREEN + f"Output saved to {save}")
        else:
            click.echo(Fore.GREEN + result)
    except FileNotFoundError:
        logging.error(f"File '{read}' not found.")
        click.echo(Fore.RED + f"File '{read}' not found.")
    except IOError as e:
        logging.error(f"File error: {e}")
        click.echo(Fore.RED + f"File error: {e}")
    except ValueError as e:
        logging.error(f"Error: {e}")
        click.echo(Fore.RED + f"Error: {e}")

if __name__ == '__main__':
    main()