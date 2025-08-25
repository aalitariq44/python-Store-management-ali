# -*- coding: utf-8 -*-
"""
شاشة تسجيل الدخول
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, QFrame,
                             QWidget, QSizePolicy)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap, QIcon
from auth.controllers.auth_controller import AuthController


class LoginDialog(QDialog):
    """
    نافذة تسجيل الدخول
    """
    
    # إشارة لإرسال حالة تسجيل الدخول
    login_successful = pyqtSignal()
    
    def __init__(self, auth_controller: AuthController, parent=None):
        """
        تهيئة نافذة تسجيل الدخول
        
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
        self.setWindowTitle("تسجيل الدخول")
        self.setWindowIcon(QIcon("resources/icons/login.png"))
        self.setFixedWidth(500)
        self.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint | Qt.CustomizeWindowHint)

        # الأنماط
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
                border-radius: 15px;
            }
            QLabel {
                font-family: Arial;
                color: #34495e;
            }
            #password_label {
                font-size: 24px;
            }
            #title_label {
                font-size: 28px;
                font-weight: bold;
                color: #2c3e50;
                padding: 15px 0;
            }
            #password_input {
                background-color: white;
                border: 1px solid #ced4da;
                border-radius: 10px;
                padding: 15px 20px;
                font-size: 24px;
                min-height: 50px;
            }
            #password_input:focus {
                border-color: #80bdff;
            }
            QPushButton {
                border-radius: 10px;
                padding: 15px 25px;
                font-size: 24px;
                font-weight: bold;
                min-height: 50px;
            }
            #login_button {
                background-color: #007bff;
                color: white;
            }
            #login_button:hover {
                background-color: #0069d9;
            }
            #login_button:pressed {
                background-color: #0056b3;
            }
            #cancel_button {
                background-color: #6c757d;
                color: white;
            }
            #cancel_button:hover {
                background-color: #5a6268;
            }
            #cancel_button:pressed {
                background-color: #545b62;
            }
        """)

        # التخطيط الرئيسي
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(50, 50, 50, 50)
        main_layout.setSpacing(30)

        # عنوان النافذة
        title_label = QLabel("تسجيل الدخول")
        title_label.setObjectName("title_label")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # حقل كلمة المرور
        password_label = QLabel("كلمة المرور:")
        password_label.setObjectName("password_label")
        self.password_input = QLineEdit()
        self.password_input.setObjectName("password_input")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("أدخل كلمة المرور هنا")
        self.password_input.returnPressed.connect(self.login)
        # Default development password for ease of testing
        self.password_input.setText("123456")
        
        form_layout = QVBoxLayout()
        form_layout.setSpacing(5)
        form_layout.addWidget(password_label)
        form_layout.addWidget(self.password_input)
        main_layout.addLayout(form_layout)

        # أزرار التحكم
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)

        self.login_button = QPushButton("دخول")
        self.login_button.setObjectName("login_button")
        self.login_button.clicked.connect(self.login)
        
        cancel_button = QPushButton("إلغاء")
        cancel_button.setObjectName("cancel_button")
        cancel_button.clicked.connect(self.reject)

        buttons_layout.addWidget(cancel_button)
        buttons_layout.addWidget(self.login_button)
        
        main_layout.addLayout(buttons_layout)

        # تركيز على حقل كلمة المرور
        self.password_input.setFocus()
    
    def login(self):
        """
        تسجيل الدخول
        """
        password = self.password_input.text().strip()
        
        if not password:
            QMessageBox.warning(self, "تحذير", "يرجى إدخال كلمة المرور")
            return
        
        # التحقق من كلمة المرور
        is_valid, message = self.auth_controller.verify_password(password)
        
        if is_valid:
            self.login_successful.emit()
            self.accept()
        else:
            QMessageBox.critical(self, "خطأ", message)
            self.password_input.clear()
            self.password_input.setFocus()
    
    def keyPressEvent(self, event):
        """
        التعامل مع ضغط المفاتيح
        """
        if event.key() == Qt.Key_Escape:
            self.reject()
        else:
            super().keyPressEvent(event)
