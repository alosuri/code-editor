from PySide6.QtWidgets import QPlainTextEdit


class TextEditor(QPlainTextEdit):
    def __init__(self) -> None:
        super(TextEditor, self).__init__()