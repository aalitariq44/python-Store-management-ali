# نوافذ الحوار - Dialog Windows
# يحتوي على النوافذ المنبثقة لإضافة وتعديل البيانات

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from datetime import datetime, date

class PersonDialog(QDialog):
    """نافذة حوار لإضافة/تعديل الزبون"""
    
    def __init__(self, parent=None, person_data=None):
        super().__init__(parent)
        self.person_data = person_data
        self.init_ui()
        
        if person_data:
            self.load_person_data()
    
    def init_ui(self):
        """تهيئة واجهة المستخدم"""
        self.setWindowTitle("إضافة زبون جديد" if not self.person_data else "تعديل بيانات الزبون")
        self.setFixedSize(450, 350)

        # تطبيق تصميم عصري
        self.setStyleSheet("""
            QDialog {
                background-color: #3C3C3C;
                color: #F0F0F0;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
            }
            QLabel {
                font-size: 14px;
                margin-bottom: 5px;
            }
            QLineEdit, QTextEdit, QDoubleSpinBox, QDateEdit {
                background-color: #505050;
                border: 1px solid #707070;
                border-radius: 5px;
                padding: 8px;
                color: #F0F0F0;
            }
            QPushButton {
                background-color: #5A9B5A;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #6BBF6B;
            }
            QPushButton:pressed {
                background-color: #4A8B4A;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        form_layout = QFormLayout()
        
        # حقل الاسم
        self.name_edit = QLineEdit()
        form_layout.addRow(QLabel("الاسم:"), self.name_edit)
        
        # حقل الهاتف
        self.phone_edit = QLineEdit()
        form_layout.addRow(QLabel("رقم الهاتف:"), self.phone_edit)
        
        # حقل العنوان
        self.address_edit = QTextEdit()
        self.address_edit.setMaximumHeight(80)
        form_layout.addRow(QLabel("العنوان:"), self.address_edit)
        
        layout.addLayout(form_layout)
        
        # أزرار الحفظ والإلغاء
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("حفظ")
        self.cancel_button = QPushButton("إلغاء")
        
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)
        
        # ربط الأزرار
        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        
        self.setLayout(layout)
    
    def load_person_data(self):
        """تحميل بيانات الزبون للتعديل"""
        if self.person_data:
            self.name_edit.setText(self.person_data[1])  # name
            self.phone_edit.setText(self.person_data[2] or "")  # phone
            self.address_edit.setText(self.person_data[3] or "")  # address
    
    def get_data(self):
        """الحصول على البيانات المدخلة"""
        return {
            'name': self.name_edit.text().strip(),
            'phone': self.phone_edit.text().strip(),
            'address': self.address_edit.toPlainText().strip()
        }

class DebtDialog(QDialog):
    """نافذة حوار لإضافة/تعديل الدين"""
    
    def __init__(self, parent=None, debt_data=None):
        super().__init__(parent)
        self.debt_data = debt_data
        self.init_ui()
        
        if debt_data:
            self.load_debt_data()
    
    def init_ui(self):
        """تهيئة واجهة المستخدم"""
        self.setWindowTitle("إضافة دين جديد" if not self.debt_data else "تعديل الدين")
        self.setFixedSize(450, 300)

        # تطبيق تصميم عصري
        self.setStyleSheet("""
            QDialog {
                background-color: #3C3C3C;
                color: #F0F0F0;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
            }
            QLabel {
                font-size: 14px;
                margin-bottom: 5px;
            }
            QDoubleSpinBox, QTextEdit, QCheckBox {
                background-color: #505050;
                border: 1px solid #707070;
                border-radius: 5px;
                padding: 8px;
                color: #F0F0F0;
            }
            QCheckBox {
                border: none;
            }
            QPushButton {
                background-color: #5A9B5A;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #6BBF6B;
            }
            QPushButton:pressed {
                background-color: #4A8B4A;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        form_layout = QFormLayout()
        
        # حقل المبلغ
        self.amount_edit = QDoubleSpinBox()
        self.amount_edit.setMaximum(999999.99)
        self.amount_edit.setSuffix(" ريال")
        form_layout.addRow(QLabel("المبلغ:"), self.amount_edit)
        
        # حقل الوصف
        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(80)
        form_layout.addRow(QLabel("الوصف:"), self.description_edit)
        
        layout.addLayout(form_layout)
        
        # حالة السداد
        if self.debt_data:  # فقط في حالة التعديل
            self.is_paid_checkbox = QCheckBox("تم السداد")
            layout.addWidget(self.is_paid_checkbox)
        
        # أزرار الحفظ والإلغاء
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("حفظ")
        self.cancel_button = QPushButton("إلغاء")
        
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)
        
        # ربط الأزرار
        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        
        self.setLayout(layout)
    
    def load_debt_data(self):
        """تحميل بيانات الدين للتعديل"""
        if self.debt_data:
            self.amount_edit.setValue(self.debt_data[2])  # amount
            self.description_edit.setText(self.debt_data[3] or "")  # description
            if hasattr(self, 'is_paid_checkbox'):
                self.is_paid_checkbox.setChecked(bool(self.debt_data[5]))  # is_paid
    
    def get_data(self):
        """الحصول على البيانات المدخلة"""
        data = {
            'amount': self.amount_edit.value(),
            'description': self.description_edit.toPlainText().strip()
        }
        
        if hasattr(self, 'is_paid_checkbox'):
            data['is_paid'] = self.is_paid_checkbox.isChecked()
        
        return data

class InstallmentDialog(QDialog):
    """نافذة حوار لإضافة/تعديل القسط"""
    
    def __init__(self, parent=None, installment_data=None):
        super().__init__(parent)
        self.installment_data = installment_data
        self.init_ui()
        
        if installment_data:
            self.load_installment_data()
    
    def init_ui(self):
        """تهيئة واجهة المستخدم"""
        self.setWindowTitle("إضافة قسط جديد" if not self.installment_data else "تعديل القسط")
        self.setFixedSize(450, 400)

        # تطبيق تصميم عصري
        self.setStyleSheet("""
            QDialog {
                background-color: #3C3C3C;
                color: #F0F0F0;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
            }
            QLabel {
                font-size: 14px;
                margin-bottom: 5px;
            }
            QDoubleSpinBox, QDateEdit, QTextEdit, QCheckBox {
                background-color: #505050;
                border: 1px solid #707070;
                border-radius: 5px;
                padding: 8px;
                color: #F0F0F0;
            }
            QCheckBox, QDateEdit::drop-down {
                border: none;
            }
            QPushButton {
                background-color: #5A9B5A;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #6BBF6B;
            }
            QPushButton:pressed {
                background-color: #4A8B4A;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        form_layout = QFormLayout()
        
        # المبلغ الإجمالي
        self.total_amount_edit = QDoubleSpinBox()
        self.total_amount_edit.setMaximum(999999.99)
        self.total_amount_edit.setSuffix(" ريال")
        form_layout.addRow(QLabel("المبلغ الإجمالي:"), self.total_amount_edit)
        
        # المبلغ المدفوع (فقط في حالة التعديل)
        if self.installment_data:
            self.paid_amount_edit = QDoubleSpinBox()
            self.paid_amount_edit.setMaximum(999999.99)
            self.paid_amount_edit.setSuffix(" ريال")
            form_layout.addRow(QLabel("المبلغ المدفوع:"), self.paid_amount_edit)
        
        # مبلغ القسط
        self.installment_amount_edit = QDoubleSpinBox()
        self.installment_amount_edit.setMaximum(999999.99)
        self.installment_amount_edit.setSuffix(" ريال")
        form_layout.addRow(QLabel("مبلغ القسط:"), self.installment_amount_edit)
        
        # تاريخ الاستحقاق
        self.due_date_edit = QDateEdit()
        self.due_date_edit.setDate(date.today())
        self.due_date_edit.setCalendarPopup(True)
        form_layout.addRow(QLabel("تاريخ الاستحقاق:"), self.due_date_edit)
        
        # الوصف
        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(60)
        form_layout.addRow(QLabel("الوصف:"), self.description_edit)
        
        layout.addLayout(form_layout)
        
        # حالة الإكمال (فقط في حالة التعديل)
        if self.installment_data:
            self.is_completed_checkbox = QCheckBox("مكتمل")
            layout.addWidget(self.is_completed_checkbox)
        
        # أزرار الحفظ والإلغاء
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("حفظ")
        self.cancel_button = QPushButton("إلغاء")
        
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)
        
        # ربط الأزرار
        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        
        self.setLayout(layout)
    
    def load_installment_data(self):
        """تحميل بيانات القسط للتعديل"""
        if self.installment_data:
            self.total_amount_edit.setValue(self.installment_data[2])  # total_amount
            if hasattr(self, 'paid_amount_edit'):
                self.paid_amount_edit.setValue(self.installment_data[3])  # paid_amount
            self.installment_amount_edit.setValue(self.installment_data[4])  # installment_amount
            if self.installment_data[5]:  # due_date
                due_date = datetime.strptime(self.installment_data[5], "%Y-%m-%d").date()
                self.due_date_edit.setDate(due_date)
            self.description_edit.setText(self.installment_data[6] or "")  # description
            if hasattr(self, 'is_completed_checkbox'):
                self.is_completed_checkbox.setChecked(bool(self.installment_data[7]))  # is_completed
    
    def get_data(self):
        """الحصول على البيانات المدخلة"""
        data = {
            'total_amount': self.total_amount_edit.value(),
            'installment_amount': self.installment_amount_edit.value(),
            'due_date': self.due_date_edit.date().toString("yyyy-MM-dd"),
            'description': self.description_edit.toPlainText().strip()
        }
        
        if hasattr(self, 'paid_amount_edit'):
            data['paid_amount'] = self.paid_amount_edit.value()
        
        if hasattr(self, 'is_completed_checkbox'):
            data['is_completed'] = self.is_completed_checkbox.isChecked()
        
        return data

class SubscriptionDialog(QDialog):
    """نافذة حوار لإضافة/تعديل اشتراك الإنترنت"""
    
    def __init__(self, parent=None, subscription_data=None):
        super().__init__(parent)
        self.subscription_data = subscription_data
        self.init_ui()
        
        if subscription_data:
            self.load_subscription_data()
    
    def init_ui(self):
        """تهيئة واجهة المستخدم"""
        self.setWindowTitle("إضافة اشتراك جديد" if not self.subscription_data else "تعديل الاشتراك")
        self.setFixedSize(450, 400)

        # تطبيق تصميم عصري
        self.setStyleSheet("""
            QDialog {
                background-color: #3C3C3C;
                color: #F0F0F0;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
            }
            QLabel {
                font-size: 14px;
                margin-bottom: 5px;
            }
            QLineEdit, QDoubleSpinBox, QDateEdit, QTextEdit, QCheckBox {
                background-color: #505050;
                border: 1px solid #707070;
                border-radius: 5px;
                padding: 8px;
                color: #F0F0F0;
            }
            QCheckBox, QDateEdit::drop-down {
                border: none;
            }
            QPushButton {
                background-color: #5A9B5A;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #6BBF6B;
            }
            QPushButton:pressed {
                background-color: #4A8B4A;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        form_layout = QFormLayout()
        
        # اسم الخطة
        self.plan_name_edit = QLineEdit()
        form_layout.addRow(QLabel("اسم الخطة:"), self.plan_name_edit)
        
        # التكلفة الشهرية
        self.monthly_cost_edit = QDoubleSpinBox()
        self.monthly_cost_edit.setMaximum(999999.99)
        self.monthly_cost_edit.setSuffix(" ريال")
        form_layout.addRow(QLabel("التكلفة الشهرية:"), self.monthly_cost_edit)
        
        # تاريخ البداية
        self.start_date_edit = QDateEdit()
        self.start_date_edit.setDate(date.today())
        self.start_date_edit.setCalendarPopup(True)
        form_layout.addRow(QLabel("تاريخ البداية:"), self.start_date_edit)
        
        # تاريخ النهاية
        self.end_date_edit = QDateEdit()
        self.end_date_edit.setDate(date.today())
        self.end_date_edit.setCalendarPopup(True)
        form_layout.addRow(QLabel("تاريخ النهاية:"), self.end_date_edit)
        
        # الوصف
        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(60)
        form_layout.addRow(QLabel("الوصف:"), self.description_edit)
        
        layout.addLayout(form_layout)
        
        # حالة النشاط (فقط في حالة التعديل)
        if self.subscription_data:
            self.is_active_checkbox = QCheckBox("نشط")
            layout.addWidget(self.is_active_checkbox)
        
        # أزرار الحفظ والإلغاء
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("حفظ")
        self.cancel_button = QPushButton("إلغاء")
        
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)
        
        # ربط الأزرار
        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        
        self.setLayout(layout)
    
    def load_subscription_data(self):
        """تحميل بيانات الاشتراك للتعديل"""
        if self.subscription_data:
            self.plan_name_edit.setText(self.subscription_data[2])  # plan_name
            self.monthly_cost_edit.setValue(self.subscription_data[3])  # monthly_cost
            if self.subscription_data[4]:  # start_date
                start_date = datetime.strptime(self.subscription_data[4], "%Y-%m-%d").date()
                self.start_date_edit.setDate(start_date)
            if self.subscription_data[5]:  # end_date
                end_date = datetime.strptime(self.subscription_data[5], "%Y-%m-%d").date()
                self.end_date_edit.setDate(end_date)
            if hasattr(self, 'is_active_checkbox'):
                self.is_active_checkbox.setChecked(bool(self.subscription_data[6]))  # is_active
            self.description_edit.setText(self.subscription_data[7] or "")  # description
    
    def get_data(self):
        """الحصول على البيانات المدخلة"""
        data = {
            'plan_name': self.plan_name_edit.text().strip(),
            'monthly_cost': self.monthly_cost_edit.value(),
            'start_date': self.start_date_edit.date().toString("yyyy-MM-dd"),
            'end_date': self.end_date_edit.date().toString("yyyy-MM-dd"),
            'description': self.description_edit.toPlainText().strip()
        }
        
        if hasattr(self, 'is_active_checkbox'):
            data['is_active'] = self.is_active_checkbox.isChecked()
        
        return data
