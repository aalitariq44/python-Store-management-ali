# -*- coding: utf-8 -*-
"""
واجهة عرض جميع الديون في النظام
تحتوي على عرض وإضافة وتعديل وحذف الديون مع بيانات الزبائن
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QTableWidget, QTableWidgetItem, QLineEdit,
                             QLabel, QHeaderView, QFrame, QComboBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from controllers.debt_controller import DebtController
from controllers.person_controller import PersonController
from database.models import Debt
from utils.helpers import MessageHelper, AppHelper, TableHelper, DateHelper, NumberHelper
from views.dialogs.add_debt_dialog import AddDebtDialog


class DebtsView(QMainWindow):
    """
    واجهة عرض جميع الديون
    """
    
    def __init__(self):
        super().__init__()
        self.debt_controller = DebtController()
        self.person_controller = PersonController()
        self.selected_debt = None
        self.init_ui()
        self.setup_connections()
        self.load_debts()
    
    def init_ui(self):
        """
        تهيئة واجهة المستخدم
        """
        self.setWindowTitle("إدارة الديون")
        self.setMinimumSize(1200, 700)
        AppHelper.center_window(self, 1300, 800)
        
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
                background-color: #dc3545;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        
        title_layout = QVBoxLayout(title_frame)
        
        title_label = QLabel("إدارة الديون")
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
        
        subtitle_label = QLabel("عرض وإدارة جميع الديون في النظام")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("""
            QLabel {
                color: #f8d7da;
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
        self.status_filter.addItems(["الكل", "غير مدفوع", "مدفوع", "متأخر"])
        self.status_filter.setMaximumWidth(120)
        
        # الأزرار
        self.add_btn = QPushButton("إضافة دين")
        self.edit_btn = QPushButton("تعديل")
        self.delete_btn = QPushButton("حذف")
        self.mark_paid_btn = QPushButton("وضع علامة مدفوع")
        self.refresh_btn = QPushButton("تحديث")
        
        # تنسيق الأزرار
        buttons = [self.add_btn, self.edit_btn, self.delete_btn, self.mark_paid_btn, self.refresh_btn]
        for btn in buttons:
            btn.setMinimumHeight(35)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #dc3545;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    padding: 8px 16px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #c82333;
                }
                QPushButton:disabled {
                    background-color: #6c757d;
                }
            """)
        
        # تلوين أزرار خاصة
        self.edit_btn.setStyleSheet(self.edit_btn.styleSheet().replace("#dc3545", "#28a745").replace("#c82333", "#218838"))
        self.mark_paid_btn.setStyleSheet(self.mark_paid_btn.styleSheet().replace("#dc3545", "#007bff").replace("#c82333", "#0056b3"))
        
        # تعطيل الأزرار في البداية
        self.edit_btn.setEnabled(False)
        self.delete_btn.setEnabled(False)
        self.mark_paid_btn.setEnabled(False)
        
        # ترتيب العناصر
        toolbar_layout.addWidget(search_label)
        toolbar_layout.addWidget(self.search_input)
        toolbar_layout.addWidget(status_label)
        toolbar_layout.addWidget(self.status_filter)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.add_btn)
        toolbar_layout.addWidget(self.edit_btn)
        toolbar_layout.addWidget(self.delete_btn)
        toolbar_layout.addWidget(self.mark_paid_btn)
        toolbar_layout.addWidget(self.refresh_btn)
        
        layout.addWidget(toolbar_frame)
    
    def add_table(self, layout: QVBoxLayout):
        """
        إضافة جدول الديون
        """
        # إطار الجدول
        table_frame = QFrame()
        table_layout = QVBoxLayout(table_frame)
        
        # عنوان الجدول
        table_title = QLabel("قائمة الديون")
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
        headers = ["المعرف", "اسم الزبون", "المبلغ", "الوصف", "تاريخ الاستحقاق", "الحالة", "تاريخ الإضافة"]
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
                background-color: #dc3545;
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
        
        self.total_debts_label = QLabel("إجمالي الديون: -")
        self.unpaid_debts_label = QLabel("غير مدفوع: -")
        self.paid_debts_label = QLabel("مدفوع: -")
        self.overdue_debts_label = QLabel("متأخر: -")
        
        for label in [self.total_debts_label, self.unpaid_debts_label, 
                     self.paid_debts_label, self.overdue_debts_label]:
            label.setStyleSheet("""
                QLabel {
                    font-weight: bold;
                    color: #495057;
                }
            """)
        
        status_layout.addWidget(self.total_debts_label)
        status_layout.addWidget(self.unpaid_debts_label)
        status_layout.addWidget(self.paid_debts_label)
        status_layout.addWidget(self.overdue_debts_label)
        status_layout.addStretch()
        
        layout.addWidget(status_frame)
    
    def setup_connections(self):
        """
        إعداد الاتصالات والأحداث
        """
        # أحداث الأزرار
        self.add_btn.clicked.connect(self.add_debt)
        self.edit_btn.clicked.connect(self.edit_debt)
        self.delete_btn.clicked.connect(self.delete_debt)
        self.mark_paid_btn.clicked.connect(self.mark_debt_paid)
        self.refresh_btn.clicked.connect(self.load_debts)
        
        # أحداث الجدول
        self.table.selectionModel().selectionChanged.connect(self.on_selection_changed)
        self.table.doubleClicked.connect(self.edit_debt)
        
        # أحداث البحث والفلترة
        self.search_input.textChanged.connect(self.filter_debts)
        self.status_filter.currentTextChanged.connect(self.filter_debts)
    
    def load_debts(self):
        """
        تحميل قائمة الديون
        """
        try:
            debts = self.debt_controller.get_all_debts()
            self.all_debts = debts  # حفظ النسخة الأصلية للفلترة
            self.populate_table(debts)
            self.update_statistics()
        except Exception as e:
            MessageHelper.show_error(self, "خطأ", f"حدث خطأ أثناء تحميل البيانات: {str(e)}")
    
    def populate_table(self, debts: list):
        """
        ملء الجدول بالبيانات
        """
        self.table.setRowCount(len(debts))
        
        for row, debt in enumerate(debts):
            # إخفاء المعرف في عمود مخفي
            id_item = QTableWidgetItem(str(debt.id))
            id_item.setData(Qt.UserRole, debt)
            self.table.setItem(row, 0, id_item)
            
            # اسم الزبون
            self.table.setItem(row, 1, QTableWidgetItem(debt.person_name))
            
            # المبلغ
            amount_item = QTableWidgetItem(NumberHelper.format_currency(debt.amount))
            amount_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(row, 2, amount_item)
            
            # الوصف
            self.table.setItem(row, 3, QTableWidgetItem(debt.description))
            
            # تاريخ الاستحقاق
            due_date = DateHelper.format_date(debt.due_date) if debt.due_date else "غير محدد"
            self.table.setItem(row, 4, QTableWidgetItem(due_date))
            
            # الحالة
            status = "مدفوع" if debt.is_paid else "غير مدفوع"
            status_item = QTableWidgetItem(status)
            
            # تلوين الحالة
            if debt.is_paid:
                status_item.setBackground(Qt.green)
                status_item.setForeground(Qt.white)
            else:
                # فحص إذا كان متأخر
                from datetime import date
                if debt.due_date and debt.due_date < date.today():
                    status_item.setBackground(Qt.red)
                    status_item.setForeground(Qt.white)
                    status_item.setText("متأخر")
                else:
                    status_item.setBackground(Qt.yellow)
                    status_item.setForeground(Qt.black)
            
            self.table.setItem(row, 5, status_item)
            
            # تاريخ الإضافة
            created_date = DateHelper.format_datetime(debt.created_at) if debt.created_at else ""
            self.table.setItem(row, 6, QTableWidgetItem(created_date))
        
        # ضبط عرض الأعمدة
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # اسم الزبون
        header.setSectionResizeMode(3, QHeaderView.Stretch)  # الوصف
    
    def filter_debts(self):
        """
        فلترة الديون حسب البحث والحالة
        """
        if not hasattr(self, 'all_debts'):
            return
        
        search_term = self.search_input.text().strip().lower()
        status_filter = self.status_filter.currentText()
        
        filtered_debts = []
        
        for debt in self.all_debts:
            # فلترة النص
            if search_term:
                if not (search_term in debt.description.lower() or
                       search_term in debt.person_name.lower() or
                       search_term in str(debt.amount)):
                    continue
            
            # فلترة الحالة
            if status_filter == "مدفوع" and not debt.is_paid:
                continue
            elif status_filter == "غير مدفوع" and debt.is_paid:
                continue
            elif status_filter == "متأخر":
                from datetime import date
                if debt.is_paid or not debt.due_date or debt.due_date >= date.today():
                    continue
            
            filtered_debts.append(debt)
        
        self.populate_table(filtered_debts)
    
    def update_statistics(self):
        """
        تحديث الإحصائيات
        """
        try:
            stats = self.debt_controller.get_debt_statistics()
            
            self.total_debts_label.setText(
                f"إجمالي الديون: {stats['total_debts_count']} "
                f"({NumberHelper.format_currency(stats['total_unpaid_amount'] + stats['total_paid_amount'])})"
            )
            
            self.unpaid_debts_label.setText(
                f"غير مدفوع: {stats['unpaid_debts_count']} "
                f"({NumberHelper.format_currency(stats['total_unpaid_amount'])})"
            )
            
            self.paid_debts_label.setText(
                f"مدفوع: {stats['paid_debts_count']} "
                f"({NumberHelper.format_currency(stats['total_paid_amount'])})"
            )
            
            self.overdue_debts_label.setText(
                f"متأخر: {stats['overdue_debts_count']} "
                f"({NumberHelper.format_currency(stats['total_overdue_amount'])})"
            )
            
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
        
        if has_selection:
            # الحصول على الدين المحدد
            id_item = self.table.item(current_row, 0)
            if id_item:
                self.selected_debt = id_item.data(Qt.UserRole)
                # تفعيل زر "وضع علامة مدفوع" للديون غير المدفوعة فقط
                self.mark_paid_btn.setEnabled(self.selected_debt and not self.selected_debt.is_paid)
            else:
                self.selected_debt = None
                self.mark_paid_btn.setEnabled(False)
        else:
            self.selected_debt = None
            self.mark_paid_btn.setEnabled(False)
    
    def add_debt(self):
        """
        إضافة دين جديد
        """
        # أولاً نحتاج لاختيار الزبون
        persons = self.person_controller.get_all_persons()
        if not persons:
            MessageHelper.show_warning(self, "تنبيه", "يجب إضافة زبائن أولاً قبل إضافة الديون")
            return
        
        # يمكن إضافة نافذة اختيار الزبون هنا
        # لكن للبساطة سنفترض أن المستخدم سيختار من نافذة الديالوج
        
        dialog = AddDebtDialog(self)
        if dialog.exec_() == dialog.Accepted:
            debt_data = dialog.get_debt_data()
            
            # هنا نحتاج person_id - يمكن تحسين هذا لاحقاً
            if persons:
                person_id = persons[0].id  # مؤقت - يختار أول زبون
                
                success, message, debt_id = self.debt_controller.add_debt(
                    person_id,
                    debt_data['amount'],
                    debt_data['description'],
                    debt_data['due_date']
                )
                
                if success:
                    MessageHelper.show_info(self, "نجح", message)
                    self.load_debts()
                else:
                    MessageHelper.show_error(self, "خطأ", message)
    
    def edit_debt(self):
        """
        تعديل دين
        """
        if not self.selected_debt:
            return
        
        dialog = AddDebtDialog(self, self.selected_debt)
        if dialog.exec_() == dialog.Accepted:
            debt_data = dialog.get_debt_data()
            
            success, message = self.debt_controller.update_debt(
                self.selected_debt.id,
                debt_data['amount'],
                debt_data['description'],
                debt_data['due_date'],
                debt_data['is_paid']
            )
            
            if success:
                MessageHelper.show_info(self, "نجح", message)
                self.load_debts()
            else:
                MessageHelper.show_error(self, "خطأ", message)
    
    def delete_debt(self):
        """
        حذف دين
        """
        if not self.selected_debt:
            return
        
        reply = MessageHelper.show_question(
            self, "تأكيد الحذف",
            f"هل أنت متأكد من حذف هذا الدين؟\n"
            f"الوصف: {self.selected_debt.description}\n"
            f"المبلغ: {NumberHelper.format_currency(self.selected_debt.amount)}"
        )
        
        if reply:
            success, message = self.debt_controller.delete_debt(self.selected_debt.id)
            
            if success:
                MessageHelper.show_info(self, "نجح", message)
                self.load_debts()
            else:
                MessageHelper.show_error(self, "خطأ", message)
    
    def mark_debt_paid(self):
        """
        وضع علامة مدفوع على الدين
        """
        if not self.selected_debt or self.selected_debt.is_paid:
            return
        
        reply = MessageHelper.show_question(
            self, "تأكيد الدفع",
            f"هل تريد وضع علامة 'مدفوع' على هذا الدين؟\n"
            f"الوصف: {self.selected_debt.description}\n"
            f"المبلغ: {NumberHelper.format_currency(self.selected_debt.amount)}"
        )
        
        if reply:
            success, message = self.debt_controller.mark_debt_as_paid(self.selected_debt.id)
            
            if success:
                MessageHelper.show_info(self, "نجح", message)
                self.load_debts()
            else:
                MessageHelper.show_error(self, "خطأ", message)
