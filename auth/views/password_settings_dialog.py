# -*- coding: utf-8 -*-
"""
شاشة إعدادات تغيير كلمة المرور
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, QWidget)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from auth.controllers.auth_controller import AuthController


class PasswordSettingsDialog(QDialog):
    """
    نافذة إعدادات كلمة المرور
    """
    
    # إشارة لإرسال حالة تغيير كلمة المرور
    password_changed = pyqtSignal()
    
    def __init__(self, auth_controller: AuthController, parent=None):
        """
        تهيئة نافذة إعدادات كلمة المرور
        
        Args:
            auth_controller: كنترولر التسجيل
            parent: النافذة الأب
        """
        super().__init__(parent)
        self.auth_controller = auth_controller
        self.setup_ui()
        self.setModal(True)
    
    def setup_ui(self):
        """
        إعداد واجهة المستخدم
        """
        self.setWindowTitle("إعدادات كلمة المرور - نظام إدارة المتجر")
        self.setFixedSize(600, 550)  # زيادة حجم النافذة
        self.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)

        # التخطيط الرئيسي
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(25)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setAlignment(Qt.AlignCenter)

        # عنوان النافذة
        title_label = QLabel("تغيير كلمة المرور")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 22, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50; padding-bottom: 10px;")
        main_layout.addWidget(title_label)

        # مجموعة حقول كلمة المرور
        fields_layout = QVBoxLayout()
        fields_layout.setSpacing(20)

        # حقل كلمة المرور القديمة
        self.old_password_input = QLineEdit()
        self.old_password_input.setEchoMode(QLineEdit.Password)
        self.old_password_input.setPlaceholderText("كلمة المرور الحالية")
        fields_layout.addWidget(self.create_password_field(
            "كلمة المرور الحالية:", self.old_password_input
        ))

        # حقل كلمة المرور الجديدة
        self.new_password_input = QLineEdit()
        self.new_password_input.setEchoMode(QLineEdit.Password)
        self.new_password_input.setPlaceholderText("كلمة المرور الجديدة")
        fields_layout.addWidget(self.create_password_field(
            "كلمة المرور الجديدة:", self.new_password_input
        ))

        # حقل تأكيد كلمة المرور الجديدة
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setPlaceholderText("تأكيد كلمة المرور الجديدة")
        self.confirm_password_input.returnPressed.connect(self.change_password)
        fields_layout.addWidget(self.create_password_field(
            "تأكيد كلمة المرور:", self.confirm_password_input
        ))

        main_layout.addLayout(fields_layout)
        main_layout.addStretch(1)

        # أزرار التحكم
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)
        
        # زر حفظ التغييرات
        self.save_button = QPushButton("حفظ التغييرات")
        self.save_button.clicked.connect(self.change_password)
        buttons_layout.addWidget(self.save_button)
        
        # زر الإلغاء
        cancel_button = QPushButton("إلغاء")
        cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_button)
        
        main_layout.addLayout(buttons_layout)

        # تطبيق الأنماط
        self.apply_styles()

        # تركيز على الحقل الأول
        self.old_password_input.setFocus()

    def create_password_field(self, label_text, line_edit):
        """
        إنشاء حقل إدخال كلمة المرور مع التسمية
        """
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        label = QLabel(label_text)
        label.setFont(QFont("Arial", 12))
        label.setStyleSheet("color: #34495e;")
        
        layout.addWidget(label)
        layout.addWidget(line_edit)
        
        return widget

    def apply_styles(self):
        """
        تطبيق الأنماط على الواجهة
        """
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
            }
            QLineEdit {
                background-color: white;
                border: 1px solid #ced4da;
                border-radius: 8px;
                padding: 12px 15px;
                font-size: 14px;
                color: #495057;
            }
            QLineEdit:focus {
                border-color: #f39c12;
                box-shadow: 0 0 0 3px rgba(243, 156, 18, 0.25);
            }
            QPushButton {
                border-radius: 8px;
                padding: 12px 25px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton#save_button {
                background-color: #f39c12;
                color: white;
            }
            QPushButton#save_button:hover {
                background-color: #e67e22;
            }
            QPushButton#save_button:pressed {
                background-color: #d35400;
            }
            QPushButton#cancel_button {
                background-color: #95a5a6;
                color: white;
            }
            QPushButton#cancel_button:hover {
                background-color: #7f8c8d;
            }
            QPushButton#cancel_button:pressed {
                background-color: #6c7b7d;
            }
        """)
        self.save_button.setObjectName("save_button")
        # Find the cancel button by its text and set its object name
        for button in self.findChildren(QPushButton):
            if button.text() == "إلغاء":
                button.setObjectName("cancel_button")
                break
    
    def change_password(self):
        """
        تغيير كلمة المرور
        """
        old_password = self.old_password_input.text().strip()
        new_password = self.new_password_input.text().strip()
        confirm_password = self.confirm_password_input.text().strip()
        
        if not old_password:
            QMessageBox.warning(self, "تحذير", "يرجى إدخال كلمة المرور الحالية")
            self.old_password_input.setFocus()
            return
        
        if not new_password:
            QMessageBox.warning(self, "تحذير", "يرجى إدخال كلمة المرور الجديدة")
            self.new_password_input.setFocus()
            return
        
        if not confirm_password:
            QMessageBox.warning(self, "تحذير", "يرجى تأكيد كلمة المرور الجديدة")
            self.confirm_password_input.setFocus()
            return
        
        # تغيير كلمة المرور
        success, message = self.auth_controller.change_password(old_password, new_password, confirm_password)
        
        if success:
            QMessageBox.information(self, "نجح", message)
            self.password_changed.emit()
            self.accept()
        else:
            QMessageBox.critical(self, "خطأ", message)
            # مسح الحقول وإعادة التركيز
            self.old_password_input.clear()
            self.new_password_input.clear()
            self.confirm_password_input.clear()
            self.old_password_input.setFocus()
    
    def keyPressEvent(self, event):
        """
        التعامل مع ضغط المفاتيح
        """
        if event.key() == Qt.Key_Escape:
            self.reject()
        else:
            super().keyPressEvent(event)
