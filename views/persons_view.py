# -*- coding: utf-8 -*-
"""
واجهة إدارة الزبائن
تحتوي على عرض وإضافة وتعديل وحذف الزبائن
(نسخة مُعادة التصميم)
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QTableWidget, QTableWidgetItem, QLineEdit,
                             QLabel, QHeaderView, QFrame, QSplitter, QFormLayout, QGroupBox)
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QFont, QIcon # QIcon is optional for future use
from controllers.person_controller import PersonController
from database.models import Person
from utils.helpers import MessageHelper, AppHelper, TableHelper, NumberHelper, DateHelper


class PersonsView(QMainWindow):
    """
    واجهة إدارة الزبائن بتصميم مُحسّن
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
        تهيئة واجهة المستخدم الرئيسية
        """
        self.setWindowTitle("إدارة الزبائن")
        self.setMinimumSize(1200, 700)
        AppHelper.center_window(self)
        
        # القطعة المركزية والتخطيط الرئيسي
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # تطبيق الأنماط على الواجهة بأكملها
        self._apply_styles()
        
        # إنشاء شريط الأدوات (بحث وأزرار)
        toolbar = self._create_toolbar()
        main_layout.addLayout(toolbar)
        
        # إنشاء منطقة المحتوى (الجدول ولوحة التفاصيل)
        content_splitter = self._create_content_area()
        main_layout.addWidget(content_splitter)

    def _create_toolbar(self) -> QHBoxLayout:
        """
        إنشاء شريط الأدوات العلوي الذي يحتوي على البحث والأزرار
        """
        toolbar_layout = QHBoxLayout()
        toolbar_layout.setSpacing(10)
        
        # مكونات البحث
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("ابحث بالاسم، رقم الهاتف، أو العنوان...")
        self.search_input.setObjectName("searchInput")

        # أزرار الإجراءات
        self.add_btn = QPushButton("إضافة زبون")
        self.edit_btn = QPushButton("تعديل")
        self.delete_btn = QPushButton("حذف")
        self.details_btn = QPushButton("عرض التفاصيل")
        self.refresh_btn = QPushButton("تحديث")
        
        # تعيين أسماء كائنات للأزرار لتطبيق الأنماط
        self.add_btn.setObjectName("addButton")
        self.edit_btn.setObjectName("editButton")
        self.delete_btn.setObjectName("deleteButton")
        self.refresh_btn.setObjectName("refreshButton")
        
        # تعطيل الأزرار التي تتطلب تحديدًا
        self.edit_btn.setEnabled(False)
        self.delete_btn.setEnabled(False)
        self.details_btn.setEnabled(False)
        
        # إضافة المكونات إلى التخطيط
        toolbar_layout.addWidget(QLabel("🔍 بحث:"))
        toolbar_layout.addWidget(self.search_input)
        toolbar_layout.addStretch(1)
        toolbar_layout.addWidget(self.add_btn)
        toolbar_layout.addWidget(self.edit_btn)
        toolbar_layout.addWidget(self.delete_btn)
        toolbar_layout.addWidget(self.details_btn)
        toolbar_layout.addWidget(self.refresh_btn)
        
        return toolbar_layout

    def _create_content_area(self) -> QSplitter:
        """
        إنشاء منطقة المحتوى المقسمة
        """
        splitter = QSplitter(Qt.Horizontal)
        
        # إنشاء لوحة الجدول
        table_panel = self._create_table_panel()
        
        # إنشاء لوحة المعلومات
        info_panel = self._create_info_panel()
        
        splitter.addWidget(table_panel)
        splitter.addWidget(info_panel)
        
        # تعيين نسب التقسيم (70% للجدول، 30% للمعلومات)
        splitter.setSizes([700, 300])
        splitter.setStretchFactor(0, 1) # السماح للجدول بالتمدد
        splitter.setStretchFactor(1, 0)
        
        return splitter

    def _create_table_panel(self) -> QGroupBox:
        """
        إنشاء لوحة عرض قائمة الزبائن
        """
        group_box = QGroupBox("قائمة الزبائن")
        layout = QVBoxLayout(group_box)
        
        self.table = QTableWidget()
        headers = ["المعرف", "الاسم الكامل", "رقم الهاتف", "العنوان", "تاريخ الإضافة"]
        TableHelper.setup_table_headers(self.table, headers)
        
        # تنسيق الجدول
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setAlternatingRowColors(True)
        
        # ضبط عرض الأعمدة
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        
        # إخفاء عمود المعرف
        self.table.setColumnHidden(0, True)

        layout.addWidget(self.table)
        return group_box

    def _create_info_panel(self) -> QWidget:
        """
        إنشاء لوحة عرض معلومات وإحصائيات الزبون المحدد
        """
        # الحاوي الرئيسي للوحة المعلومات
        container = QWidget()
        main_layout = QVBoxLayout(container)
        main_layout.setSpacing(15)

        # 1. صندوق معلومات الزبون
        info_group = QGroupBox("معلومات الزبون")
        info_layout = QFormLayout(info_group)
        info_layout.setLabelAlignment(Qt.AlignRight)
        
        self.info_name_val = QLabel("<i>لم يتم تحديد أي زبون</i>")
        self.info_phone_val = QLabel("-")
        self.info_address_val = QLabel("-")
        self.info_date_val = QLabel("-")
        
        info_layout.addRow("<b>الاسم:</b>", self.info_name_val)
        info_layout.addRow("<b>الهاتف:</b>", self.info_phone_val)
        info_layout.addRow("<b>العنوان:</b>", self.info_address_val)
        info_layout.addRow("<b>تاريخ الإضافة:</b>", self.info_date_val)
        
        # 2. صندوق إحصائيات الزبون
        stats_group = QGroupBox("الإحصائيات")
        stats_layout = QFormLayout(stats_group)
        stats_layout.setLabelAlignment(Qt.AlignRight)
        
        self.stats_debts_total = QLabel("-")
        self.stats_installments_total = QLabel("-")
        self.stats_subscriptions_active = QLabel("-")
        self.stats_internet_fees = QLabel("-")
        
        stats_layout.addRow("<b>إجمالي الديون المتبقية:</b>", self.stats_debts_total)
        stats_layout.addRow("<b>إجمالي الأقساط المتبقية:</b>", self.stats_installments_total)
        stats_layout.addRow("<b>الاشتراكات النشطة:</b>", self.stats_subscriptions_active)
        stats_layout.addRow("<b>رسوم الإنترنت الشهرية:</b>", self.stats_internet_fees)
        
        main_layout.addWidget(info_group)
        main_layout.addWidget(stats_group)
        main_layout.addStretch()

        return container
    
    def _apply_styles(self):
        """
        تطبيق ورقة أنماط مركزية (QSS) على الواجهة
        """
        style_sheet = """
            QMainWindow, QWidget {
                background-color: #f0f2f5;
                font-family: 'Segoe UI', 'Tahoma';
                font-size: 14px;
            }
            QGroupBox {
                font-weight: bold;
                background-color: #ffffff;
                border: 1px solid #dcdcdc;
                border-radius: 8px;
                margin-top: 10px;
                padding: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 10px;
                background-color: #f0f2f5;
            }
            QLabel {
                color: #333;
                padding: 2px;
            }
            QLineEdit#searchInput {
                background-color: #ffffff;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
            }
            QLineEdit#searchInput:focus {
                border-color: #0078d7;
            }
            QPushButton {
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-weight: bold;
                min-height: 30px;
            }
            QPushButton:hover {
                opacity: 0.9;
            }
            QPushButton:disabled {
                background-color: #b0b0b0;
            }
            QPushButton#addButton { background-color: #0078d7; }
            QPushButton#addButton:hover { background-color: #005a9e; }
            QPushButton#editButton { background-color: #107c10; }
            QPushButton#editButton:hover { background-color: #0f6a0f; }
            QPushButton#deleteButton { background-color: #d83b01; }
            QPushButton#deleteButton:hover { background-color: #b32f00; }
            QPushButton#refreshButton { background-color: #5c5c5c; }
            QPushButton#refreshButton:hover { background-color: #454545; }
            QTableWidget {
                background-color: white;
                border: 1px solid #dcdcdc;
                gridline-color: #e0e0e0;
                alternate-background-color: #f9f9f9;
                font-size: 14px;
            }
            QTableWidget::item {
                padding: 10px;
                border-bottom: 1px solid #e0e0e0;
            }
            QTableWidget::item:selected {
                background-color: #0078d7;
                color: white;
            }
            QHeaderView::section {
                background-color: #f8f8f8;
                padding: 8px;
                border: 1px solid #dcdcdc;
                font-weight: bold;
                font-size: 14px;
            }
            QSplitter::handle {
                background-color: #dcdcdc;
                width: 2px;
            }
        """
        self.setStyleSheet(style_sheet)

    def setup_connections(self):
        """
        إعداد الاتصالات والأحداث
        """
        self.add_btn.clicked.connect(self.add_person)
        self.edit_btn.clicked.connect(self.edit_person)
        self.delete_btn.clicked.connect(self.delete_person)
        self.details_btn.clicked.connect(self.show_person_details)
        self.refresh_btn.clicked.connect(self.load_persons)
        
        self.table.selectionModel().selectionChanged.connect(self.on_selection_changed)
        self.table.doubleClicked.connect(self.show_person_details)
        
        self.search_input.textChanged.connect(self.search_persons)

    def on_selection_changed(self):
        """
        معالجة تغيير التحديد في الجدول
        """
        selected_rows = self.table.selectionModel().selectedRows()
        has_selection = bool(selected_rows)
        
        self.edit_btn.setEnabled(has_selection)
        self.delete_btn.setEnabled(has_selection)
        self.details_btn.setEnabled(has_selection)
        
        if has_selection:
            current_row = selected_rows[0].row()
            id_item = self.table.item(current_row, 0)
            if id_item:
                self.selected_person = id_item.data(Qt.UserRole)
                self.update_info_panel()
        else:
            self.selected_person = None
            self.clear_info_panel()

    def update_info_panel(self):
        """
        تحديث لوحة المعلومات بالبيانات الجديدة
        """
        if not self.selected_person:
            return
            
        # تحديث معلومات الزبون
        self.info_name_val.setText(self.selected_person.name)
        self.info_phone_val.setText(self.selected_person.phone or "غير محدد")
        self.info_address_val.setText(self.selected_person.address or "غير محدد")
        formatted_date = DateHelper.format_datetime(self.selected_person.created_at)
        self.info_date_val.setText(formatted_date)
        
        # تحديث الإحصائيات
        try:
            stats = self.controller.get_person_statistics(self.selected_person.id)
            remaining_debts = stats['total_debts'] - stats['paid_debts']
            remaining_installments = stats['total_installments_amount'] - stats['paid_installments_amount']
            
            self.stats_debts_total.setText(NumberHelper.format_currency(remaining_debts))
            self.stats_installments_total.setText(NumberHelper.format_currency(remaining_installments))
            self.stats_subscriptions_active.setText(f"{stats['active_subscriptions_count']} اشتراك")
            self.stats_internet_fees.setText(NumberHelper.format_currency(stats['monthly_internet_fees']))
        except Exception as e:
            self.clear_info_panel(is_error=True)
            print(f"Error loading stats: {e}")

    def clear_info_panel(self, is_error=False):
        """
        مسح لوحة المعلومات
        """
        self.info_name_val.setText("<i>لم يتم تحديد أي زبون</i>")
        self.info_phone_val.setText("-")
        self.info_address_val.setText("-")
        self.info_date_val.setText("-")
        
        if is_error:
            error_msg = "<i>خطأ في تحميل الإحصائيات</i>"
            self.stats_debts_total.setText(error_msg)
            self.stats_installments_total.setText(error_msg)
            self.stats_subscriptions_active.setText(error_msg)
            self.stats_internet_fees.setText(error_msg)
        else:
            self.stats_debts_total.setText("-")
            self.stats_installments_total.setText("-")
            self.stats_subscriptions_active.setText("-")
            self.stats_internet_fees.setText("-")

    # --- باقي الدوال تبقى كما هي بدون تغيير ---
    
    def load_persons(self):
        try:
            self.table.setSortingEnabled(False) # إيقاف الفرز أثناء التحميل
            persons = self.controller.get_all_persons()
            self.populate_table(persons)
            self.clear_info_panel()
        except Exception as e:
            MessageHelper.show_error(self, "خطأ", f"حدث خطأ أثناء تحميل البيانات: {str(e)}")
        finally:
            self.table.setSortingEnabled(True) # إعادة تفعيل الفرز
    
    def populate_table(self, persons: list):
        self.table.setRowCount(len(persons))
        for row, person in enumerate(persons):
            id_item = QTableWidgetItem(str(person.id))
            id_item.setData(Qt.UserRole, person)
            self.table.setItem(row, 0, id_item)
            
            self.table.setItem(row, 1, QTableWidgetItem(person.name))
            self.table.setItem(row, 2, QTableWidgetItem(person.phone or ""))
            self.table.setItem(row, 3, QTableWidgetItem(person.address or ""))
            
            created_date = DateHelper.format_datetime(person.created_at)
            self.table.setItem(row, 4, QTableWidgetItem(created_date))

    def search_persons(self):
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
        from views.dialogs.add_person_dialog import AddPersonDialog
        dialog = AddPersonDialog(self)
        if dialog.exec_() == dialog.Accepted:
            person_data = dialog.get_person_data()
            success, message, _ = self.controller.add_person(
                person_data['name'],
                person_data['phone'], 
                person_data['address'],
                person_data['notes']
            )
            if success:
                MessageHelper.show_info(self, "نجاح", message)
                self.load_persons()
                self.person_updated.emit()
            else:
                MessageHelper.show_error(self, "خطأ", message)
    
    def edit_person(self):
        if not self.selected_person:
            return
        
        from views.dialogs.add_person_dialog import AddPersonDialog
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
                MessageHelper.show_info(self, "نجاح", message)
                self.load_persons()
                self.person_updated.emit()
            else:
                MessageHelper.show_error(self, "خطأ", message)
    
    def delete_person(self):
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
                MessageHelper.show_info(self, "نجاح", message)
                self.load_persons()
                self.person_updated.emit()
            else:
                MessageHelper.show_error(self, "خطأ", message)
    
    def show_person_details(self):
        if not self.selected_person:
            return
        
        try:
            from views.person_details_view import PersonDetailsView
            self.details_window = PersonDetailsView(self.selected_person)
            self.details_window.person_updated.connect(self.load_persons)
            self.details_window.showMaximized()
        except Exception as e:
            MessageHelper.show_error(self, "خطأ", f"حدث خطأ في فتح نافذة التفاصيل: {str(e)}")