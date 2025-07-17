# -*- coding: utf-8 -*-
"""
نافذة حوار إضافة/تعديل اشتراك إنترنت
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
                             QLineEdit, QTextEdit, QPushButton, QLabel, QFrame,
                             QDateEdit, QDoubleSpinBox, QComboBox)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont
from datetime import date, timedelta
from database.models import InternetSubscription
from utils.helpers import MessageHelper, DateHelper
from controllers.person_controller import PersonController


class AddInternetDialog(QDialog):
    """
    نافذة حوار إضافة أو تعديل اشتراك إنترنت
    """
    
    def __init__(self, parent=None, subscription: InternetSubscription = None, person_id: int = None):
        super().__init__(parent)
        self.subscription = subscription
        self.person_id = person_id
        self.person_controller = PersonController()
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
        self.setMinimumSize(600, 600)
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
        title_frame.setStyleSheet("background-color: #27ae60;") # Custom green
        
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
        
        # اسم الباقة
        self.plan_name_input = QLineEdit()
        self.plan_name_input.setPlaceholderText("مثال: باقة الذهبية")
        form_layout.addRow("اسم الباقة: *", self.plan_name_input)
        
        # الرسوم الشهرية
        self.monthly_fee_input = QDoubleSpinBox()
        self.monthly_fee_input.setRange(0.00, 999999.99)
        self.monthly_fee_input.setDecimals(2)
        self.monthly_fee_input.setSuffix(" د.ع")
        form_layout.addRow("الرسوم الشهرية:", self.monthly_fee_input)
        
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
        
        save_text = "تحديث" if self.subscription else "حفظ"
        self.save_btn = QPushButton(save_text)
        self.save_btn.setObjectName("edit-button")
        
        self.cancel_btn = QPushButton("إلغاء")
        # Default style is fine
        
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
            
            if self.subscription.start_date:
                qdate = DateHelper.date_to_qdate(self.subscription.start_date)
                if qdate:
                    self.start_date_input.setDate(qdate)
    
    def get_subscription_data(self) -> dict:
        """
        الحصول على بيانات الاشتراك من النموذج
        """
        start_date = DateHelper.qdate_to_date(self.start_date_input.date())
        # تاريخ النهاية يكون بعد 30 يوم من تاريخ البداية
        end_date = start_date + timedelta(days=30) if start_date else None
        selected_person_id = self.person_combo.currentData()
        
        # يتم تحديد حالة النشاط تلقائيًا بناءً على التواريخ
        is_active = False
        if start_date and end_date:
            today = date.today()
            is_active = start_date <= today <= end_date

        return {
            'person_id': selected_person_id,
            'plan_name': self.plan_name_input.text().strip(),
            'monthly_fee': self.monthly_fee_input.value(),
            'speed': None,  # تم حذف حقل السرعة
            'start_date': start_date,
            'end_date': end_date,
            'is_active': is_active
        }
    
    def validate_data(self) -> tuple[bool, str]:
        """
        التحقق من صحة البيانات
        """
        data = self.get_subscription_data()
        
        # التحقق من اختيار الزبون
        if not self.person_id and not data['person_id']:
            return False, "الرجاء اختيار زبون"
        
        if not data['plan_name']:
            return False, "اسم الباقة مطلوب"
        
        if len(data['plan_name']) > 100:
            return False, "اسم الباقة طويل جداً (أكثر من 100 حرف)"
        
        if data['monthly_fee'] < 0:
            return False, "الرسوم الشهرية لا يمكن أن تكون سالبة"
        
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
