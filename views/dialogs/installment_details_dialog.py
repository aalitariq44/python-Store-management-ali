# -*- coding: utf-8 -*-
"""
نافذة عرض تفاصيل القسط
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QProgressBar, QFrame, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox)
from PyQt5.QtCore import Qt
from database.models import Installment, Payment
from database.queries import PaymentQueries
from database.database_connection import DatabaseConnection
from utils.helpers import NumberHelper, DateHelper
from datetime import date

class InstallmentDetailsDialog(QDialog):
    """
    نافذة منبثقة لعرض تفاصيل قسط معين
    """
    
    def __init__(self, installment: Installment, db_connection: DatabaseConnection, parent=None):
        super().__init__(parent)
        self.installment = installment
        self.db_connection = db_connection
        self.payment_queries = PaymentQueries(self.db_connection)
        self.setWindowTitle("تفاصيل القسط")
        self.setMinimumWidth(600)
        self.main_layout = QVBoxLayout(self)
        self.init_ui()
        self.load_payments()

    def init_ui(self):
        """
        تهيئة واجهة المستخدم
        """
        self.main_layout.setSpacing(15)
        
        # إضافة التفاصيل
        self.add_details_section(self.main_layout)
        
        # إضافة قسم المبالغ
        self.add_amounts_section(self.main_layout)
        
        # إضافة شريط التقدم
        self.add_progress_section(self.main_layout)
        
        # إضافة قسم الدفعات
        self.add_payments_section(self.main_layout)
        
        # إضافة زر الإغلاق
        self.add_close_button(self.main_layout)

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
        self.amounts_frame = QFrame()
        self.amounts_frame.setFrameShape(QFrame.StyledPanel)
        amounts_layout = QVBoxLayout(self.amounts_frame)
        
        self.total_amount_label = self.create_info_label("المبلغ الإجمالي:", NumberHelper.format_currency(self.installment.total_amount), "font-size: 16px; color: #2c3e50;")
        self.paid_amount_label = self.create_info_label("المبلغ المدفوع:", NumberHelper.format_currency(self.installment.paid_amount), "font-size: 16px; color: #27ae60;")
        self.remaining_amount_label = self.create_info_label("المبلغ المتبقي:", NumberHelper.format_currency(self.installment.remaining_amount), "font-size: 16px; color: #c0392b;")
        
        amounts_layout.addWidget(self.total_amount_label)
        amounts_layout.addWidget(self.paid_amount_label)
        amounts_layout.addWidget(self.remaining_amount_label)
        
        layout.addWidget(self.amounts_frame)

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

    def add_payments_section(self, layout: QVBoxLayout):
        """
        إضافة قسم الدفعات
        """
        payments_frame = QFrame()
        payments_frame.setFrameShape(QFrame.StyledPanel)
        payments_layout = QVBoxLayout(payments_frame)

        title_label = QLabel("سجل الدفعات")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        payments_layout.addWidget(title_label)

        self.payments_table = QTableWidget()
        self.payments_table.setColumnCount(4)
        self.payments_table.setHorizontalHeaderLabels(["المبلغ", "تاريخ الدفعة", "تاريخ التسجيل", ""])
        self.payments_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.payments_table.setEditTriggers(QTableWidget.NoEditTriggers)
        payments_layout.addWidget(self.payments_table)

        add_payment_button = QPushButton("إضافة دفعة")
        add_payment_button.clicked.connect(self.add_payment)
        payments_layout.addWidget(add_payment_button)

        layout.addWidget(payments_frame)

    def load_payments(self):
        """
        تحميل الدفعات من قاعدة البيانات وعرضها في الجدول
        """
        payments = self.payment_queries.get_payments_by_installment(self.installment.id)
        self.payments_table.setRowCount(len(payments))

        for row, payment in enumerate(payments):
            self.payments_table.setItem(row, 0, QTableWidgetItem(NumberHelper.format_currency(payment.amount)))
            self.payments_table.setItem(row, 1, QTableWidgetItem(DateHelper.format_date(payment.payment_date)))
            self.payments_table.setItem(row, 2, QTableWidgetItem(DateHelper.format_datetime(payment.created_at)))

            delete_button = QPushButton("حذف")
            delete_button.clicked.connect(lambda _, p=payment.id: self.delete_payment(p))
            self.payments_table.setCellWidget(row, 3, delete_button)

    def add_payment(self):
        """
        إضافة دفعة جديدة
        """
        # هنا يمكن فتح نافذة جديدة لإضافة دفعة
        # حاليا سنضيف دفعة افتراضية كمثال
        new_payment = Payment(
            installment_id=self.installment.id,
            amount=self.installment.installment_amount,
            payment_date=date.today()
        )
        payment_id = self.payment_queries.create_payment(new_payment)
        if payment_id:
            # تحديث المبلغ المدفوع في القسط
            self.installment.paid_amount += new_payment.amount
            # يمكنك استدعاء دالة لتحديث القسط في قاعدة البيانات هنا
            self.load_payments()
            # تحديث واجهة المستخدم
            self.update_amounts_display()

    def delete_payment(self, payment_id: int):
        """
        حذف دفعة
        """
        reply = QMessageBox.question(self, 'تأكيد الحذف', 'هل أنت متأكد من حذف هذه الدفعة؟',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            # قبل الحذف، يجب استعادة المبلغ المدفوع من القسط
            # هذه الخطوة تحتاج إلى الحصول على تفاصيل الدفعة قبل حذفها
            # حاليا، سنقوم بالحذف مباشرة
            if self.payment_queries.delete_payment(payment_id):
                QMessageBox.information(self, "نجاح", "تم حذف الدفعة بنجاح.")
                self.load_payments()
                # يجب تحديث المبلغ المدفوع في القسط وواجهة المستخدم
            else:
                QMessageBox.critical(self, "خطأ", "فشل حذف الدفعة.")

    def update_amounts_display(self):
        """
        تحديث عرض المبالغ
        """
        self.total_amount_label.setText(f"<b>المبلغ الإجمالي:</b> {NumberHelper.format_currency(self.installment.total_amount)}")
        self.paid_amount_label.setText(f"<b>المبلغ المدفوع:</b> {NumberHelper.format_currency(self.installment.paid_amount)}")
        self.remaining_amount_label.setText(f"<b>المبلغ المتبقي:</b> {NumberHelper.format_currency(self.installment.remaining_amount)}")
        self.progress_bar.setValue(int(self.installment.completion_percentage))
