import tkinter as tk
from tkinter import messagebox
import time

class TypingSpeedTestApp:
    """
    A class to represent a typing speed test application.
    """

    def __init__(self, root):
        """
        Initialize the TypingSpeedTestApp with the given root window.

        Parameters:
        root (tk.Tk): The root window of the Tkinter application.
        """
        self.root = root
        self.root.title("Typing Speed Test")
        self.root.geometry("800x400")

        self.sample_text = "The quick brown fox jumps over the lazy dog."
        self.start_time = None
        self.end_time = None
        self.timer_running = False

        self.setup_gui()

    def setup_gui(self):
        """
        Set up the graphical user interface for the typing speed test application.
        """
        self.instructions_label = tk.Label(self.root, text="Type the following text as quickly as you can:")
        self.instructions_label.pack(pady=10)

        self.sample_text_label = tk.Label(self.root, text=self.sample_text, wraplength=700)
        self.sample_text_label.pack(pady=10)

        self.text_box = tk.Text(self.root, height=10, width=80)
        self.text_box.pack(pady=10)
        self.text_box.bind("<KeyPress>", self.start_test)
        self.text_box.bind("<KeyRelease>", self.update_typing_speed)
        self.text_box.bind("<Return>", self.check_completion)

        self.start_button = tk.Button(self.root, text="Start", command=self.start_test)
        self.start_button.pack(pady=5)

        self.reset_button = tk.Button(self.root, text="Reset", command=self.reset_test)
        self.reset_button.pack(pady=5)

        self.result_label = tk.Label(self.root, text="")
        self.result_label.pack(pady=10)

        self.timer_label = tk.Label(self.root, text="Time: 0.00 seconds")
        self.timer_label.pack(pady=10)

        self.accuracy_label = tk.Label(self.root, text="Accuracy: 0.00%")
        self.accuracy_label.pack(pady=10)

        self.errors_label = tk.Label(self.root, text="Errors: 0")
        self.errors_label.pack(pady=10)

        self.typing_speed_label = tk.Label(self.root, text="Typing Speed: 0.00 WPM")
        self.typing_speed_label.pack(pady=10)

        self.add_button = tk.Button(self.root, text="Add", command=self.check_completion)
        self.add_button.pack(pady=5)

    def start_test(self, event=None):
        """
        Start the typing test and the timer when the user begins typing.

        Parameters:
        event (tk.Event): The event that triggered the method (default is None).
        """
        if not self.start_time:
            self.start_time = time.time()
            self.timer_running = True
            self.update_timer()
            self.text_box.bind("<space>", self.check_completion)
            self.text_box.bind("<Return>", self.check_completion)

    def update_timer(self):
        """
        Update the timer label with the elapsed time since the test started.
        """
        if self.timer_running:
            elapsed_time = time.time() - self.start_time
            self.timer_label.config(text=f"Time: {elapsed_time:.2f} seconds")
            self.root.after(100, self.update_timer)

    def update_typing_speed(self, event=None):
        """
        Update the typing speed label in real-time as the user types.

        Parameters:
        event (tk.Event): The event that triggered the method (default is None).
        """
        if self.start_time:
            elapsed_time = time.time() - self.start_time
            typed_text = self.text_box.get("1.0", tk.END).strip()
            words_typed = len(typed_text.split())
            wpm = (words_typed / elapsed_time) * 60 if elapsed_time > 0 else 0
            self.typing_speed_label.config(text=f"Typing Speed: {wpm:.2f} WPM")

    def check_completion(self, event=None):
        """
        Check if the user has completed typing the sample text.

        Parameters:
        event (tk.Event): The event that triggered the method (default is None).
        """
        typed_text = self.text_box.get("1.0", tk.END).strip()
        if typed_text == self.sample_text or event.keysym == "Return":
            self.end_time = time.time()
            self.timer_running = False
            self.calculate_wpm()
            self.calculate_accuracy(typed_text)
            self.calculate_errors(typed_text)
            self.text_box.unbind("<space>")
            self.text_box.unbind("<Return>")

    def calculate_wpm(self):
        """
        Calculate and display the user's typing speed in words per minute.
        """
        time_taken = self.end_time - self.start_time
        words_typed = len(self.sample_text.split())
        wpm = (words_typed / time_taken) * 60
        self.result_label.config(text=f"Your typing speed is {wpm:.2f} words per minute.")

    def calculate_accuracy(self, typed_text):
        """
        Calculate and display the user's typing accuracy as a percentage.

        Parameters:
        typed_text (str): The text typed by the user.
        """
        correct_chars = sum(1 for a, b in zip(typed_text, self.sample_text) if a == b)
        accuracy = (correct_chars / len(self.sample_text)) * 100
        self.accuracy_label.config(text=f"Accuracy: {accuracy:.2f}%")

    def calculate_errors(self, typed_text):
        """
        Calculate and display the number of typing errors made by the user.

        Parameters:
        typed_text (str): The text typed by the user.
        """
        errors = sum(1 for a, b in zip(typed_text, self.sample_text) if a != b)
        self.errors_label.config(text=f"Errors: {errors}")

    def reset_test(self):
        """
        Reset the typing test to its initial state.
        """
        self.start_time = None
        self.end_time = None
        self.timer_running = False
        self.text_box.delete("1.0", tk.END)
        self.result_label.config(text="")
        self.timer_label.config(text="Time: 0.00 seconds")
        self.accuracy_label.config(text="Accuracy: 0.00%")
        self.errors_label.config(text="Errors: 0")
        self.typing_speed_label.config(text="Typing Speed: 0.00 WPM")

if __name__ == "__main__":
    root = tk.Tk()
    app = TypingSpeedTestApp(root)
    root.mainloop()