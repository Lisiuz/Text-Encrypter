"""
MIT License

Copyright (c) 2025 Luca Lisiari

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
Text Encryptor/Decryptor Application -  Learn Python with Projects

A GUI application that provides multiple encryption and decryption algorithms including:
- Custom Demo Encryption
- Caesar Cipher
- ASCII encoding
- HASH Algorithm
- SHA256

The application features a modern UI with Material Design-inspired styling.
"""
import sys
import hashlib
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                               QLineEdit, QPushButton, QTextEdit, QLabel, QComboBox, QHBoxLayout, QInputDialog)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor


def encrypt_text(text):
    """
    Encrypts text using a custom algorithm.

    The encryption process:
    1. For each word longer than 2 characters:
       - Takes the first character
       - Takes the last character
       - Takes characters from index 2 to second-to-last
       - Takes the second character
       - Combines them in this order: first + last + middle + second
    2. Converts the first character of each word to its ASCII code
    3. Joins all words with spaces

    Args:
        text (str): The input text to encrypt
        Returns:
        str: The encrypted text, or empty string if input is empty
    """
    res = ""
    if text:
        for word in text.split():
            if len(word) > 2:
                res += word[0] + word[-1] + word[2:-1] + word[1] + " "
            else:
                res += word + " "
        text = ""
        for word in res.split():
            ascii_char = str(ord(word[0]))
            text += ascii_char + word[1:] + " "
        return text[0:-1]
    else:
        return ""


def decrypt_text(text):
    """
    Decrypts text that was encrypted with the custom encrypt_text algorithm.
    """
    res = ""
    if text:
        for word in text.split():
            try:
                ascii_code = ""
                i = 0
                while i < len(word) and word[i].isdigit():
                    ascii_code += word[i]
                    i += 1

                if ascii_code:
                    first_char = chr(int(ascii_code))
                    modified_word = first_char + word[i:]

                    if len(modified_word) > 2:
                        original_word = modified_word[0] + modified_word[-1] + \
                            modified_word[2:-1] + modified_word[1]
                        res += original_word + " "
                    else:
                        res += modified_word + " "
                else:
                    res += word + " "
            except ValueError:
                return "Invalid input: Could not decrypt"
        return res[0:-1]
    else:
        return ""


def cesare_enc(text, shifting):
    """
    Encrypts text using Caesar Cipher algorithm with custom shift.
    """
    ces_enc = ""
    for c in text:
        ces_enc += chr(ord(c) + int(shifting))
    return ces_enc


def cesare_dec(text, shifting):
    """
    Decrypts text using Caesar Cipher algorithm with custom shift.
    """
    ces_dec = ""
    for c in text:
        ces_dec += chr(ord(c) - int(shifting))
    return ces_dec


def hash_enc(text):
    res = hash(text)
    return res


def hash_dec(text):
    return "Non è possibile decodificare l'algoritmo di HASH"


"""
    Encrypts text using SHA-256 cryptographic hash function.

    Args:
        text (str): The text to hash

    Returns:
        str: The SHA-256 hash as a hexadecimal string
    """


