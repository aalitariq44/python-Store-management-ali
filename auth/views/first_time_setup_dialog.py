# -*- coding: utf-8 -*-
"""
شاشة الإعداد الأولي لكلمة المرور
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, QFrame,
                             QWidget)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from auth.controllers.auth_controller import AuthController


class FirstTimeSetupDialog(QDialog):
    """
    نافذة الإعداد الأولي لكلمة المرور
    """
    
    # إشارة لإرسال حالة اكتمال الإعداد
    setup_completed = pyqtSignal()
    
    def __init__(self, auth_controller: AuthController, parent=None):
        """
        تهيئة نافذة الإعداد الأولي
        
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
        self.setWindowTitle("إعداد كلمة المرور - نظام إدارة المتجر")
        self.setFixedSize(600, 400)  # تم تغيير العرض من 450 إلى 600
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
                border: 2px solid #27ae60;
                border-radius: 10px;
                background-color: #f8f9fa;
                padding: 20px;
            }
        """)
        
        content_layout = QVBoxLayout(content_frame)
        content_layout.setSpacing(15)
        
        # عنوان النافذة
        title_label = QLabel("مرحباً بك في نظام إدارة المتجر")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50; border: none; padding: 10px;")
        content_layout.addWidget(title_label)
        
        # رسالة التوضيح
        info_label = QLabel("لحماية بياناتك، يرجى إعداد كلمة مرور للتطبيق")
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setFont(QFont("Arial", 10))
        info_label.setStyleSheet("color: #7f8c8d; border: none; padding: 5px;")
        info_label.setWordWrap(True)
        content_layout.addWidget(info_label)
        
        # مساحة فارغة
        content_layout.addWidget(QWidget())
        
        # حقل كلمة المرور الأولى
        password1_layout = QVBoxLayout()
        password1_label = QLabel("كلمة المرور:")
        password1_label.setFont(QFont("Arial", 10))
        password1_label.setStyleSheet("color: #34495e; border: none;")
        password1_layout.addWidget(password1_label)
        
        self.password1_input = QLineEdit()
        self.password1_input.setEchoMode(QLineEdit.Password)
        self.password1_input.setPlaceholderText("أدخل كلمة المرور...")
        self.password1_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                font-size: 24px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #27ae60;
            }
        """)
        password1_layout.addWidget(self.password1_input)
        
        content_layout.addLayout(password1_layout)
        
        # حقل تأكيد كلمة المرور
        password2_layout = QVBoxLayout()
        password2_label = QLabel("تأكيد كلمة المرور:")
        password2_label.setFont(QFont("Arial", 10))
        password2_label.setStyleSheet("color: #34495e; border: none;")
        password2_layout.addWidget(password2_label)
        
        self.password2_input = QLineEdit()
        self.password2_input.setEchoMode(QLineEdit.Password)
        self.password2_input.setPlaceholderText("أعد إدخال كلمة المرور...")
        self.password2_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                font-size: 24px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #27ae60;
            }
        """)
        self.password2_input.returnPressed.connect(self.setup_password)
        password2_layout.addWidget(self.password2_input)
        
        content_layout.addLayout(password2_layout)
        
        # مساحة فارغة
        content_layout.addWidget(QWidget())
        
        # أزرار التحكم
        buttons_layout = QHBoxLayout()
        
        # زر الإعداد
        self.setup_button = QPushButton("إعداد كلمة المرور")
        self.setup_button.setFont(QFont("Arial", 10, QFont.Bold))
        self.setup_button.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 12px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #229954;
            }
            QPushButton:pressed {
                background-color: #1e8449;
            }
        """)
        self.setup_button.clicked.connect(self.setup_password)
        buttons_layout.addWidget(self.setup_button)
        
        # زر الخروج
        exit_button = QPushButton("خروج")
        exit_button.setFont(QFont("Arial", 10))
        exit_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 12px 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            QPushButton:pressed {
                background-color: #a93226;
            }
        """)
        exit_button.clicked.connect(self.reject)
        buttons_layout.addWidget(exit_button)
        
        content_layout.addLayout(buttons_layout)
        
        main_layout.addWidget(content_frame)
        self.setLayout(main_layout)
        
        # تركيز على الحقل الأول
        self.password1_input.setFocus()
    
    def setup_password(self):
        """
        إعداد كلمة المرور
        """
        password1 = self.password1_input.text().strip()
        password2 = self.password2_input.text().strip()
        
        if not password1:
            QMessageBox.warning(self, "تحذير", "يرجى إدخال كلمة المرور")
            self.password1_input.setFocus()
            return
        
        if not password2:
            QMessageBox.warning(self, "تحذير", "يرجى تأكيد كلمة المرور")
            self.password2_input.setFocus()
            return
        
        # إعداد كلمة المرور
        success, message = self.auth_controller.setup_first_password(password1, password2)
        
        if success:
            QMessageBox.information(self, "نجح", message)
            self.setup_completed.emit()
            self.accept()
        else:
            QMessageBox.critical(self, "خطأ", message)
            self.password1_input.clear()
            self.password2_input.clear()
            self.password1_input.setFocus()
    
    def keyPressEvent(self, event):
        """
        التعامل مع ضغط المفاتيح
        """
        if event.key() == Qt.Key_Escape:
            self.reject()
        else:
            super().keyPressEvent(event)
