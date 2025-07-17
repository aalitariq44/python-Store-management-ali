# -*- coding: utf-8 -*-
"""
نافذة عرض تفاصيل القسط
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QProgressBar, QFrame, QPushButton)
from PyQt5.QtCore import Qt
from database.models import Installment
from utils.helpers import NumberHelper, DateHelper

class InstallmentDetailsDialog(QDialog):
    """
    نافذة منبثقة لعرض تفاصيل قسط معين
    """
    
    def __init__(self, installment: Installment, parent=None):
        super().__init__(parent)
        self.installment = installment
        self.setWindowTitle("تفاصيل القسط")
        self.setMinimumWidth(500)
        self.init_ui()

    def init_ui(self):
        """
        تهيئة واجهة المستخدم
        """
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        
        # إضافة التفاصيل
        self.add_details_section(main_layout)
        
        # إضافة قسم المبالغ
        self.add_amounts_section(main_layout)
        
        # إضافة شريط التقدم
        self.add_progress_section(main_layout)
        
        # إضافة زر الإغلاق
        self.add_close_button(main_layout)

    def add_details_section(self, layout: QVBoxLayout):
        """
        إضافة قسم التفاصيل الأساسية
        """
        details_frame = QFrame()
        details_frame.setFrameShape(QFrame.StyledPanel)
        details_layout = QVBoxLayout(details_frame)
        
        details_layout.addWidget(self.create_info_label("الزبون:", self.installment.person_name))
        details_layout.addWidget(self.create_info_label("الوصف:", self.installment.description))
        
        frequency_map = {"monthly": "شهري", "weekly": "أسبوعي", "yearly": "سنوي"}
        frequency_text = frequency_map.get(self.installment.frequency, self.installment.frequency)
        details_layout.addWidget(self.create_info_label("الدورية:", frequency_text))
        
        start_date = DateHelper.format_date(self.installment.start_date) if self.installment.start_date else "غير محدد"
        details_layout.addWidget(self.create_info_label("تاريخ البداية:", start_date))
        
        status = "مكتمل" if self.installment.is_completed else "نشط"
        details_layout.addWidget(self.create_info_label("الحالة:", status))
        
        layout.addWidget(details_frame)

    def add_amounts_section(self, layout: QVBoxLayout):
        """
        إضافة قسم المبالغ
        """
        amounts_frame = QFrame()
        amounts_frame.setFrameShape(QFrame.StyledPanel)
        amounts_layout = QVBoxLayout(amounts_frame)
        
        amounts_layout.addWidget(self.create_info_label("المبلغ الإجمالي:", NumberHelper.format_currency(self.installment.total_amount), "font-size: 16px; color: #2c3e50;"))
        amounts_layout.addWidget(self.create_info_label("المبلغ المدفوع:", NumberHelper.format_currency(self.installment.paid_amount), "font-size: 16px; color: #27ae60;"))
        amounts_layout.addWidget(self.create_info_label("المبلغ المتبقي:", NumberHelper.format_currency(self.installment.remaining_amount), "font-size: 16px; color: #c0392b;"))
        
        layout.addWidget(amounts_frame)

    def add_progress_section(self, layout: QVBoxLayout):
        """
        إضافة قسم شريط التقدم
        """
        progress_layout = QHBoxLayout()
        
        progress_label = QLabel("نسبة الإنجاز:")
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(int(self.installment.completion_percentage))
        self.progress_bar.setAlignment(Qt.AlignCenter)
        
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid grey;
                border-radius: 5px;
                text-align: center;
                height: 25px;
            }
            QProgressBar::chunk {
                background-color: #f39c12;
                width: 20px;
            }
        """)
        
        progress_layout.addWidget(progress_label)
        progress_layout.addWidget(self.progress_bar)
        
        layout.addLayout(progress_layout)

    def add_close_button(self, layout: QVBoxLayout):
        """
        إضافة زر الإغلاق
        """
        close_btn = QPushButton("إغلاق")
        close_btn.clicked.connect(self.accept)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #7f8c8d;
                color: white;
                border-radius: 5px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #95a5a6;
            }
        """)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(close_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)

    def create_info_label(self, title: str, value: str, style: str = "") -> QLabel:
        """
        إنشاء ملصق لعرض معلومة
        """
        label = QLabel(f"<b>{title}</b> {value}")
        label.setTextFormat(Qt.RichText)
        if style:
            label.setStyleSheet(style)
        return label
