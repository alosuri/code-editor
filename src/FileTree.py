import os, sys
from PySide6.QtWidgets import QTreeView, QFileSystemModel
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt

from src.TextEditor import TextEditor

class FileTree(QTreeView):
    def __init__(self, main_window) -> None:
        super(FileTree, self).__init__()
        self.main_window = main_window
        self.opened_tabs = []
        self.populate()
        self.selectionModel().selectionChanged.connect(lambda: self.open_file(self.selectionModel().selectedIndexes()))

    def populate(self) -> None:
        path = "C:/Users/rafal/Documents/Programming/Python"
        self.model = CustomFileSystemModel()
        self.model.setRootPath(path)
        self.setModel(self.model)
        self.setRootIndex(self.model.index(path))
        self.setHeaderHidden(True)
        self.hideColumn(1)
        self.hideColumn(2)
        self.hideColumn(3)

    def open_file(self, selected_indexes) -> None:
        if selected_indexes:
            selected_index = selected_indexes[0]
            self.selected_item = self.model.filePath(selected_index)

            if os.path.isfile(self.selected_item) and self.selected_item not in self.opened_tabs:
                try:
                    with open(self.selected_item, 'r', encoding='utf-8') as file:
                        self.content = file.read()
                        self.text_editor = TextEditor()
                        self.text_editor.setPlainText(self.content)

                        self.main_window.tabs_widget.addTab(self.text_editor, os.path.basename(self.selected_item))
                        self.main_window.tabs_widget.setCurrentIndex(len(self.opened_tabs))
                        self.main_window.tabs_widget.setTabIcon(len(self.opened_tabs), QIcon("./ui/icons/file.png"))


                        self.opened_tabs.append(self.selected_item)

                except (UnicodeDecodeError, OSError):
                    print("Unsupported file type.")
                    return False
            elif self.selected_item in self.opened_tabs:
                self.main_window.tabs_widget.setCurrentIndex(self.opened_tabs.index(self.selected_item))

class CustomFileSystemModel(QFileSystemModel):
    def __init__(self) -> None:
        super(CustomFileSystemModel, self).__init__()
        self.folder_icon = QIcon("./ui/icons/folder.png")
        self.file_icon = QIcon("./ui/icons/file.png")

    def data(self, index, role) -> None:
        if role == Qt.ItemDataRole.DecorationRole:
            if index.isValid():
                file_info = self.fileInfo(index)
                if file_info.isDir():
                    return self.folder_icon
                else:
                    return self.file_icon
                    
        return super().data(index, role)