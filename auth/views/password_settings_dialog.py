# -*- coding: utf-8 -*-
"""
شاشة إعدادات تغيير كلمة المرور
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, QFrame,
                             QWidget, QGroupBox)
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
        self.setFixedSize(500, 450)
        self.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint)
        
        # التخطيط الرئيسي
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # إطار المحتوى
        content_frame = QFrame()
        content_frame.setFrameStyle(QFrame.Box)
        content_frame.setStyleSheet("""
            QFrame {
                border: 2px solid #f39c12;
                border-radius: 10px;
                background-color: #f8f9fa;
                padding: 20px;
            }
        """)
        
        content_layout = QVBoxLayout(content_frame)
        content_layout.setSpacing(20)
        
        # عنوان النافذة
        title_label = QLabel("إعدادات كلمة المرور")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50; border: none; padding: 10px;")
        content_layout.addWidget(title_label)
        
        # مجموعة تغيير كلمة المرور
        password_group = QGroupBox("تغيير كلمة المرور")
        password_group.setFont(QFont("Arial", 12, QFont.Bold))
        password_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 10px 0 10px;
                color: #34495e;
            }
        """)
        
        password_layout = QVBoxLayout(password_group)
        password_layout.setSpacing(15)
        
        # حقل كلمة المرور القديمة
        old_password_layout = QVBoxLayout()
        old_password_label = QLabel("كلمة المرور الحالية:")
        old_password_label.setFont(QFont("Arial", 10))
        old_password_label.setStyleSheet("color: #34495e; border: none;")
        old_password_layout.addWidget(old_password_label)
        
        self.old_password_input = QLineEdit()
        self.old_password_input.setEchoMode(QLineEdit.Password)
        self.old_password_input.setPlaceholderText("أدخل كلمة المرور الحالية...")
        self.old_password_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                font-size: 12px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #f39c12;
            }
        """)
        old_password_layout.addWidget(self.old_password_input)
        
        password_layout.addLayout(old_password_layout)
        
        # حقل كلمة المرور الجديدة
        new_password_layout = QVBoxLayout()
        new_password_label = QLabel("كلمة المرور الجديدة:")
        new_password_label.setFont(QFont("Arial", 10))
        new_password_label.setStyleSheet("color: #34495e; border: none;")
        new_password_layout.addWidget(new_password_label)
        
        self.new_password_input = QLineEdit()
        self.new_password_input.setEchoMode(QLineEdit.Password)
        self.new_password_input.setPlaceholderText("أدخل كلمة المرور الجديدة...")
        self.new_password_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                font-size: 12px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #f39c12;
            }
        """)
        new_password_layout.addWidget(self.new_password_input)
        
        password_layout.addLayout(new_password_layout)
        
        # حقل تأكيد كلمة المرور الجديدة
        confirm_password_layout = QVBoxLayout()
        confirm_password_label = QLabel("تأكيد كلمة المرور الجديدة:")
        confirm_password_label.setFont(QFont("Arial", 10))
        confirm_password_label.setStyleSheet("color: #34495e; border: none;")
        confirm_password_layout.addWidget(confirm_password_label)
        
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setPlaceholderText("أعد إدخال كلمة المرور الجديدة...")
        self.confirm_password_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                font-size: 12px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #f39c12;
            }
        """)
        self.confirm_password_input.returnPressed.connect(self.change_password)
        confirm_password_layout.addWidget(self.confirm_password_input)
        
        password_layout.addLayout(confirm_password_layout)
        
        content_layout.addWidget(password_group)
        
        # مساحة فارغة
        content_layout.addWidget(QWidget())
        
        # أزرار التحكم
        buttons_layout = QHBoxLayout()
        
        # زر حفظ التغييرات
        self.save_button = QPushButton("حفظ التغييرات")
        self.save_button.setFont(QFont("Arial", 10, QFont.Bold))
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #f39c12;
                color: white;
                border: none;
                padding: 12px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e67e22;
            }
            QPushButton:pressed {
                background-color: #d35400;
            }
        """)
        self.save_button.clicked.connect(self.change_password)
        buttons_layout.addWidget(self.save_button)
        
        # زر الإلغاء
        cancel_button = QPushButton("إلغاء")
        cancel_button.setFont(QFont("Arial", 10))
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                padding: 12px 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
            QPushButton:pressed {
                background-color: #6c7b7d;
            }
        """)
        cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_button)
        
        content_layout.addLayout(buttons_layout)
        
        main_layout.addWidget(content_frame)
        self.setLayout(main_layout)
        
        # تركيز على الحقل الأول
        self.old_password_input.setFocus()
    
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
