# -*- coding: utf-8 -*-
"""
نافذة حوار إضافة/تعديل دين
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
                             QLineEdit, QTextEdit, QPushButton, QLabel, QFrame,
                             QDateEdit, QCheckBox, QDoubleSpinBox)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont
from datetime import date
from database.models import Debt
from utils.helpers import MessageHelper, DateHelper


class AddDebtDialog(QDialog):
    """
    نافذة حوار إضافة أو تعديل دين
    """
    
    def __init__(self, parent=None, debt: Debt = None, person_id: int = None):
        super().__init__(parent)
        self.debt = debt
        self.person_id = person_id  # للإضافة الجديدة
        self.init_ui()
        self.setup_connections()
        
        if self.debt:
            self.load_debt_data()
    
    def init_ui(self):
        """
        تهيئة واجهة المستخدم
        """
        title = "تعديل دين" if self.debt else "إضافة دين جديد"
        self.setWindowTitle(title)
        self.setFixedSize(500, 450)
        self.setModal(True)
        
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        self.add_title(main_layout, title)
        self.add_form(main_layout)
        self.add_buttons(main_layout)
    
    def add_title(self, layout: QVBoxLayout, title: str):
        """
        إضافة عنوان النافذة
        """
        title_frame = QFrame()
        title_frame.setStyleSheet("""
            QFrame {
                background-color: #dc3545;
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
        
        # مبلغ الدين
        self.amount_input = QDoubleSpinBox()
        self.amount_input.setRange(0.01, 999999999.99)
        self.amount_input.setDecimals(2)
        self.amount_input.setSuffix(" ر.س")
        self.style_input(self.amount_input)
        form_layout.addRow("مبلغ الدين: *", self.amount_input)
        
        # وصف الدين
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("أدخل وصف الدين")
        self.description_input.setMaximumHeight(80)
        self.style_input(self.description_input)
        form_layout.addRow("وصف الدين: *", self.description_input)
        
        # تاريخ الاستحقاق
        self.due_date_input = QDateEdit()
        self.due_date_input.setDate(QDate.currentDate().addDays(30))  # افتراضي: بعد شهر
        self.due_date_input.setCalendarPopup(True)
        self.due_date_input.setDisplayFormat("yyyy-MM-dd")
        self.style_input(self.due_date_input)
        form_layout.addRow("تاريخ الاستحقاق:", self.due_date_input)
        
        # حالة الدفع
        self.is_paid_checkbox = QCheckBox("مدفوع")
        self.is_paid_checkbox.setStyleSheet("""
            QCheckBox {
                font-size: 12px;
                font-weight: bold;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
        """)
        form_layout.addRow("", self.is_paid_checkbox)
        
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
        """
        widget.setStyleSheet("""
            QLineEdit, QTextEdit, QDoubleSpinBox, QDateEdit {
                padding: 8px 12px;
                border: 2px solid #ced4da;
                border-radius: 5px;
                font-size: 12px;
                background-color: white;
            }
            QLineEdit:focus, QTextEdit:focus, QDoubleSpinBox:focus, QDateEdit:focus {
                border-color: #dc3545;
                outline: none;
            }
        """)
    
    def add_buttons(self, layout: QVBoxLayout):
        """
        إضافة أزرار الحفظ والإلغاء
        """
        buttons_frame = QFrame()
        buttons_layout = QHBoxLayout(buttons_frame)
        buttons_layout.setSpacing(10)
        
        save_text = "تحديث" if self.debt else "حفظ"
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
        """)
        
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
        """)
        
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.save_btn)
        buttons_layout.addWidget(self.cancel_btn)
        
        layout.addWidget(buttons_frame)
    
    def setup_connections(self):
        """
        إعداد الاتصالات والأحداث
        """
        self.save_btn.clicked.connect(self.save_debt)
        self.cancel_btn.clicked.connect(self.reject)
    
    def load_debt_data(self):
        """
        تحميل بيانات الدين للتعديل
        """
        if self.debt:
            self.amount_input.setValue(self.debt.amount)
            self.description_input.setPlainText(self.debt.description)
            
            if self.debt.due_date:
                qdate = DateHelper.date_to_qdate(self.debt.due_date)
                if qdate:
                    self.due_date_input.setDate(qdate)
            
            self.is_paid_checkbox.setChecked(self.debt.is_paid)
    
    def get_debt_data(self) -> dict:
        """
        الحصول على بيانات الدين من النموذج
        """
        due_date = DateHelper.qdate_to_date(self.due_date_input.date())
        
        return {
            'amount': self.amount_input.value(),
            'description': self.description_input.toPlainText().strip(),
            'due_date': due_date,
            'is_paid': self.is_paid_checkbox.isChecked()
        }
    
    def validate_data(self) -> tuple[bool, str]:
        """
        التحقق من صحة البيانات
        """
        data = self.get_debt_data()
        
        if data['amount'] <= 0:
            return False, "مبلغ الدين يجب أن يكون أكبر من صفر"
        
        if not data['description']:
            return False, "وصف الدين مطلوب"
        
        if len(data['description']) > 200:
            return False, "وصف الدين طويل جداً (أكثر من 200 حرف)"
        
        return True, ""
    
    def save_debt(self):
        """
        حفظ بيانات الدين
        """
        is_valid, error_message = self.validate_data()
        if not is_valid:
            MessageHelper.show_error(self, "خطأ في البيانات", error_message)
            return
        
        self.accept()
    
    def keyPressEvent(self, event):
        """
        معالجة الضغط على المفاتيح
        """
        if event.key() == Qt.Key_Escape:
            self.reject()
        elif event.key() in (Qt.Key_Return, Qt.Key_Enter):
            if not self.description_input.hasFocus():
                self.save_debt()
        else:
            super().keyPressEvent(event)
