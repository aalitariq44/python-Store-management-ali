# -*- coding: utf-8 -*-
"""
نافذة حوار إضافة/تعديل دين
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
                             QLineEdit, QTextEdit, QPushButton, QLabel, QFrame,
                             QDateEdit, QCheckBox, QDoubleSpinBox, QComboBox)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont
from datetime import date
from database.models import Debt
from utils.helpers import MessageHelper, DateHelper
from controllers.person_controller import PersonController


class AddDebtDialog(QDialog):
    """
    نافذة حوار إضافة أو تعديل دين
    """
    
    def __init__(self, parent=None, debt: Debt = None, person_id: int = None):
        super().__init__(parent)
        self.debt = debt
        self.person_id = person_id  # للإضافة الجديدة
        self.person_controller = PersonController()
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
        self.setMinimumSize(600, 550) # استخدام حجم أدنى
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
        title_frame.setObjectName("title-frame")
        # The background color is different, let's override it for this specific dialog
        title_frame.setStyleSheet("background-color: var(--danger-color);")

        title_layout = QVBoxLayout(title_frame)
        
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        
        title_layout.addWidget(title_label)
        
        layout.addWidget(title_frame)
    
    def add_form(self, layout: QVBoxLayout):
        """
        إضافة نموذج الإدخال
        """
        form_frame = QFrame()
        # Remove inline style
        
        form_layout = QFormLayout(form_frame)
        form_layout.setSpacing(15)
        
        # حقل اختيار الزبون
        self.person_combo = QComboBox()
        self.populate_persons_combo()
        form_layout.addRow("الزبون: *", self.person_combo)
        
        if self.person_id:
            # إذا تم تحديد الزبون مسبقًا، قم بتعيينه ومنع التغيير
            for i in range(self.person_combo.count()):
                if self.person_combo.itemData(i) == self.person_id:
                    self.person_combo.setCurrentIndex(i)
                    break
            self.person_combo.setEnabled(False)
        
        # مبلغ الدين
        self.amount_input = QDoubleSpinBox()
        self.amount_input.setRange(0.01, 999999999.99)
        self.amount_input.setDecimals(2)
        self.amount_input.setSuffix(" د.ع")
        form_layout.addRow("مبلغ الدين: *", self.amount_input)
        
        # وصف الدين
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("أدخل وصف الدين")
        self.description_input.setMinimumHeight(100)
        form_layout.addRow("وصف الدين: *", self.description_input)
        
        # تاريخ الاستحقاق
        self.due_date_input = QDateEdit()
        self.due_date_input.setDate(QDate.currentDate().addDays(30))  # افتراضي: بعد شهر
        self.due_date_input.setCalendarPopup(True)
        self.due_date_input.setDisplayFormat("yyyy-MM-dd")
        form_layout.addRow("تاريخ الاستحقاق:", self.due_date_input)
        
        # حالة الدفع
        self.is_paid_checkbox = QCheckBox("مدفوع")
        form_layout.addRow("", self.is_paid_checkbox)
        
        # ملاحظة الحقول المطلوبة
        note_label = QLabel("* الحقول المطلوبة")
        note_label.setObjectName("error-label")
        form_layout.addRow("", note_label)
        
        layout.addWidget(form_frame)

    def populate_persons_combo(self):
        """
        تعبئة قائمة الزبائن
        """
        self.person_combo.clear()
        self.person_combo.addItem("اختر زبون...", None)
        persons = self.person_controller.get_all_persons()
        if persons:
            for person in persons:
                self.person_combo.addItem(f"{person.name} ({person.phone})", person.id)
    
    def add_buttons(self, layout: QVBoxLayout):
        """
        إضافة أزرار الحفظ والإلغاء
        """
        buttons_frame = QFrame()
        buttons_layout = QHBoxLayout(buttons_frame)
        buttons_layout.setSpacing(10)
        
        save_text = "تحديث" if self.debt else "حفظ"
        self.save_btn = QPushButton(save_text)
        self.save_btn.setObjectName("edit-button")
        
        self.cancel_btn = QPushButton("إلغاء")
        # No objectName needed, will use default QPushButton style
        
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
        selected_person_id = self.person_combo.currentData()
        
        return {
            'person_id': selected_person_id,
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
        
        # التحقق من اختيار الزبون
        if not self.person_id and not data['person_id']:
            return False, "الرجاء اختيار زبون"
        
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
