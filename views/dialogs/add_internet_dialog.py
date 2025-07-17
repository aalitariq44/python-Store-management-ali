# -*- coding: utf-8 -*-
"""
نافذة حوار إضافة/تعديل اشتراك إنترنت
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
                             QLineEdit, QTextEdit, QPushButton, QLabel, QFrame,
                             QDateEdit, QCheckBox, QDoubleSpinBox)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont
from datetime import date
from database.models import InternetSubscription
from utils.helpers import MessageHelper, DateHelper


class AddInternetDialog(QDialog):
    """
    نافذة حوار إضافة أو تعديل اشتراك إنترنت
    """
    
    def __init__(self, parent=None, subscription: InternetSubscription = None, person_id: int = None):
        super().__init__(parent)
        self.subscription = subscription
        self.person_id = person_id
        self.init_ui()
        self.setup_connections()
        
        if self.subscription:
            self.load_subscription_data()
    
    def init_ui(self):
        """
        تهيئة واجهة المستخدم
        """
        title = "تعديل اشتراك إنترنت" if self.subscription else "إضافة اشتراك إنترنت جديد"
        self.setWindowTitle(title)
        self.setFixedSize(500, 500)
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
                background-color: #27ae60;
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
        
        # اسم الباقة
        self.plan_name_input = QLineEdit()
        self.plan_name_input.setPlaceholderText("مثال: باقة الذهبية")
        self.style_input(self.plan_name_input)
        form_layout.addRow("اسم الباقة: *", self.plan_name_input)
        
        # الرسوم الشهرية
        self.monthly_fee_input = QDoubleSpinBox()
        self.monthly_fee_input.setRange(0.00, 999999.99)
        self.monthly_fee_input.setDecimals(2)
        self.monthly_fee_input.setSuffix(" ر.س")
        self.style_input(self.monthly_fee_input)
        form_layout.addRow("الرسوم الشهرية:", self.monthly_fee_input)
        
        # السرعة
        self.speed_input = QLineEdit()
        self.speed_input.setPlaceholderText("مثال: 100 Mbps")
        self.style_input(self.speed_input)
        form_layout.addRow("السرعة:", self.speed_input)
        
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
        
        # حالة النشاط
        self.is_active_checkbox = QCheckBox("نشط")
        self.is_active_checkbox.setChecked(True)  # افتراضي نشط
        self.is_active_checkbox.setStyleSheet("""
            QCheckBox {
                font-size: 12px;
                font-weight: bold;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
        """)
        form_layout.addRow("", self.is_active_checkbox)
        
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
                border-color: #27ae60;
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
        
        save_text = "تحديث" if self.subscription else "حفظ"
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
        self.save_btn.clicked.connect(self.save_subscription)
        self.cancel_btn.clicked.connect(self.reject)
    
    def load_subscription_data(self):
        """
        تحميل بيانات الاشتراك للتعديل
        """
        if self.subscription:
            self.plan_name_input.setText(self.subscription.plan_name)
            self.monthly_fee_input.setValue(self.subscription.monthly_fee)
            self.speed_input.setText(self.subscription.speed or "")
            
            if self.subscription.start_date:
                qdate = DateHelper.date_to_qdate(self.subscription.start_date)
                if qdate:
                    self.start_date_input.setDate(qdate)
            
            if self.subscription.end_date:
                qdate = DateHelper.date_to_qdate(self.subscription.end_date)
                if qdate:
                    self.end_date_input.setDate(qdate)
            
            self.is_active_checkbox.setChecked(self.subscription.is_active)
    
    def get_subscription_data(self) -> dict:
        """
        الحصول على بيانات الاشتراك من النموذج
        """
        start_date = DateHelper.qdate_to_date(self.start_date_input.date())
        end_date = DateHelper.qdate_to_date(self.end_date_input.date())
        
        return {
            'plan_name': self.plan_name_input.text().strip(),
            'monthly_fee': self.monthly_fee_input.value(),
            'speed': self.speed_input.text().strip(),
            'start_date': start_date,
            'end_date': end_date,
            'is_active': self.is_active_checkbox.isChecked()
        }
    
    def validate_data(self) -> tuple[bool, str]:
        """
        التحقق من صحة البيانات
        """
        data = self.get_subscription_data()
        
        if not data['plan_name']:
            return False, "اسم الباقة مطلوب"
        
        if len(data['plan_name']) > 100:
            return False, "اسم الباقة طويل جداً (أكثر من 100 حرف)"
        
        if data['monthly_fee'] < 0:
            return False, "الرسوم الشهرية لا يمكن أن تكون سالبة"
        
        if data['speed'] and len(data['speed']) > 50:
            return False, "وصف السرعة طويل جداً (أكثر من 50 حرف)"
        
        if data['start_date'] and data['end_date'] and data['start_date'] >= data['end_date']:
            return False, "تاريخ البداية يجب أن يكون قبل تاريخ النهاية"
        
        return True, ""
    
    def save_subscription(self):
        """
        حفظ بيانات الاشتراك
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
            self.save_subscription()
        else:
            super().keyPressEvent(event)
