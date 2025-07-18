# -*- coding: utf-8 -*-
"""
واجهة إدارة الزبائن
تحتوي على عرض وإضافة وتعديل وحذف الزبائن
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QTableWidget, QTableWidgetItem, QLineEdit,
                             QLabel, QHeaderView, QFrame, QSplitter, QTextEdit)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from controllers.person_controller import PersonController
from database.models import Person
from utils.helpers import MessageHelper, AppHelper, TableHelper
from views.dialogs.add_person_dialog import AddPersonDialog


class PersonsView(QMainWindow):
    """
    واجهة إدارة الزبائن
    """
    
    # إشارة لتحديث البيانات
    person_updated = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.controller = PersonController()
        self.selected_person = None
        self.init_ui()
        self.setup_connections()
        self.load_persons()
    
    def init_ui(self):
        """
        تهيئة واجهة المستخدم
        """
        self.setWindowTitle("إدارة الزبائن")
        self.setMinimumSize(1000, 600)
        AppHelper.center_window(self, 1200, 700)
        
        # القطعة المركزية
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # التخطيط الرئيسي
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # إضافة شريط البحث والأزرار
        self.add_toolbar(main_layout)
        
        # إضافة الجدول ولوحة التفاصيل
        self.add_content_area(main_layout)
    
    def add_toolbar(self, layout: QVBoxLayout):
        """
        إضافة شريط الأدوات
        
        Args:
            layout: التخطيط
        """
        toolbar_frame = QFrame()
        toolbar_layout = QHBoxLayout(toolbar_frame)
        
        # شريط البحث
        search_label = QLabel("البحث:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("ابحث بالاسم أو رقم الهاتف أو العنوان...")
        self.search_input.setMaximumWidth(300)
        
        # الأزرار
        self.add_btn = QPushButton("إضافة زبون")
        self.edit_btn = QPushButton("تعديل")
        self.delete_btn = QPushButton("حذف")
        self.details_btn = QPushButton("عرض التفاصيل")
        self.refresh_btn = QPushButton("تحديث")
        
        # تنسيق الأزرار
        buttons = [self.add_btn, self.edit_btn, self.delete_btn, self.details_btn, self.refresh_btn]
        for btn in buttons:
            btn.setMinimumHeight(35)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #007bff;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    padding: 8px 16px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #0056b3;
                }
                QPushButton:disabled {
                    background-color: #6c757d;
                }
            """)
        
        # تلوين أزرار خاصة
        self.edit_btn.setStyleSheet(self.edit_btn.styleSheet().replace("#007bff", "#28a745").replace("#0056b3", "#1e7e34"))
        self.delete_btn.setStyleSheet(self.delete_btn.styleSheet().replace("#007bff", "#dc3545").replace("#0056b3", "#a71d2a"))
        
        # تعطيل الأزرار في البداية
        self.edit_btn.setEnabled(False)
        self.delete_btn.setEnabled(False)
        self.details_btn.setEnabled(False)
        
        # ترتيب العناصر
        toolbar_layout.addWidget(search_label)
        toolbar_layout.addWidget(self.search_input)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.add_btn)
        toolbar_layout.addWidget(self.edit_btn)
        toolbar_layout.addWidget(self.delete_btn)
        toolbar_layout.addWidget(self.details_btn)
        toolbar_layout.addWidget(self.refresh_btn)
        
        layout.addWidget(toolbar_frame)
    
    def add_content_area(self, layout: QVBoxLayout):
        """
        إضافة منطقة المحتوى
        
        Args:
            layout: التخطيط
        """
        # تقسيم المحتوى
        splitter = QSplitter(Qt.Horizontal)
        
        # إضافة الجدول
        self.add_table(splitter)
        
        # إضافة لوحة المعلومات
        self.add_info_panel(splitter)
        
        # تعيين نسب التقسيم
        splitter.setSizes([700, 300])
        
        layout.addWidget(splitter)
    
    def add_table(self, parent):
        """
        إضافة جدول الزبائن
        
        Args:
            parent: الحاوي الأب
        """
        # إطار الجدول
        table_frame = QFrame()
        table_layout = QVBoxLayout(table_frame)
        
        # عنوان الجدول
        table_title = QLabel("قائمة الزبائن")
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
        headers = ["المعرف", "الاسم", "رقم الهاتف", "العنوان", "تاريخ الإضافة"]
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
                background-color: #007bff;
                color: white;
            }
        """)
        
        table_layout.addWidget(self.table)
        parent.addWidget(table_frame)
    
    def add_info_panel(self, parent):
        """
        إضافة لوحة المعلومات
        
        Args:
            parent: الحاوي الأب
        """
        # إطار المعلومات
        info_frame = QFrame()
        info_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 8px;
            }
        """)
        info_layout = QVBoxLayout(info_frame)
        
        # عنوان اللوحة
        info_title = QLabel("معلومات الزبون")
        info_title.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #495057;
                margin-bottom: 15px;
                padding: 10px;
                background-color: #e9ecef;
                border-radius: 5px;
            }
        """)
        info_layout.addWidget(info_title)
        
        # منطقة عرض المعلومات
        self.info_display = QTextEdit()
        self.info_display.setReadOnly(True)
        self.info_display.setMaximumHeight(200)
        self.info_display.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 1px solid #ced4da;
                border-radius: 5px;
                padding: 10px;
                font-size: 12px;
            }
        """)
        info_layout.addWidget(self.info_display)
        
        # إحصائيات سريعة
        stats_label = QLabel("الإحصائيات:")
        stats_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #495057;
                margin-top: 15px;
                margin-bottom: 10px;
            }
        """)
        info_layout.addWidget(stats_label)
        
        self.stats_display = QTextEdit()
        self.stats_display.setReadOnly(True)
        self.stats_display.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 1px solid #ced4da;
                border-radius: 5px;
                padding: 10px;
                font-size: 11px;
            }
        """)
        info_layout.addWidget(self.stats_display)
        
        info_layout.addStretch()
        parent.addWidget(info_frame)
    
    def setup_connections(self):
        """
        إعداد الاتصالات والأحداث
        """
        # أحداث الأزرار
        self.add_btn.clicked.connect(self.add_person)
        self.edit_btn.clicked.connect(self.edit_person)
        self.delete_btn.clicked.connect(self.delete_person)
        self.details_btn.clicked.connect(self.show_person_details)
        self.refresh_btn.clicked.connect(self.load_persons)
        
        # أحداث الجدول
        self.table.selectionModel().selectionChanged.connect(self.on_selection_changed)
        self.table.doubleClicked.connect(self.show_person_details)
        
        # حدث البحث
        self.search_input.textChanged.connect(self.search_persons)
    
    def load_persons(self):
        """
        تحميل قائمة الزبائن
        """
        try:
            persons = self.controller.get_all_persons()
            self.populate_table(persons)
            self.clear_info_panel()
        except Exception as e:
            MessageHelper.show_error(self, "خطأ", f"حدث خطأ أثناء تحميل البيانات: {str(e)}")
    
    def populate_table(self, persons: list):
        """
        ملء الجدول بالبيانات
        
        Args:
            persons: قائمة الزبائن
        """
        self.table.setRowCount(len(persons))
        
        for row, person in enumerate(persons):
            # إخفاء المعرف في عمود مخفي
            id_item = QTableWidgetItem(str(person.id))
            id_item.setData(Qt.UserRole, person)  # حفظ كائن الزبون
            self.table.setItem(row, 0, id_item)
            
            # باقي البيانات
            self.table.setItem(row, 1, QTableWidgetItem(person.name))
            self.table.setItem(row, 2, QTableWidgetItem(person.phone or ""))
            self.table.setItem(row, 3, QTableWidgetItem(person.address or ""))
            
            from utils.helpers import DateHelper
            created_date = DateHelper.format_datetime(person.created_at)
            self.table.setItem(row, 4, QTableWidgetItem(created_date))
        
        # إخفاء عمود المعرف
        self.table.setColumnHidden(0, True)
        
        # ضبط عرض الأعمدة
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # الاسم
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # الهاتف
        header.setSectionResizeMode(3, QHeaderView.Stretch)  # العنوان
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # التاريخ
    
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
            # الحصول على الزبون المحدد
            id_item = self.table.item(current_row, 0)
            if id_item:
                self.selected_person = id_item.data(Qt.UserRole)
                self.update_info_panel()
        else:
            self.selected_person = None
            self.clear_info_panel()
    
    def update_info_panel(self):
        """
        تحديث لوحة المعلومات
        """
        if not self.selected_person:
            return
        
        # عرض معلومات الزبون
        info_text = f"""
        <b>الاسم:</b> {self.selected_person.name}<br>
        <b>رقم الهاتف:</b> {self.selected_person.phone or 'غير محدد'}<br>
        <b>العنوان:</b> {self.selected_person.address or 'غير محدد'}<br>
        <b>تاريخ الإضافة:</b> {self.selected_person.created_at.strftime('%Y-%m-%d %H:%M') if self.selected_person.created_at else 'غير محدد'}
        """
        self.info_display.setHtml(info_text)
        
        # عرض الإحصائيات
        try:
            stats = self.controller.get_person_statistics(self.selected_person.id)
            stats_text = f"""
            <b>عدد الديون:</b> {stats['debts_count']}<br>
            <b>إجمالي الديون:</b> {stats['total_debts']:.2f}<br>
            <b>الديون المدفوعة:</b> {stats['paid_debts']:.2f}<br>
            <b>عدد الأقساط:</b> {stats['installments_count']}<br>
            <b>إجمالي الأقساط:</b> {stats['total_installments_amount']:.2f}<br>
            <b>المدفوع من الأقساط:</b> {stats['paid_installments_amount']:.2f}<br>
            <b>عدد الاشتراكات:</b> {stats['subscriptions_count']}<br>
            <b>الاشتراكات النشطة:</b> {stats['active_subscriptions_count']}<br>
            <b>رسوم الإنترنت الشهرية:</b> {stats['monthly_internet_fees']:.2f}
            """
            self.stats_display.setHtml(stats_text)
        except Exception as e:
            self.stats_display.setHtml(f"<i>خطأ في تحميل الإحصائيات: {str(e)}</i>")
    
    def clear_info_panel(self):
        """
        مسح لوحة المعلومات
        """
        self.info_display.setHtml("<i>اختر زبوناً لعرض معلوماته</i>")
        self.stats_display.setHtml("<i>لا توجد إحصائيات للعرض</i>")
    
    def search_persons(self):
        """
        البحث في الزبائن
        """
        search_term = self.search_input.text().strip()
        
        try:
            if search_term:
                persons = self.controller.search_persons(search_term)
            else:
                persons = self.controller.get_all_persons()
            
            self.populate_table(persons)
            self.clear_info_panel()
        except Exception as e:
            MessageHelper.show_error(self, "خطأ", f"حدث خطأ أثناء البحث: {str(e)}")
    
    def add_person(self):
        """
        إضافة زبون جديد
        """
        dialog = AddPersonDialog(self)
        if dialog.exec_() == dialog.Accepted:
            person_data = dialog.get_person_data()
            
            success, message, person_id = self.controller.add_person(
                person_data['name'],
                person_data['phone'], 
                person_data['address'],
                person_data['notes']
            )
            
            if success:
                MessageHelper.show_info(self, "نجح", message)
                self.load_persons()
            else:
                MessageHelper.show_error(self, "خطأ", message)
    
    def edit_person(self):
        """
        تعديل زبون
        """
        if not self.selected_person:
            return
        
        dialog = AddPersonDialog(self, self.selected_person)
        if dialog.exec_() == dialog.Accepted:
            person_data = dialog.get_person_data()
            
            success, message = self.controller.update_person(
                self.selected_person.id,
                person_data['name'],
                person_data['phone'],
                person_data['address'],
                person_data['notes']
            )
            
            if success:
                MessageHelper.show_info(self, "نجح", message)
                self.load_persons()
            else:
                MessageHelper.show_error(self, "خطأ", message)
    
    def delete_person(self):
        """
        حذف زبون
        """
        if not self.selected_person:
            return
        
        reply = MessageHelper.show_question(
            self, "تأكيد الحذف",
            f"هل أنت متأكد من حذف الزبون '{self.selected_person.name}'؟\n"
            "سيتم حذف جميع البيانات المرتبطة به (الديون، الأقساط، الاشتراكات)."
        )
        
        if reply:
            success, message = self.controller.delete_person(self.selected_person.id)
            
            if success:
                MessageHelper.show_info(self, "نجح", message)
                self.load_persons()
            else:
                MessageHelper.show_error(self, "خطأ", message)
    
    def show_person_details(self):
        """
        عرض تفاصيل الزبون
        """
        if not self.selected_person:
            return
        
        try:
            from views.person_details_view import PersonDetailsView
            # تخزين النافذة كعضو في الكلاس لمنعها من الحذف
            self.details_window = PersonDetailsView(self.selected_person)
            self.details_window.person_updated.connect(self.load_persons)  # تحديث البيانات عند التعديل
            self.details_window.show()
        except Exception as e:
            MessageHelper.show_error(self, "خطأ", f"حدث خطأ في فتح نافذة التفاصيل: {str(e)}")
