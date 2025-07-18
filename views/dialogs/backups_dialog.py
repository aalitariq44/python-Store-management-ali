# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QListWidget, QPushButton, QMessageBox
from controllers.backup_controller import BackupController

class BackupsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("النسخ الاحتياطية")
        self.setModal(True)
        self.controller = BackupController()
        
        self.layout = QVBoxLayout(self)
        
        self.list_widget = QListWidget()
        self.layout.addWidget(self.list_widget)
        
        self.refresh_button = QPushButton("تحديث")
        self.refresh_button.clicked.connect(self.load_backups)
        self.layout.addWidget(self.refresh_button)
        
        self.load_backups()
        
    def load_backups(self):
        self.list_widget.clear()
        backups = self.controller.list_backups()
        if backups:
            for backup in backups:
                self.list_widget.addItem(backup['name'])
        else:
            QMessageBox.information(self, "معلومات", "لا توجد نسخ احتياطية متاحة.")
