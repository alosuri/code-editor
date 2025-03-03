import sys, os
from PySide6 import QtWidgets, QtCore
from main_window import Ui_MainWindow

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.populate()
        self.current_file = ""
        self.opened_tabs = []

        self.treeView.selectionModel().selectionChanged.connect(lambda: self.open_file())

    def populate(self):
        path = "C:/Windows"
        self.model = QtWidgets.QFileSystemModel()
        self.model.setRootPath((QtCore.QDir.rootPath()))
        self.treeView.setModel(self.model)
        self.treeView.setRootIndex(self.model.index(path))
        self.treeView.setSortingEnabled(True)
        for x in range(1, self.model.columnCount()):
            self.treeView.hideColumn(x)

    def open_file(self):
        selected_indexes  = self.treeView.selectionModel().selectedIndexes()
        if selected_indexes:
            selected_index = selected_indexes[0]
            selected_item = self.model.filePath(selected_index)
            if (os.path.isfile(selected_item)) & (selected_item not in self.opened_tabs):
                with open(selected_item) as f:
                    self.opened_tabs.append(selected_item)
                    self.current_file = f.read()
                    self.textEdit = QtWidgets.QTextEdit()
                    self.textEdit.setText(self.current_file)
                    self.tabWidget.addTab(self.textEdit, str(self.model.fileName(selected_index)))
                    self.tabWidget.setCurrentIndex(len(self.opened_tabs))



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()