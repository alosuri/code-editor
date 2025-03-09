from PySide6.QtWidgets import QTabWidget

class TabsWidget(QTabWidget):
    def __init__(self, opened_tabs: list) -> None:
        super(TabsWidget, self).__init__()
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.close)
        self.setMovable(True)
        self.opened_tabs = opened_tabs

    def close(self, index) -> None:
        self.opened_tabs.remove(self.opened_tabs[index])
        self.removeTab(index)