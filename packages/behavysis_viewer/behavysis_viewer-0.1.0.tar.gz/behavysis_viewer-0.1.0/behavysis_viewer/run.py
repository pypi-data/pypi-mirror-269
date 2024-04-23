import sys

from PySide6.QtWidgets import QApplication

from behavysis_viewer.windows.main import MainWindow

if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    window.open(
        # r"Z:\PRJ-BowenLab\TimLee\resources\neda_project\0_configs\608DVR_CH1_5_9_65_20240403112644.json"
        r"z:\PRJ-BowenLab\TimLee\resources\project_ma\0_configs\2_Round1.1_20220530_AGG-MOA_test3-M3_a2.json"
    )

    # window.export_vid("example.mp4")

    sys.exit(app.exec())
