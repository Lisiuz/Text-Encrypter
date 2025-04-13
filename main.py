import sys
import hashlib
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                               QLineEdit, QPushButton, QTextEdit, QLabel, QComboBox, QHBoxLayout, QInputDialog)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor


def encrypt_text(text):
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


def cesare_enc(text, sliding):

    ces_enc = ""
    for c in text:
        ces_enc += chr(ord(c) + int(sliding))
    return ces_enc


def cesare_dec(text, sliding):

    ces_dec = ""
    for c in text:
        ces_dec += chr(ord(c) - int(sliding))
    return ces_dec


def cesare_enc11(text):
    ces_enc = ""
    for c in text:
        ces_enc += chr(ord(c) + 11)
    return ces_enc


def cesare_dec11(text):
    ces_dec = ""
    for c in text:
        ces_dec += chr(ord(c) - 11)
    return ces_dec


def hash_enc(text):
    res = hash(text)
    return res


def hash_dec(text):
    return "Non è possibile decodificare l'algoritmo di HASH"


def sha256_enc(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def sha256_dec(text):
    return "Non è possibile decodificare l'algoritmo SHA256"


def ascii_enc(text):
    res = ""
    for c in text:
        res += str(ord(c)) + " "
    return res


def ascii_dec(text):

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
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Text Encrypter/Decrypter")
        self.input_label = QLabel("Chiave cifratura:")
        self.input_label.setStyleSheet("font-size: 16px; color: #CFD8DC;")
        self.menu_tendina = QComboBox()
        self.menu_tendina.addItem("LukeEncrypt")
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
        text = self.input_text.text()
        if text:
            if self.menu_tendina.currentText() == "LukeEncrypt":
                encrypted_text = encrypt_text(text)
            elif self.menu_tendina.currentText() == "Caesar Cipher":
                sliding, ok = QInputDialog.getInt(self, "Quanti scostamenti di Caesar Cypher",
                                                  "Inserisci il numero di scostamenti per Caesar Cypher (1-22): ", 3, 1, 22)
                if ok:
                    encrypted_text = cesare_enc(text,  sliding)
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
        text = self.input_text.text()
        if text:
            if self.menu_tendina.currentText() == "LukeEncrypt":
                decrypted_text = decrypt_text(text)
            elif self.menu_tendina.currentText() == "Caesar Cipher":
                sliding, ok = QInputDialog.getInt(self, "Quanti scostamenti di Caesar Cypher",
                                                  "Inserisci il numero di scostamenti per Caesar Cypher (1-22): ", 3, 1, 22)
                if ok:
                    decrypted_text = cesare_dec(text, sliding)
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
