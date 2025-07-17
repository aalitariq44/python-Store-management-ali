# -*- coding: utf-8 -*-
"""
نافذة حوار إضافة/تعديل زبون
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
                             QLineEdit, QTextEdit, QPushButton, QLabel, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from database.models import Person
from utils.helpers import MessageHelper


class AddPersonDialog(QDialog):
    """
    نافذة حوار إضافة أو تعديل زبون
    """
    
    def __init__(self, parent=None, person: Person = None):
        super().__init__(parent)
        self.person = person  # إذا كان موجود فهو تعديل، وإلا فهو إضافة
        self.init_ui()
        self.setup_connections()
        
        if self.person:
            self.load_person_data()
    
    def init_ui(self):
        """
        تهيئة واجهة المستخدم
        """
        # إعداد النافذة
        title = "تعديل زبون" if self.person else "إضافة زبون جديد"
        self.setWindowTitle(title)
        self.setFixedSize(500, 400)
        self.setModal(True)
        
        # التخطيط الرئيسي
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # إضافة العنوان
        self.add_title(main_layout, title)
        
        # إضافة النموذج
        self.add_form(main_layout)
        
        # إضافة الأزرار
        self.add_buttons(main_layout)
    
    def add_title(self, layout: QVBoxLayout, title: str):
        """
        إضافة عنوان النافذة
        
        Args:
            layout: التخطيط
            title: العنوان
        """
        title_frame = QFrame()
        title_frame.setStyleSheet("""
            QFrame {
                background-color: #007bff;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        
        title_layout = QVBoxLayout(title_frame)
        
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 18px;
                font-weight: bold;
                background: transparent;
            }
        """)
        title_layout.addWidget(title_label)
        
        layout.addWidget(title_frame)
    
    def add_form(self, layout: QVBoxLayout):
        """
        إضافة نموذج الإدخال
        
        Args:
            layout: التخطيط
        """
        form_frame = QFrame()
        form_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 20px;
            }
        """)
        
        form_layout = QFormLayout(form_frame)
        form_layout.setSpacing(15)
        
        # حقل الاسم
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("أدخل اسم الزبون")
        self.style_input(self.name_input)
        form_layout.addRow("الاسم: *", self.name_input)
        
        # حقل رقم الهاتف
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("أدخل رقم الهاتف")
        self.style_input(self.phone_input)
        form_layout.addRow("رقم الهاتف:", self.phone_input)
        
        # حقل العنوان
        self.address_input = QTextEdit()
        self.address_input.setPlaceholderText("أدخل العنوان")
        self.address_input.setMaximumHeight(80)
        self.style_input(self.address_input)
        form_layout.addRow("العنوان:", self.address_input)
        
        # ملاحظة الحقول المطلوبة
        note_label = QLabel("* الحقول المطلوبة")
        note_label.setStyleSheet("""
            QLabel {
                color: #dc3545;
                font-size: 11px;
                font-style: italic;
            }
        """)
        form_layout.addRow("", note_label)
        
        layout.addWidget(form_frame)
    
    def style_input(self, widget):
        """
        تنسيق حقل الإدخال
        
        Args:
            widget: حقل الإدخال
        """
        widget.setStyleSheet("""
            QLineEdit, QTextEdit {
                padding: 8px 12px;
                border: 2px solid #ced4da;
                border-radius: 5px;
                font-size: 12px;
                background-color: white;
            }
            QLineEdit:focus, QTextEdit:focus {
                border-color: #007bff;
                outline: none;
            }
        """)
    
    def add_buttons(self, layout: QVBoxLayout):
        """
        إضافة أزرار الحفظ والإلغاء
        
        Args:
            layout: التخطيط
        """
        buttons_frame = QFrame()
        buttons_layout = QHBoxLayout(buttons_frame)
        buttons_layout.setSpacing(10)
        
        # زر الحفظ
        save_text = "تحديث" if self.person else "حفظ"
        self.save_btn = QPushButton(save_text)
        self.save_btn.setMinimumHeight(40)
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:pressed {
                background-color: #1e7e34;
            }
        """)
        
        # زر الإلغاء
        self.cancel_btn = QPushButton("إلغاء")
        self.cancel_btn.setMinimumHeight(40)
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #545b62;
            }
            QPushButton:pressed {
                background-color: #495057;
            }
        """)
        
        # ترتيب الأزرار
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.save_btn)
        buttons_layout.addWidget(self.cancel_btn)
        
        layout.addWidget(buttons_frame)
    
    def setup_connections(self):
        """
        إعداد الاتصالات والأحداث
        """
        self.save_btn.clicked.connect(self.save_person)
        self.cancel_btn.clicked.connect(self.reject)
        
        # التنقل بين الحقول بـ Enter
        self.name_input.returnPressed.connect(self.phone_input.setFocus)
        self.phone_input.returnPressed.connect(self.address_input.setFocus)
    
    def load_person_data(self):
        """
        تحميل بيانات الزبون للتعديل
        """
        if self.person:
            self.name_input.setText(self.person.name)
            self.phone_input.setText(self.person.phone or "")
            self.address_input.setPlainText(self.person.address or "")
    
    def get_person_data(self) -> dict:
        """
        الحصول على بيانات الزبون من النموذج
        
        Returns:
            قاموس ببيانات الزبون
        """
        return {
            'name': self.name_input.text().strip(),
            'phone': self.phone_input.text().strip(),
            'address': self.address_input.toPlainText().strip()
        }
    
    def validate_data(self) -> tuple[bool, str]:
        """
        التحقق من صحة البيانات
        
        Returns:
            tuple: (صحيح, رسالة الخطأ)
        """
        data = self.get_person_data()
        
        # التحقق من الاسم
        if not data['name']:
            return False, "اسم الزبون مطلوب"
        
        if len(data['name']) < 2:
            return False, "اسم الزبون يجب أن يكون أكثر من حرفين"
        
        if len(data['name']) > 100:
            return False, "اسم الزبون طويل جداً (أكثر من 100 حرف)"
        
        # التحقق من رقم الهاتف (إذا تم إدخاله)
        if data['phone']:
            # فحص بسيط لرقم الهاتف
            phone_clean = data['phone'].replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
            if not phone_clean.replace('+', '').isdigit():
                return False, "رقم الهاتف يجب أن يحتوي على أرقام فقط"
            
            if len(phone_clean) < 7 or len(phone_clean) > 20:
                return False, "رقم الهاتف غير صحيح (يجب أن يكون بين 7-20 رقم)"
        
        # التحقق من العنوان
        if data['address'] and len(data['address']) > 200:
            return False, "العنوان طويل جداً (أكثر من 200 حرف)"
        
        return True, ""
    
    def save_person(self):
        """
        حفظ بيانات الزبون
        """
        # التحقق من صحة البيانات
        is_valid, error_message = self.validate_data()
        if not is_valid:
            MessageHelper.show_error(self, "خطأ في البيانات", error_message)
            return
        
        # قبول النافذة
        self.accept()
    
    def keyPressEvent(self, event):
        """
        معالجة الضغط على المفاتيح
        
        Args:
            event: حدث الضغط على المفتاح
        """
        # Escape للإلغاء
        if event.key() == Qt.Key_Escape:
            self.reject()
        # Enter للحفظ (إذا لم يكن في حقل النص المتعدد الأسطر)
        elif event.key() in (Qt.Key_Return, Qt.Key_Enter):
            if not self.address_input.hasFocus():
                self.save_person()
        else:
            super().keyPressEvent(event)
