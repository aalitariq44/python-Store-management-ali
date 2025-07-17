# -*- coding: utf-8 -*-
"""
واجهة عرض جميع الأقساط في النظام
تحتوي على عرض وإدارة جميع الأقساط مع بيانات الزبائن
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QTableWidget, QTableWidgetItem, QLineEdit,
                             QLabel, QHeaderView, QFrame, QComboBox, QProgressBar)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from controllers.installment_controller import InstallmentController
from controllers.person_controller import PersonController
from database.models import Installment
from utils.helpers import MessageHelper, AppHelper, TableHelper, DateHelper, NumberHelper
from views.dialogs.add_installment_dialog import AddInstallmentDialog
from views.dialogs.installment_details_dialog import InstallmentDetailsDialog


class InstallmentsView(QMainWindow):
    """
    واجهة عرض جميع الأقساط
    """
    
    def __init__(self):
        super().__init__()
        self.installment_controller = InstallmentController()
        self.person_controller = PersonController()
        self.selected_installment = None
        self.init_ui()
        self.setup_connections()
        self.load_installments()
    
    def init_ui(self):
        """
        تهيئة واجهة المستخدم
        """
        self.setWindowTitle("إدارة الأقساط")
        self.setMinimumSize(1400, 700)
        AppHelper.center_window(self, 1500, 800)
        
        # القطعة المركزية
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # التخطيط الرئيسي
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # إضافة العنوان
        self.add_title(main_layout)
        
        # إضافة شريط البحث والأدوات
        self.add_toolbar(main_layout)
        
        # إضافة الجدول
        self.add_table(main_layout)
        
        # إضافة شريط الحالة
        self.add_status_bar(main_layout)
    
    def add_title(self, layout: QVBoxLayout):
        """
        إضافة عنوان الصفحة
        """
        title_frame = QFrame()
        title_frame.setStyleSheet("""
            QFrame {
                background-color: #f39c12;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        
        title_layout = QVBoxLayout(title_frame)
        
        title_label = QLabel("إدارة الأقساط")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                background: transparent;
            }
        """)
        title_layout.addWidget(title_label)
        
        subtitle_label = QLabel("عرض وإدارة جميع الأقساط في النظام")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("""
            QLabel {
                color: #fdf2e9;
                font-size: 14px;
                background: transparent;
            }
        """)
        title_layout.addWidget(subtitle_label)
        
        layout.addWidget(title_frame)
    
    def add_toolbar(self, layout: QVBoxLayout):
        """
        إضافة شريط الأدوات
        """
        toolbar_frame = QFrame()
        toolbar_layout = QHBoxLayout(toolbar_frame)
        
        # شريط البحث
        search_label = QLabel("البحث:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("ابحث في الوصف أو اسم الزبون أو المبلغ...")
        self.search_input.setMaximumWidth(300)
        
        # فلتر الحالة
        status_label = QLabel("الحالة:")
        self.status_filter = QComboBox()
        self.status_filter.addItems(["الكل", "نشط", "مكتمل"])
        self.status_filter.setMaximumWidth(120)
        
        # فلتر الدورية
        frequency_label = QLabel("الدورية:")
        self.frequency_filter = QComboBox()
        self.frequency_filter.addItems(["الكل", "شهري", "أسبوعي", "سنوي"])
        self.frequency_filter.setMaximumWidth(120)
        
        # الأزرار
        self.add_btn = QPushButton("إضافة قسط")
        self.edit_btn = QPushButton("تعديل")
        self.delete_btn = QPushButton("حذف")
        self.add_payment_btn = QPushButton("إضافة دفعة")
        self.details_btn = QPushButton("عرض التفاصيل")
        self.refresh_btn = QPushButton("تحديث")
        
        # تنسيق الأزرار
        buttons = [self.add_btn, self.edit_btn, self.delete_btn, self.add_payment_btn, self.details_btn, self.refresh_btn]
        for btn in buttons:
            btn.setMinimumHeight(35)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #f39c12;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    padding: 8px 16px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #e67e22;
                }
                QPushButton:disabled {
                    background-color: #6c757d;
                }
            """)
        
        # تلوين أزرار خاصة
        self.edit_btn.setStyleSheet(self.edit_btn.styleSheet().replace("#f39c12", "#28a745").replace("#e67e22", "#218838"))
        self.delete_btn.setStyleSheet(self.delete_btn.styleSheet().replace("#f39c12", "#dc3545").replace("#e67e22", "#c82333"))
        self.add_payment_btn.setStyleSheet(self.add_payment_btn.styleSheet().replace("#f39c12", "#007bff").replace("#e67e22", "#0056b3"))
        
        # تعطيل الأزرار في البداية
        self.edit_btn.setEnabled(False)
        self.delete_btn.setEnabled(False)
        self.add_payment_btn.setEnabled(False)
        self.details_btn.setEnabled(False)
        
        # ترتيب العناصر
        toolbar_layout.addWidget(search_label)
        toolbar_layout.addWidget(self.search_input)
        toolbar_layout.addWidget(status_label)
        toolbar_layout.addWidget(self.status_filter)
        toolbar_layout.addWidget(frequency_label)
        toolbar_layout.addWidget(self.frequency_filter)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.add_btn)
        toolbar_layout.addWidget(self.edit_btn)
        toolbar_layout.addWidget(self.delete_btn)
        toolbar_layout.addWidget(self.add_payment_btn)
        toolbar_layout.addWidget(self.details_btn)
        toolbar_layout.addWidget(self.refresh_btn)
        
        layout.addWidget(toolbar_frame)
    
    def add_table(self, layout: QVBoxLayout):
        """
        إضافة جدول الأقساط
        """
        # إطار الجدول
        table_frame = QFrame()
        table_layout = QVBoxLayout(table_frame)
        
        # عنوان الجدول
        table_title = QLabel("قائمة الأقساط")
        table_title.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #495057;
                margin-bottom: 10px;
            }
        """)
        table_layout.addWidget(table_title)
        
        # الجدول
        self.table = QTableWidget()
        headers = ["المعرف", "اسم الزبون", "المبلغ الإجمالي", 
                  "الدورية", "الوصف", "نسبة الإنجاز", "الحالة", "تاريخ البداية"]
        TableHelper.setup_table_headers(self.table, headers)
        
        # تنسيق الجدول
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setStyleSheet("""
            QTableWidget {
                gridline-color: #dee2e6;
                background-color: white;
                alternate-background-color: #f8f9fa;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #dee2e6;
            }
            QTableWidget::item:selected {
                background-color: #f39c12;
                color: white;
            }
        """)
        
        # إخفاء عمود المعرف
        self.table.setColumnHidden(0, True)
        
        table_layout.addWidget(self.table)
        layout.addWidget(table_frame)
    
    def add_status_bar(self, layout: QVBoxLayout):
        """
        إضافة شريط الحالة مع الإحصائيات
        """
        status_frame = QFrame()
        status_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        
        status_layout = QHBoxLayout(status_frame)
        
        self.total_installments_label = QLabel("إجمالي الأقساط: -")
        self.active_installments_label = QLabel("نشط: -")
        self.completed_installments_label = QLabel("مكتمل: -")
        self.total_amount_label = QLabel("إجمالي المبالغ: -")
        self.paid_amount_label = QLabel("المدفوع: -")
        
        for label in [self.total_installments_label, self.active_installments_label, 
                     self.completed_installments_label, self.total_amount_label, self.paid_amount_label]:
            label.setStyleSheet("""
                QLabel {
                    font-weight: bold;
                    color: #495057;
                }
            """)
        
        status_layout.addWidget(self.total_installments_label)
        status_layout.addWidget(self.active_installments_label)
        status_layout.addWidget(self.completed_installments_label)
        status_layout.addWidget(self.total_amount_label)
        status_layout.addWidget(self.paid_amount_label)
        status_layout.addStretch()
        
        layout.addWidget(status_frame)
    
    def setup_connections(self):
        """
        إعداد الاتصالات والأحداث
        """
        # أحداث الأزرار
        self.add_btn.clicked.connect(self.add_installment)
        self.edit_btn.clicked.connect(self.edit_installment)
        self.delete_btn.clicked.connect(self.delete_installment)
        self.add_payment_btn.clicked.connect(self.add_payment)
        self.details_btn.clicked.connect(self.show_installment_details)
        self.refresh_btn.clicked.connect(self.load_installments)
        
        # أحداث الجدول
        self.table.selectionModel().selectionChanged.connect(self.on_selection_changed)
        self.table.doubleClicked.connect(self.edit_installment)
        
        # أحداث البحث والفلترة
        self.search_input.textChanged.connect(self.filter_installments)
        self.status_filter.currentTextChanged.connect(self.filter_installments)
        self.frequency_filter.currentTextChanged.connect(self.filter_installments)
    
    def load_installments(self):
        """
        تحميل قائمة الأقساط
        """
        try:
            installments = self.installment_controller.get_all_installments()
            self.all_installments = installments  # حفظ النسخة الأصلية للفلترة
            self.populate_table(installments)
            self.update_statistics()
        except Exception as e:
            MessageHelper.show_error(self, "خطأ", f"حدث خطأ أثناء تحميل البيانات: {str(e)}")
    
    def populate_table(self, installments: list):
        """
        ملء الجدول بالبيانات
        """
        self.table.setRowCount(len(installments))
        
        for row, installment in enumerate(installments):
            # إخفاء المعرف في عمود مخفي
            id_item = QTableWidgetItem(str(installment.id))
            id_item.setData(Qt.UserRole, installment)
            self.table.setItem(row, 0, id_item)
            
            # اسم الزبون
            self.table.setItem(row, 1, QTableWidgetItem(installment.person_name))
            
            # المبلغ الإجمالي
            total_item = QTableWidgetItem(NumberHelper.format_currency(installment.total_amount))
            total_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(row, 2, total_item)
            
            # الدورية
            frequency_map = {"monthly": "شهري", "weekly": "أسبوعي", "yearly": "سنوي"}
            frequency_text = frequency_map.get(installment.frequency, installment.frequency)
            self.table.setItem(row, 3, QTableWidgetItem(frequency_text))
            
            # الوصف
            self.table.setItem(row, 4, QTableWidgetItem(installment.description))
            
            # نسبة الإنجاز
            percentage = NumberHelper.format_percentage(installment.completion_percentage)
            progress_item = QTableWidgetItem(percentage)
            progress_item.setTextAlignment(Qt.AlignCenter)
            
            # تلوين نسبة الإنجاز
            if installment.completion_percentage >= 100:
                progress_item.setBackground(Qt.green)
                progress_item.setForeground(Qt.white)
            elif installment.completion_percentage >= 50:
                progress_item.setBackground(Qt.yellow)
                progress_item.setForeground(Qt.black)
            else:
                progress_item.setBackground(Qt.red)
                progress_item.setForeground(Qt.white)
            
            self.table.setItem(row, 5, progress_item)
            
            # الحالة
            status = "مكتمل" if installment.is_completed else "نشط"
            status_item = QTableWidgetItem(status)
            
            if installment.is_completed:
                status_item.setBackground(Qt.green)
                status_item.setForeground(Qt.white)
            else:
                status_item.setBackground(Qt.blue)
                status_item.setForeground(Qt.white)
            
            self.table.setItem(row, 6, status_item)
            
            # تاريخ البداية
            start_date = DateHelper.format_date(installment.start_date) if installment.start_date else "غير محدد"
            self.table.setItem(row, 7, QTableWidgetItem(start_date))
        
        # ضبط عرض الأعمدة
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # اسم الزبون
        header.setSectionResizeMode(6, QHeaderView.Stretch)  # الوصف
    
    def filter_installments(self):
        """
        فلترة الأقساط حسب البحث والحالة والدورية
        """
        if not hasattr(self, 'all_installments'):
            return
        
        search_term = self.search_input.text().strip().lower()
        status_filter = self.status_filter.currentText()
        frequency_filter = self.frequency_filter.currentText()
        
        filtered_installments = []
        
        for installment in self.all_installments:
            # فلترة النص
            if search_term:
                if not (search_term in installment.description.lower() or
                       search_term in installment.person_name.lower() or
                       search_term in str(installment.total_amount)):
                    continue
            
            # فلترة الحالة
            if status_filter == "نشط" and installment.is_completed:
                continue
            elif status_filter == "مكتمل" and not installment.is_completed:
                continue
            
            # فلترة الدورية
            frequency_map = {"شهري": "monthly", "أسبوعي": "weekly", "سنوي": "yearly"}
            if frequency_filter != "الكل":
                expected_frequency = frequency_map.get(frequency_filter)
                if expected_frequency and installment.frequency != expected_frequency:
                    continue
            
            filtered_installments.append(installment)
        
        self.populate_table(filtered_installments)
    
    def update_statistics(self):
        """
        تحديث الإحصائيات
        """
        try:
            stats = self.installment_controller.get_installment_statistics()
            
            self.total_installments_label.setText(f"إجمالي الأقساط: {stats['total_installments_count']}")
            self.active_installments_label.setText(f"نشط: {stats['active_installments_count']}")
            self.completed_installments_label.setText(f"مكتمل: {stats['completed_installments_count']}")
            self.total_amount_label.setText(f"إجمالي المبالغ: {NumberHelper.format_currency(stats['total_amount'])}")
            self.paid_amount_label.setText(f"المدفوع: {NumberHelper.format_currency(stats['total_paid_amount'])}")
            
        except Exception as e:
            print(f"خطأ في تحديث الإحصائيات: {str(e)}")
    
    def on_selection_changed(self):
        """
        معالجة تغيير التحديد في الجدول
        """
        current_row = self.table.currentRow()
        has_selection = current_row >= 0
        
        # تفعيل/تعطيل الأزرار
        self.edit_btn.setEnabled(has_selection)
        self.delete_btn.setEnabled(has_selection)
        self.details_btn.setEnabled(has_selection)
        
        if has_selection:
            # الحصول على القسط المحدد
            id_item = self.table.item(current_row, 0)
            if id_item:
                self.selected_installment = id_item.data(Qt.UserRole)
                # تفعيل زر "إضافة دفعة" للأقساط غير المكتملة فقط
                self.add_payment_btn.setEnabled(
                    self.selected_installment and not self.selected_installment.is_completed
                )
            else:
                self.selected_installment = None
                self.add_payment_btn.setEnabled(False)
        else:
            self.selected_installment = None
            self.add_payment_btn.setEnabled(False)
    
    def add_installment(self):
        """
        إضافة قسط جديد
        """
        persons = self.person_controller.get_all_persons()
        if not persons:
            MessageHelper.show_warning(self, "تنبيه", "يجب إضافة زبائن أولاً قبل إضافة الأقساط")
            return
        
        dialog = AddInstallmentDialog(self)
        if dialog.exec_() == dialog.Accepted:
            installment_data = dialog.get_installment_data()
            
            person_id = installment_data.get('person_id')
            if not person_id:
                MessageHelper.show_error(self, "خطأ", "لم يتم اختيار زبون.")
                return

            success, message, installment_id = self.installment_controller.add_installment(
                person_id,
                installment_data['total_amount'],
                installment_data['frequency'],
                installment_data['description'],
                installment_data['start_date']
            )
            
            if success:
                MessageHelper.show_info(self, "نجح", message)
                self.load_installments()
            else:
                MessageHelper.show_error(self, "خطأ", message)
    
    def edit_installment(self):
        """
        تعديل قسط
        """
        if not self.selected_installment:
            return
        
        dialog = AddInstallmentDialog(self, self.selected_installment)
        if dialog.exec_() == dialog.Accepted:
            installment_data = dialog.get_installment_data()
            
            success, message = self.installment_controller.update_installment(
                self.selected_installment.id,
                installment_data['total_amount'],
                installment_data['frequency'],
                installment_data['description'],
                installment_data['start_date']
            )
            
            if success:
                MessageHelper.show_info(self, "نجح", message)
                self.load_installments()
            else:
                MessageHelper.show_error(self, "خطأ", message)
    
    def delete_installment(self):
        """
        حذف قسط
        """
        if not self.selected_installment:
            return
        
        reply = MessageHelper.show_question(
            self, "تأكيد الحذف",
            f"هل أنت متأكد من حذف هذا القسط؟\n"
            f"الوصف: {self.selected_installment.description}\n"
            f"المبلغ الإجمالي: {NumberHelper.format_currency(self.selected_installment.total_amount)}"
        )
        
        if reply:
            success, message = self.installment_controller.delete_installment(self.selected_installment.id)
            
            if success:
                MessageHelper.show_info(self, "نجح", message)
                self.load_installments()
            else:
                MessageHelper.show_error(self, "خطأ", message)
    
    def show_installment_details(self):
        """
        عرض تفاصيل القسط المحدد
        """
        if not self.selected_installment:
            return
        
        dialog = InstallmentDetailsDialog(self.selected_installment, self)
        dialog.exec_()

    def add_payment(self):
        """
        إضافة دفعة للقسط
        """
        if not self.selected_installment or self.selected_installment.is_completed:
            return
        
        from PyQt5.QtWidgets import QInputDialog
        
        remaining = self.selected_installment.remaining_amount
        payment_amount, ok = QInputDialog.getDouble(
            self, "إضافة دفعة", 
            f"أدخل مبلغ الدفعة:\n"
            f"المبلغ المتبقي: {NumberHelper.format_currency(remaining)}",
            0.0, 0.0, remaining, 2
        )
        
        if ok and payment_amount > 0:
            success, message = self.installment_controller.add_payment(
                self.selected_installment.id, payment_amount
            )
            
            if success:
                MessageHelper.show_info(self, "نجح", message)
                self.load_installments()
            else:
                MessageHelper.show_error(self, "خطأ", message)
