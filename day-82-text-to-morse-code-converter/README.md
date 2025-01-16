# Text to Morse Code Converter

## Description

The Text to Morse Code Converter is a command line tool that allows users to convert text to Morse Code and vice versa. It supports custom Morse Code dictionaries and can read input from files and save output to files.

## Features

- Convert text to Morse Code.
- Convert Morse Code to text.
- Support for custom Morse Code dictionaries.
- Read input from a file or command line.
- Save output to a file.
- Logging of conversion processes and errors.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/drayerh/text-to-morse-code-converter.git
    cd text-to-morse-code-converter
    ```

2. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

### Basic Usage

To convert text to Morse Code:
```sh
python main.py "Hello, World!"
```

To convert Morse Code to text:
```sh
python main.py --reverse ".... . .-.. .-.. ---"
```

### Reading Input from a File

To read input from a file:
```sh
python main.py --read input.txt
```

### Saving Output to a File

To save the output to a file:
```sh
python main.py "Hello, World!" --save output.txt
```

### Using a Custom Morse Code Dictionary

To use a custom Morse Code dictionary:
```sh
python main.py "Hello, World!" --custom-dict custom_dict.json
```

### Full Command Line Options

```sh
Usage: main.py [OPTIONS] [TEXT]

  Command line tool to convert text to Morse Code and vice versa.

Options:
  --reverse         Convert Morse Code to text.
  --save PATH       Save the output to a file.
  --read PATH       Read input from a file.
  --custom-dict PATH  Path to a custom Morse Code dictionary file.
  --help            Show this message and exit.
```

## Logging

The tool logs conversion processes and errors. Logs are saved to `error.log` for errors and displayed in the console for general information.

## Example

### Converting Text to Morse Code

```sh
python main.py "HELLO WORLD"
```

Output:
```
.... . .-.. .-.. --- / .-- --- .-. .-.. -..
```

### Converting Morse Code to Text

```sh
python main.py --reverse ".... . .-.. .-.. --- / .-- --- .-. .-.. -.."
```

Output:
```
HELLO WORLD
```

## Custom Morse Code Dictionary

You can create a custom Morse Code dictionary in JSON format. For example:

`custom_dict.json`:
```json
{
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "1": ".----",
    "2": "..---"
}
```

Use the custom dictionary with the `--custom-dict` option:
```sh
python main.py "ABC 12" --custom-dict custom_dict.json
```

## Error Handling

The tool handles various errors such as invalid characters in the input text or Morse Code sequences. Errors are logged and displayed to the user.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on GitHub.

## Contact

For any questions or feedback, please contact pythontutorlabs@gmail.com.