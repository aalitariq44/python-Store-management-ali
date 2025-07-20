# -*- coding: utf-8 -*-
"""
نافذة حوار إضافة/تعديل زبون
"""

from typing import Tuple
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
        self.setMinimumSize(600, 550)  # استخدام حجم أدنى لمرونة أكبر
        self.setModal(True)
        
        # التخطيط الرئيسي
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(25, 25, 25, 25)
        
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
        title_frame.setObjectName("title-frame") # استخدام ObjectName للتنسيق من QSS
        
        title_layout = QVBoxLayout(title_frame)
        
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        # إزالة التنسيق المباشر، سيعتمد على QSS
        
        title_layout.addWidget(title_label)
        
        layout.addWidget(title_frame)
    
    def add_form(self, layout: QVBoxLayout):
        """
        إضافة نموذج الإدخال
        
        Args:
            layout: التخطيط
        """
        form_frame = QFrame()
        # إزالة التنسيق المباشر
        
        form_layout = QFormLayout(form_frame)
        form_layout.setLabelAlignment(Qt.AlignRight)
        form_layout.setSpacing(18)
        
        # حقل الاسم
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("أدخل اسم الزبون")
        form_layout.addRow("الاسم: *", self.name_input)
        
        # حقل رقم الهاتف
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("أدخل رقم الهاتف")
        form_layout.addRow("رقم الهاتف:", self.phone_input)
        
        # حقل العنوان
        self.address_input = QTextEdit()
        self.address_input.setPlaceholderText("أدخل العنوان")
        self.address_input.setMinimumHeight(120)
        form_layout.addRow("العنوان:", self.address_input)
        
        # حقل الملاحظات
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("أدخل أي ملاحظات إضافية")
        self.notes_input.setMinimumHeight(100)
        form_layout.addRow("ملاحظات:", self.notes_input)
        
        # ملاحظة الحقول المطلوبة
        note_label = QLabel("* الحقول المطلوبة")
        note_label.setObjectName("error-label") # استخدام ObjectName
        form_layout.addRow("", note_label)
        
        layout.addWidget(form_frame)
    
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
        self.save_btn.setObjectName("edit-button") # استخدام ObjectName
        
        # زر الإلغاء
        self.cancel_btn = QPushButton("إلغاء")
        # يمكن إضافة objectName هنا إذا أردنا تنسيقًا خاصًا
        
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
        # لا يمكن استخدام returnPressed مع QTextEdit، لذا التنقل سيكون يدويًا بالـ Tab
    
    def load_person_data(self):
        """
        تحميل بيانات الزبون للتعديل
        """
        if self.person:
            self.name_input.setText(self.person.name)
            self.phone_input.setText(self.person.phone or "")
            self.address_input.setPlainText(self.person.address or "")
            if hasattr(self.person, 'notes'):
                self.notes_input.setPlainText(self.person.notes or "")
    
    def get_person_data(self) -> dict:
        """
        الحصول على بيانات الزبون من النموذج
        
        Returns:
            قاموس ببيانات الزبون
        """
        return {
            'name': self.name_input.text().strip(),
            'phone': self.phone_input.text().strip(),
            'address': self.address_input.toPlainText().strip(),
            'notes': self.notes_input.toPlainText().strip()
        }
    
    def validate_data(self) -> Tuple[bool, str]:
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
            
        # التحقق من الملاحظات
        if data['notes'] and len(data['notes']) > 500:
            return False, "الملاحظات طويلة جداً (أكثر من 500 حرف)"
        
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
            if not self.address_input.hasFocus() and not self.notes_input.hasFocus():
                self.save_person()
        else:
            super().keyPressEvent(event)
