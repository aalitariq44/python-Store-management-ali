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
from controllers.person_controller import PersonController


class AddInstallmentDialog(QDialog):
    """
    نافذة حوار إضافة أو تعديل قسط
    """
    
    def __init__(self, parent=None, installment: Installment = None, person_id: int = None):
        super().__init__(parent)
        self.installment = installment
        self.person_id = person_id
        if self.installment and self.installment.person_id:
            self.person_id = self.installment.person_id
        self.person_controller = PersonController()
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
        self.setMinimumSize(600, 700) # استخدام حجم أدنى
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
        # Override background color for this specific dialog
        title_frame.setStyleSheet("background-color: var(--warning-color);")
        
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
        
        # المبلغ الإجمالي
        self.total_amount_input = QDoubleSpinBox()
        self.total_amount_input.setRange(0.01, 999999999.99)
        self.total_amount_input.setDecimals(2)
        self.total_amount_input.setSuffix(" د.ع")
        form_layout.addRow("المبلغ الإجمالي: *", self.total_amount_input)
        
        
        
        
        # وصف القسط
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("أدخل وصف القسط")
        self.description_input.setMinimumHeight(100)
        form_layout.addRow("وصف القسط: *", self.description_input)
        
        # تاريخ البداية
        self.start_date_input = QDateEdit()
        self.start_date_input.setDate(QDate.currentDate())
        self.start_date_input.setCalendarPopup(True)
        self.start_date_input.setDisplayFormat("yyyy-MM-dd")
        form_layout.addRow("تاريخ البداية:", self.start_date_input)
        
        
        
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
        
        save_text = "تحديث" if self.installment else "حفظ"
        self.save_btn = QPushButton(save_text)
        self.save_btn.setObjectName("edit-button")
        
        self.cancel_btn = QPushButton("إلغاء")
        # No objectName needed for default style
        
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
    
    def load_installment_data(self):
        """
        تحميل بيانات القسط للتعديل
        """
        if self.installment:
            self.total_amount_input.setValue(self.installment.total_amount)
            self.description_input.setPlainText(self.installment.description)
            
            if self.installment.start_date:
                qdate = DateHelper.date_to_qdate(self.installment.start_date)
                if qdate:
                    self.start_date_input.setDate(qdate)
            
    
    def get_installment_data(self) -> dict:
        """
        الحصول على بيانات القسط من النموذج
        """
        start_date = DateHelper.qdate_to_date(self.start_date_input.date())
        selected_person_id = self.person_combo.currentData()
        
        # Use self.person_id if it's available (especially in edit mode)
        person_id_to_use = selected_person_id if selected_person_id is not None else self.person_id

        return {
            'person_id': person_id_to_use,
            'total_amount': self.total_amount_input.value(),
            'description': self.description_input.toPlainText().strip(),
            'start_date': start_date,
        }
    
    def validate_data(self) -> tuple[bool, str]:
        """
        التحقق من صحة البيانات
        """
        data = self.get_installment_data()
        
        # التحقق من اختيار الزبون
        if not self.person_id and not data['person_id']:
            return False, "الرجاء اختيار زبون"
        
        if data['total_amount'] <= 0:
            return False, "المبلغ الإجمالي يجب أن يكون أكبر من صفر"
        
        if not data['description']:
            return False, "وصف القسط مطلوب"
        
        if len(data['description']) > 200:
            return False, "وصف القسط طويل جداً (أكثر من 200 حرف)"
        
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
