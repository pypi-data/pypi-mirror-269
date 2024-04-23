from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from PySide6.QtCore import Qt
from PySide6.QtGui import QShortcut
from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget

from behavysis_viewer.ui.settings_ui import Ui_SettingsWindow
from behavysis_viewer.windows.window_mixin import WindowMixin

if TYPE_CHECKING:
    from behavysis_viewer.windows.main import MainWindow


class SettingsWindow(QTabWidget, WindowMixin):

    ui: Ui_SettingsWindow
    main: MainWindow

    def __init__(self, main: MainWindow, *args, **kwargs):
        # Instatiating QMainWindow
        super().__init__(*args, **kwargs)

        # Linking reference to main window
        self.main = main

        # Connecting main window with UI (from Qt-Designer)
        self.ui = Ui_SettingsWindow()
        self.ui.setupUi(self)

        # Setting window flags
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

        # Connecting signals and slots
        self._init_conns()

    def _init_conns(self):
        # SIGNALS AND SLOTS: PREFERENCES
        # Save signals
        self.ui.confirm_dbtn.accepted.connect(self.save)
        QShortcut(Qt.Key.Key_Return, self).activated.connect(self.save)
        # Cancel signals
        self.ui.confirm_dbtn.rejected.connect(self.cancel)
        QShortcut(Qt.Key.Key_Escape, self).activated.connect(self.cancel)
        QShortcut(Qt.Key.Key_P, self).activated.connect(self.cancel)

    def cancel(self):
        self.toggle_window(self)

    def save(self):
        self.set_vid_size()
        self.set_window_size()

    def set_vid_size(self):
        width_str = self.ui.vid_width_le.text()
        if width_str.isnumeric():
            width = int(width_str)
            height = int(width * 2 / 3)
            # Setting new vid_viewer and plot_viewer dimensions
            self.main.resize_viewer(width, height)

    def set_window_size(self):
        window_size_str = self.ui.window_size_le.text()
        if window_size_str.isnumeric():
            self.main.window_size = int(int(window_size_str) * self.main.vid_model.fps)
            self.main.update_frame_plot()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = SettingsWindow(QMainWindow())
    window.show()

    sys.exit(app.exec())
