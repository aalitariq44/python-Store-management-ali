# -*- coding: utf-8 -*-
"""
نافذة حوار إضافة/تعديل قسط
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
                             QLineEdit, QTextEdit, QPushButton, QLabel, QFrame,
                             QDateEdit, QCheckBox, QDoubleSpinBox, QComboBox)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont
from datetime import date
from database.models import Installment
from utils.helpers import MessageHelper, DateHelper


class AddInstallmentDialog(QDialog):
    """
    نافذة حوار إضافة أو تعديل قسط
    """
    
    def __init__(self, parent=None, installment: Installment = None, person_id: int = None):
        super().__init__(parent)
        self.installment = installment
        self.person_id = person_id
        self.init_ui()
        self.setup_connections()
        
        if self.installment:
            self.load_installment_data()
    
    def init_ui(self):
        """
        تهيئة واجهة المستخدم
        """
        title = "تعديل قسط" if self.installment else "إضافة قسط جديد"
        self.setWindowTitle(title)
        self.setFixedSize(550, 600)
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
                background-color: #f39c12;
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
        
        # المبلغ الإجمالي
        self.total_amount_input = QDoubleSpinBox()
        self.total_amount_input.setRange(0.01, 999999999.99)
        self.total_amount_input.setDecimals(2)
        self.total_amount_input.setSuffix(" ر.س")
        self.style_input(self.total_amount_input)
        form_layout.addRow("المبلغ الإجمالي: *", self.total_amount_input)
        
        # المبلغ المدفوع
        self.paid_amount_input = QDoubleSpinBox()
        self.paid_amount_input.setRange(0.00, 999999999.99)
        self.paid_amount_input.setDecimals(2)
        self.paid_amount_input.setSuffix(" ر.س")
        self.style_input(self.paid_amount_input)
        form_layout.addRow("المبلغ المدفوع:", self.paid_amount_input)
        
        # مبلغ القسط
        self.installment_amount_input = QDoubleSpinBox()
        self.installment_amount_input.setRange(0.01, 999999999.99)
        self.installment_amount_input.setDecimals(2)
        self.installment_amount_input.setSuffix(" ر.س")
        self.style_input(self.installment_amount_input)
        form_layout.addRow("مبلغ القسط: *", self.installment_amount_input)
        
        # دورية القسط
        self.frequency_combo = QComboBox()
        self.frequency_combo.addItems(["monthly", "weekly", "yearly"])
        self.frequency_combo.setItemText(0, "شهري")
        self.frequency_combo.setItemText(1, "أسبوعي")
        self.frequency_combo.setItemText(2, "سنوي")
        self.style_input(self.frequency_combo)
        form_layout.addRow("دورية القسط: *", self.frequency_combo)
        
        # وصف القسط
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("أدخل وصف القسط")
        self.description_input.setMaximumHeight(80)
        self.style_input(self.description_input)
        form_layout.addRow("وصف القسط: *", self.description_input)
        
        # تاريخ البداية
        self.start_date_input = QDateEdit()
        self.start_date_input.setDate(QDate.currentDate())
        self.start_date_input.setCalendarPopup(True)
        self.start_date_input.setDisplayFormat("yyyy-MM-dd")
        self.style_input(self.start_date_input)
        form_layout.addRow("تاريخ البداية:", self.start_date_input)
        
        # تاريخ النهاية
        self.end_date_input = QDateEdit()
        self.end_date_input.setDate(QDate.currentDate().addYears(1))
        self.end_date_input.setCalendarPopup(True)
        self.end_date_input.setDisplayFormat("yyyy-MM-dd")
        self.style_input(self.end_date_input)
        form_layout.addRow("تاريخ النهاية:", self.end_date_input)
        
        # حالة الإكمال
        self.is_completed_checkbox = QCheckBox("مكتمل")
        self.is_completed_checkbox.setStyleSheet("""
            QCheckBox {
                font-size: 12px;
                font-weight: bold;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
        """)
        form_layout.addRow("", self.is_completed_checkbox)
        
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
            QLineEdit, QTextEdit, QDoubleSpinBox, QDateEdit, QComboBox {
                padding: 8px 12px;
                border: 2px solid #ced4da;
                border-radius: 5px;
                font-size: 12px;
                background-color: white;
            }
            QLineEdit:focus, QTextEdit:focus, QDoubleSpinBox:focus, QDateEdit:focus, QComboBox:focus {
                border-color: #f39c12;
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
        
        save_text = "تحديث" if self.installment else "حفظ"
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
        self.save_btn.clicked.connect(self.save_installment)
        self.cancel_btn.clicked.connect(self.reject)
        
        # التحديث التلقائي لحالة الإكمال
        self.paid_amount_input.valueChanged.connect(self.update_completion_status)
        self.total_amount_input.valueChanged.connect(self.update_completion_status)
    
    def update_completion_status(self):
        """
        تحديث حالة الإكمال تلقائياً
        """
        paid = self.paid_amount_input.value()
        total = self.total_amount_input.value()
        
        if total > 0 and paid >= total:
            self.is_completed_checkbox.setChecked(True)
        else:
            self.is_completed_checkbox.setChecked(False)
    
    def load_installment_data(self):
        """
        تحميل بيانات القسط للتعديل
        """
        if self.installment:
            self.total_amount_input.setValue(self.installment.total_amount)
            self.paid_amount_input.setValue(self.installment.paid_amount)
            self.installment_amount_input.setValue(self.installment.installment_amount)
            
            # تعيين الدورية
            frequency_map = {"monthly": 0, "weekly": 1, "yearly": 2}
            index = frequency_map.get(self.installment.frequency, 0)
            self.frequency_combo.setCurrentIndex(index)
            
            self.description_input.setPlainText(self.installment.description)
            
            if self.installment.start_date:
                qdate = DateHelper.date_to_qdate(self.installment.start_date)
                if qdate:
                    self.start_date_input.setDate(qdate)
            
            if self.installment.end_date:
                qdate = DateHelper.date_to_qdate(self.installment.end_date)
                if qdate:
                    self.end_date_input.setDate(qdate)
            
            self.is_completed_checkbox.setChecked(self.installment.is_completed)
    
    def get_installment_data(self) -> dict:
        """
        الحصول على بيانات القسط من النموذج
        """
        frequency_map = {0: "monthly", 1: "weekly", 2: "yearly"}
        frequency = frequency_map[self.frequency_combo.currentIndex()]
        
        start_date = DateHelper.qdate_to_date(self.start_date_input.date())
        end_date = DateHelper.qdate_to_date(self.end_date_input.date())
        
        return {
            'total_amount': self.total_amount_input.value(),
            'paid_amount': self.paid_amount_input.value(),
            'installment_amount': self.installment_amount_input.value(),
            'frequency': frequency,
            'description': self.description_input.toPlainText().strip(),
            'start_date': start_date,
            'end_date': end_date,
            'is_completed': self.is_completed_checkbox.isChecked()
        }
    
    def validate_data(self) -> tuple[bool, str]:
        """
        التحقق من صحة البيانات
        """
        data = self.get_installment_data()
        
        if data['total_amount'] <= 0:
            return False, "المبلغ الإجمالي يجب أن يكون أكبر من صفر"
        
        if data['paid_amount'] > data['total_amount']:
            return False, "المبلغ المدفوع لا يمكن أن يتجاوز المبلغ الإجمالي"
        
        if data['installment_amount'] <= 0:
            return False, "مبلغ القسط يجب أن يكون أكبر من صفر"
        
        if data['installment_amount'] > data['total_amount']:
            return False, "مبلغ القسط لا يمكن أن يتجاوز المبلغ الإجمالي"
        
        if not data['description']:
            return False, "وصف القسط مطلوب"
        
        if len(data['description']) > 200:
            return False, "وصف القسط طويل جداً (أكثر من 200 حرف)"
        
        if data['start_date'] and data['end_date'] and data['start_date'] >= data['end_date']:
            return False, "تاريخ البداية يجب أن يكون قبل تاريخ النهاية"
        
        return True, ""
    
    def save_installment(self):
        """
        حفظ بيانات القسط
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
                self.save_installment()
        else:
            super().keyPressEvent(event)
