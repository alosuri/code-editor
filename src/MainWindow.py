import re
from PySide6.QtWidgets import QMainWindow, QHBoxLayout, QWidget
from src.FileTree import FileTree
from src.TabsWidget import TabsWidget

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.setWindowTitle("Code Editor")
        self.setFixedSize(1280, 720)

        # Initialization of widgets
        self.file_tree = FileTree(self)
        self.tabs_widget = TabsWidget(self.file_tree.opened_tabs)

        # Layout
        layout = QHBoxLayout()
        layout.addWidget(self.file_tree)
        layout.addWidget(self.tabs_widget)
        layout.setStretch(1,4)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.current_theme = "dark.qss"
        self.load_theme(self.current_theme)

    def load_theme(self, theme_name) -> None:
        base_qss = self.load_qss("./ui/themes/base.qss")
        theme_qss = self.load_qss(f"./ui/themes/{theme_name}")

        final_qss = self.replace_colors(base_qss, theme_qss)

        self.setStyleSheet(final_qss)


    def load_qss(self, qss_file) -> str:
        with open(qss_file, 'r', encoding='utf-8') as file:
            return file.read()

    def replace_colors(self, base_qss, theme_qss):
        theme_colors = {}

        lines = theme_qss.splitlines()
        for line in lines:
            if line.strip().startswith('@'):
                parts = line.split(':', 1)
                if len(parts) != 2:
                    continue
                key, value = parts
                key = key.strip().lstrip('@')
                value = value.strip().rstrip(';')
                theme_colors[key] = value

        for key, value in theme_colors.items():
            pattern = rf"@{re.escape(key)}\b"
            if re.search(pattern, base_qss):
                base_qss = re.sub(pattern, value, base_qss)
                
        return base_qss

    def switch_theme(self) -> None:
        self.current_theme = 'light.qss' if self.current_theme == 'dark.qss' else 'dark.qss'
        self.load_theme(self.current_theme)
