# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings_ui.ui'
##
## Created by: Qt User Interface Compiler version 5.15.8
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore


class Ui_SettingsWindow(object):
    def setupUi(self, SettingsWindow):
        if not SettingsWindow.objectName():
            SettingsWindow.setObjectName("SettingsWindow")
        self.general_tab = QWidget()
        self.general_tab.setObjectName("general_tab")
        self.formLayout = QFormLayout(self.general_tab)
        self.formLayout.setObjectName("formLayout")
        self.vid_width_lb = QLabel(self.general_tab)
        self.vid_width_lb.setObjectName("vid_width_lb")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.vid_width_lb)

        self.graph_header_lb = QLabel(self.general_tab)
        self.graph_header_lb.setObjectName("graph_header_lb")

        self.formLayout.setWidget(3, QFormLayout.SpanningRole, self.graph_header_lb)

        self.vid_width_le = QLineEdit(self.general_tab)
        self.vid_width_le.setObjectName("vid_width_le")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.vid_width_le)

        self.window_size_lb = QLabel(self.general_tab)
        self.window_size_lb.setObjectName("window_size_lb")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.window_size_lb)

        self.window_size_le = QLineEdit(self.general_tab)
        self.window_size_le.setObjectName("window_size_le")

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.window_size_le)

        self.vid_header_lb = QLabel(self.general_tab)
        self.vid_header_lb.setObjectName("vid_header_lb")

        self.formLayout.setWidget(0, QFormLayout.SpanningRole, self.vid_header_lb)

        self.confirm_dbtn = QDialogButtonBox(self.general_tab)
        self.confirm_dbtn.setObjectName("confirm_dbtn")
        self.confirm_dbtn.setStandardButtons(
            QDialogButtonBox.Cancel | QDialogButtonBox.Ok
        )

        self.formLayout.setWidget(7, QFormLayout.FieldRole, self.confirm_dbtn)

        SettingsWindow.addTab(self.general_tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName("tab_2")
        SettingsWindow.addTab(self.tab_2, "")
        # if QT_CONFIG(shortcut)
        self.vid_width_lb.setBuddy(self.vid_width_le)
        self.window_size_lb.setBuddy(self.window_size_le)
        # endif // QT_CONFIG(shortcut)

        self.retranslateUi(SettingsWindow)

        QMetaObject.connectSlotsByName(SettingsWindow)

    # setupUi

    def retranslateUi(self, SettingsWindow):
        self.vid_width_lb.setText(
            QCoreApplication.translate("SettingsWindow", "Width", None)
        )
        self.graph_header_lb.setText(
            QCoreApplication.translate(
                "SettingsWindow",
                '<html><head/><body><p align="center"><span style=" font-weight:700;">Graph viewer</span></p></body></html>',
                None,
            )
        )
        self.window_size_lb.setText(
            QCoreApplication.translate("SettingsWindow", "Viewed seconds", None)
        )
        self.vid_header_lb.setText(
            QCoreApplication.translate(
                "SettingsWindow",
                '<html><head/><body><p align="center"><span style=" font-weight:700;">Video Player</span></p></body></html>',
                None,
            )
        )
        SettingsWindow.setTabText(
            SettingsWindow.indexOf(self.general_tab),
            QCoreApplication.translate("SettingsWindow", "General", None),
        )
        SettingsWindow.setTabText(
            SettingsWindow.indexOf(self.tab_2),
            QCoreApplication.translate("SettingsWindow", "Tab 2", None),
        )
        pass

    # retranslateUi