def sha256_enc(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def sha256_dec(text):
    return "Non è possibile decodificare l'algoritmo SHA256"


def ascii_enc(text):
    """
    Encodes text to ASCII code points separated by spaces.
    """
    res = ""
    for c in text:
        res += str(ord(c)) + " "
    return res


def ascii_dec(text):
    """
    Decodes text from ASCII code points to characters.
    """
    res = ""
    txt_lst = text.split()
    for i in txt_lst:
        try:
            if int(i).is_integer():
                res += str(chr(int(i)))
        except:
            return "Errore: ASCII Decode richiede una serie di numeri interi"
    return res


class MainWindow(QWidget):
    """
    Main application window for the Text Encryptor/Decryptor.

    Provides a GUI interface with:
    - Algorithm selection dropdown
    - Text input field
    - Encrypt/Decrypt buttons
    - Results display
    """

    def __init__(self):
        """Initialize the main window and UI components."""
        super().__init__()

        self.setWindowTitle("Text Encrypter/Decrypter")
        self.input_label = QLabel("Algoritmo cifratura:")
        self.input_label.setStyleSheet("font-size: 16px; color: #CFD8DC;")
        self.menu_tendina = QComboBox()
        self.menu_tendina.addItem("DemoEncrypt")
        self.menu_tendina.addItem("Caesar Cipher")
        self.menu_tendina.addItem("ASCII")
        self.menu_tendina.addItem("HASH Algorithm")
        self.menu_tendina.addItem("SHA256")

        self.hbox_layout = QHBoxLayout()  # Created QHBoxLayout
        self.hbox_layout.addWidget(self.input_label)
        self.hbox_layout.addWidget(self.menu_tendina)
        self.hbox_layout.setContentsMargins(10, 10, 5, 10)

        self.input_text = QLineEdit()
        self.input_text.setPlaceholderText("Inserisci il testo da cifrare")
        self.input_text.setFixedHeight(50)
        self.input_text.setStyleSheet("font-size: 18px; color: #CFD8DC;")

        self.encrypt_button = QPushButton("Encrypt Text")
        self.decrypt_button = QPushButton("Decrypt Text")

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.addLayout(self.hbox_layout)
        layout.addWidget(self.input_text)
        layout.addWidget(self.encrypt_button)
        layout.addWidget(self.decrypt_button)
        layout.addWidget(self.output_text)

        self.setLayout(layout)

        self.encrypt_button.clicked.connect(self.on_encrypt_clicked)
        self.decrypt_button.clicked.connect(self.on_decrypt_clicked)

    def on_encrypt_clicked(self):
        """
        Handle encrypt button click event.

        Encrypts the input text using the selected algorithm and displays the result.
        For Caesar Cipher, prompts user for shift amount.
        """
        text = self.input_text.text()
        if text:
            if self.menu_tendina.currentText() == "DemoEncrypt":
                encrypted_text = encrypt_text(text)
            elif self.menu_tendina.currentText() == "Caesar Cipher":
                shifting, ok = QInputDialog.getInt(self, "Quanti scostamenti di Caesar Cypher",
                                                   "Inserisci il numero di scostamenti per Caesar Cypher (1-22): ", 3, 1, 22)

                if ok:
                    encrypted_text = cesare_enc(text, shifting)
                else:
                    encrypted_text = "Seleziona un algoritmo di cifratura"
            elif self.menu_tendina.currentText() == "HASH Algorithm":
                encrypted_text = hash_enc(text)
            elif self.menu_tendina.currentText() == "SHA256":
                encrypted_text = sha256_enc(text)
            elif self.menu_tendina.currentText() == "ASCII":
                encrypted_text = ascii_enc(text)
            self.output_text.setText(str(encrypted_text))

    def on_decrypt_clicked(self):
        """
        Handle decrypt button click event.

        Decrypts the input text using the selected algorithm and displays the result.
        For Caesar Cipher, prompts user for shift amount.
        """
        text = self.input_text.text()
        if text:
            if self.menu_tendina.currentText() == "DemoEncrypt":
                decrypted_text = decrypt_text(text)
            elif self.menu_tendina.currentText() == "Caesar Cipher":
                shifting, ok = QInputDialog.getInt(self, "Quanti scostamenti di Caesar Cypher",
                                                   "Inserisci il numero di scostamenti per Caesar Cypher (1-22): ", 3, 1, 22)
                if ok:
                    decrypted_text = cesare_dec(text, shifting)
                else:
                    decrypted_text = "Seleziona un algoritmo di cifratura"
            elif self.menu_tendina.currentText() == "HASH Algorithm":
                decrypted_text = hash_dec(text)
            elif self.menu_tendina.currentText() == "SHA256":
                decrypted_text = sha256_dec(text)
            elif self.menu_tendina.currentText() == "ASCII":
                decrypted_text = ascii_dec(text)
            self.output_text.setText(str(decrypted_text))


if __name__ == "__main__":
    """
    Entry point for the application.

    Initializes the QApplication, sets up the color palette and styling,
    creates and shows the main window, and starts the event loop.
    """
    app = QApplication(sys.argv)

    # Material Design Color Palette
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(
        "#455A64"))  # Very Dark Background
    palette.setColor(QPalette.ColorRole.WindowText, QColor(
        "#CFD8DC"))  # Lighter Text on Dark Background
    palette.setColor(QPalette.ColorRole.Base, QColor(
        "#607D8B"))  # Input Field Background
    palette.setColor(QPalette.ColorRole.Text,
                     QColor("#CFD8DC"))  # Input Field Text
    palette.setColor(QPalette.ColorRole.Button, QColor(
        "#546E7A"))  # Darker Button Background
    palette.setColor(QPalette.ColorRole.ButtonText,
                     QColor("#FFFFFF"))  # Button Text
    app.setPalette(palette)

    # Style Application
    app.setStyleSheet("""
        QPushButton {
            padding: 15px;
            border-radius: 10px;
            font-size: 18px;
            background-color: #8BC34A;
            color: white;
        }
        QPushButton:hover {
            background-color: #689F38;
            font-size: 20px;
        }
            QLineEdit {
                font-size: 18px;
                border: 1px solid #7986CB;
                border-radius: 5px;
                padding: 5px;
                font-family: 'Arial';
                color: #CFD8DC;
            }
            QLineEdit::placeholder {
                color: #90A4AE;
            }
            QTextEdit {
                font-size: 18px;
                border: 1px solid #7986CB;
                border-radius: 5px;
                padding: 5px;
                font-family: 'Arial';
            }
        """)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
