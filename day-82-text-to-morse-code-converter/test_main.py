import unittest
from main import text_to_morse, morse_to_text
import data

class TestMorseCodeConverter(unittest.TestCase):
    """
    Unit tests for the Morse Code converter functions.
    """

    def setUp(self):
        """
        Set up the Morse Code dictionary for use in tests.
        """
        self.morse_dict = data.MORSE_CODE_DICT

    def test_text_to_morse(self):
        """
        Test the text_to_morse function with various inputs.
        """
        self.assertEqual(text_to_morse("HELLO", self.morse_dict), ".... . .-.. .-.. ---")
        self.assertEqual(text_to_morse("WORLD", self.morse_dict), ".-- --- .-. .-.. -..")
        self.assertEqual(text_to_morse("123", self.morse_dict), ".---- ..--- ...--")
        self.assertEqual(text_to_morse("SOS", self.morse_dict), "... --- ...")
        self.assertEqual(text_to_morse("", self.morse_dict), "")

    def test_morse_to_text(self):
        """
        Test the morse_to_text function with various inputs.
        """
        self.assertEqual(morse_to_text(".... . .-.. .-.. ---", self.morse_dict), "HELLO")
        self.assertEqual(morse_to_text(".-- --- .-. .-.. -..", self.morse_dict), "WORLD")
        self.assertEqual(morse_to_text(".---- ..--- ...--", self.morse_dict), "123")
        self.assertEqual(morse_to_text("... --- ...", self.morse_dict), "SOS")
        self.assertEqual(morse_to_text("", self.morse_dict), "")

    def test_invalid_text_to_morse(self):
        """
        Test the text_to_morse function with invalid input.
        """
        with self.assertRaises(ValueError):
            text_to_morse("HELLO@", self.morse_dict)

    def test_invalid_morse_to_text(self):
        """
        Test the morse_to_text function with invalid input.
        """
        with self.assertRaises(ValueError):
            morse_to_text(".... . .-.. .-.. --- @", self.morse_dict)

if __name__ == '__main__':
    unittest.main()