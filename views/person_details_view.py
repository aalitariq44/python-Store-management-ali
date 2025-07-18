# -*- coding: utf-8 -*-
"""
نافذة تفاصيل الزبون
تعرض جميع البيانات المرتبطة بالزبون في تبويبات منفصلة
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QTableWidget, QTableWidgetItem, QLineEdit,
                             QLabel, QHeaderView, QFrame, QTabWidget, QTextEdit, QComboBox, QInputDialog, QCheckBox)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QColor
from database.models import Person
from controllers.person_controller import PersonController
from controllers.debt_controller import DebtController
from controllers.installment_controller import InstallmentController
from controllers.internet_controller import InternetController
from utils.helpers import MessageHelper, AppHelper, TableHelper, DateHelper, NumberHelper
from views.dialogs.add_debt_dialog import AddDebtDialog
from views.dialogs.add_installment_dialog import AddInstallmentDialog
from views.dialogs.add_internet_dialog import AddInternetDialog
from views.dialogs.installment_details_dialog import InstallmentDetailsDialog


class PersonDetailsView(QMainWindow):
    """
    نافذة تفاصيل الزبون مع جميع البيانات المرتبطة
    """
    
    # إشارة لتحديث البيانات
    person_updated = pyqtSignal()
    
    def __init__(self, person: Person):
        super().__init__()
        self.person = person
        self.person_controller = PersonController()
        self.debt_controller = DebtController()
        self.installment_controller = InstallmentController()
        self.internet_controller = InternetController()
        
        self.init_ui()
        self.setup_connections()
        self.load_all_data()
    
    def init_ui(self):
        """
        تهيئة واجهة المستخدم
        """
        self.setWindowTitle(f"تفاصيل الزبون - {self.person.name}")
        self.setMinimumSize(1200, 700)
        AppHelper.center_window(self, 1300, 800)
        
        # القطعة المركزية
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # التخطيط الرئيسي
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # إضافة معلومات الزبون
        self.add_person_info(main_layout)
        
        # إضافة التبويبات
        self.add_tabs(main_layout)
    
    def add_person_info(self, layout: QVBoxLayout):
        """
        إضافة معلومات الزبون الأساسية
        
        Args:
            layout: التخطيط
        """
        info_frame = QFrame()
        info_frame.setStyleSheet("""
            QFrame {
                background-color: #007bff;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        
        info_layout = QHBoxLayout(info_frame)
        
        # معلومات الزبون
        person_info = QVBoxLayout()
        
        name_label = QLabel(f"الاسم: {self.person.name}")
        name_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                background: transparent;
            }
        """)
        person_info.addWidget(name_label)
        
        phone_label = QLabel(f"الهاتف: {self.person.phone or 'غير محدد'}")
        phone_label.setStyleSheet("""
            QLabel {
                color: #e3f2fd;
                font-size: 24px;
                background: transparent;
            }
        """)
        person_info.addWidget(phone_label)
        
        address_label = QLabel(f"العنوان: {self.person.address or 'غير محدد'}")
        address_label.setStyleSheet("""
            QLabel {
                color: #e3f2fd;
                font-size: 24px;
                background: transparent;
            }
        """)
        person_info.addWidget(address_label)
        
        # تاريخ الإضافة
        if self.person.created_at:
            created_label = QLabel(f"تاريخ الإضافة: {DateHelper.format_datetime(self.person.created_at)}")
            created_label.setStyleSheet("""
                QLabel {
                    color: #e3f2fd;
                    font-size: 24px;
                    background: transparent;
                }
            """)
            person_info.addWidget(created_label)
        
        info_layout.addLayout(person_info)
        info_layout.addStretch()
        
        # الإحصائيات السريعة
        self.stats_layout = QVBoxLayout()
        info_layout.addLayout(self.stats_layout)
        
        layout.addWidget(info_frame)
    
    def update_stats(self):
        """
        تحديث الإحصائيات السريعة
        """
        # مسح الإحصائيات السابقة
        for i in reversed(range(self.stats_layout.count())):
            self.stats_layout.itemAt(i).widget().setParent(None)
        
        try:
            stats = self.person_controller.get_person_statistics(self.person.id)
            
            stats_labels = [
                f"الديون: {stats['debts_count']} ({NumberHelper.format_currency(stats['total_debts'])})",
                f"الأقساط: {stats['installments_count']} ({NumberHelper.format_currency(stats['total_installments_amount'])})",
                f"الاشتراكات: {stats['active_subscriptions_count']}/{stats['subscriptions_count']}",
                f"رسوم شهرية: {NumberHelper.format_currency(stats['monthly_internet_fees'])}"
            ]
            
            for stat_text in stats_labels:
                stat_label = QLabel(stat_text)
                stat_label.setStyleSheet("""
                    QLabel {
                        color: white;
                        font-size: 24px;
                        font-weight: bold;
                        background: transparent;
                        padding: 2px;
                    }
                """)
                self.stats_layout.addWidget(stat_label)
                
        except Exception as e:
            error_label = QLabel("خطأ في تحميل الإحصائيات")
            error_label.setStyleSheet("""
                QLabel {
                    color: #ffcdd2;
                    font-size: 24px;
                    background: transparent;
                }
            """)
            self.stats_layout.addWidget(error_label)
    
    def add_tabs(self, layout: QVBoxLayout):
        """
        إضافة التبويبات
        
        Args:
            layout: التخطيط
        """
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #dee2e6;
                background-color: white;
                border-radius: 5px;
            }
            QTabBar::tab {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                padding: 10px 20px;
                margin-right: 2px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom-color: white;
                color: #007bff;
            }
            QTabBar::tab:hover {
                background-color: #e9ecef;
            }
        """)
        
        # تبويب الديون
        self.debts_tab = self.create_debts_tab()
        self.tab_widget.addTab(self.debts_tab, "الديون")
        
        # تبويب الأقساط
        self.installments_tab = self.create_installments_tab()
        self.tab_widget.addTab(self.installments_tab, "الأقساط")
        
        # تبويب اشتراكات الإنترنت
        self.internet_tab = self.create_internet_tab()
        self.tab_widget.addTab(self.internet_tab, "اشتراكات الإنترنت")
        
        # تبويب الملاحظات
        self.notes_tab = self.create_notes_tab()
        self.tab_widget.addTab(self.notes_tab, "الملاحظات")
        
        layout.addWidget(self.tab_widget)
    
    def create_debts_tab(self) -> QWidget:
        """
        إنشاء تبويب الديون
        
        Returns:
            QWidget: تبويب الديون
        """
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(10)

        # شريط الأدوات والفلترة
        toolbar_frame = QFrame()
        toolbar_layout = QHBoxLayout(toolbar_frame)

        # البحث
        toolbar_layout.addWidget(QLabel("البحث:"))
        self.debt_search_input = QLineEdit()
        self.debt_search_input.setPlaceholderText("ابحث في الوصف أو المبلغ...")
        self.debt_search_input.setMaximumWidth(250)
        toolbar_layout.addWidget(self.debt_search_input)

        # فلتر الحالة
        toolbar_layout.addWidget(QLabel("الحالة:"))
        self.debt_status_filter = QComboBox()
        self.debt_status_filter.addItems(["الكل", "غير مدفوع", "مدفوع", "متأخر"])
        self.debt_status_filter.setMaximumWidth(120)
        toolbar_layout.addWidget(self.debt_status_filter)
        
        toolbar_layout.addStretch()

        # الأزرار
        self.add_debt_btn = QPushButton("إضافة دين")
        self.edit_debt_btn = QPushButton("تعديل")
        self.delete_debt_btn = QPushButton("حذف")
        self.mark_paid_btn = QPushButton("وضع علامة مدفوع")
        self.debt_refresh_btn = QPushButton("تحديث")

        buttons = [self.add_debt_btn, self.edit_debt_btn, self.delete_debt_btn, self.mark_paid_btn, self.debt_refresh_btn]
        for btn in buttons:
            btn.setMinimumHeight(35)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #007bff; color: white; border: none;
                    border-radius: 5px; padding: 8px 16px; font-weight: bold;
                }
                QPushButton:hover { background-color: #0056b3; }
                QPushButton:disabled { background-color: #6c757d; }
            """)
        
        self.delete_debt_btn.setStyleSheet(self.delete_debt_btn.styleSheet().replace("#007bff", "#dc3545").replace("#0056b3", "#c82333"))
        self.mark_paid_btn.setStyleSheet(self.mark_paid_btn.styleSheet().replace("#007bff", "#28a745").replace("#0056b3", "#218838"))
        self.debt_refresh_btn.setStyleSheet(self.debt_refresh_btn.styleSheet().replace("#007bff", "#6c757d").replace("#0056b3", "#5a6268"))

        self.edit_debt_btn.setEnabled(False)
        self.delete_debt_btn.setEnabled(False)
        self.mark_paid_btn.setEnabled(False)

        toolbar_layout.addWidget(self.add_debt_btn)
        toolbar_layout.addWidget(self.edit_debt_btn)
        toolbar_layout.addWidget(self.delete_debt_btn)
        toolbar_layout.addWidget(self.mark_paid_btn)
        toolbar_layout.addWidget(self.debt_refresh_btn)
        
        layout.addWidget(toolbar_frame)
        
        # جدول الديون
        self.debts_table = QTableWidget()
        headers = ["المعرف", "المبلغ", "الوصف", "تاريخ الاستحقاق", "الحالة", "تاريخ الإضافة"]
        TableHelper.setup_table_headers(self.debts_table, headers)
        
        self.debts_table.setAlternatingRowColors(True)
        self.debts_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.debts_table.setColumnHidden(0, True)
        
        layout.addWidget(self.debts_table)

        # شريط الحالة
        status_frame = QFrame()
        status_frame.setStyleSheet("background-color: #f8f9fa; border: 1px solid #dee2e6; border-radius: 8px; padding: 10px;")
        status_layout = QHBoxLayout(status_frame)
        
        self.person_total_debts_label = QLabel("إجمالي الديون: -")
        self.person_unpaid_debts_label = QLabel("غير مدفوع: -")
        self.person_paid_debts_label = QLabel("مدفوع: -")
        self.person_overdue_debts_label = QLabel("متأخر: -")
        
        for label in [self.person_total_debts_label, self.person_unpaid_debts_label, self.person_paid_debts_label, self.person_overdue_debts_label]:
            label.setStyleSheet("font-weight: bold; color: #495057;")
            status_layout.addWidget(label)
        
        status_layout.addStretch()
        layout.addWidget(status_frame)
        
        return tab
    
    def create_installments_tab(self) -> QWidget:
        """
        إنشاء تبويب الأقساط
        
        Returns:
            QWidget: تبويب الأقساط
        """
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(10)

        # شريط الأدوات والفلترة
        toolbar_frame = QFrame()
        toolbar_layout = QHBoxLayout(toolbar_frame)

        toolbar_layout.addWidget(QLabel("البحث:"))
        self.inst_search_input = QLineEdit()
        self.inst_search_input.setPlaceholderText("ابحث في الوصف أو المبلغ...")
        self.inst_search_input.setMaximumWidth(250)
        toolbar_layout.addWidget(self.inst_search_input)

        toolbar_layout.addWidget(QLabel("الحالة:"))
        self.inst_status_filter = QComboBox()
        self.inst_status_filter.addItems(["الكل", "نشط", "مكتمل"])
        self.inst_status_filter.setMaximumWidth(120)
        toolbar_layout.addWidget(self.inst_status_filter)
        
        toolbar_layout.addStretch()

        # الأزرار
        self.add_installment_btn = QPushButton("إضافة قسط")
        self.edit_installment_btn = QPushButton("تعديل")
        self.delete_installment_btn = QPushButton("حذف")
        self.add_payment_btn = QPushButton("إضافة دفعة")
        self.installment_details_btn = QPushButton("عرض التفاصيل")
        self.installment_refresh_btn = QPushButton("تحديث")

        buttons = [self.add_installment_btn, self.edit_installment_btn, self.delete_installment_btn, self.add_payment_btn, self.installment_details_btn, self.installment_refresh_btn]
        for btn in buttons:
            btn.setMinimumHeight(35)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #f39c12; color: white; border: none;
                    border-radius: 5px; padding: 8px 16px; font-weight: bold;
                }
                QPushButton:hover { background-color: #e67e22; }
                QPushButton:disabled { background-color: #6c757d; }
            """)
        
        self.delete_installment_btn.setStyleSheet(self.delete_installment_btn.styleSheet().replace("#f39c12", "#dc3545").replace("#e67e22", "#c82333"))
        self.add_payment_btn.setStyleSheet(self.add_payment_btn.styleSheet().replace("#f39c12", "#28a745").replace("#e67e22", "#218838"))
        self.installment_refresh_btn.setStyleSheet(self.installment_refresh_btn.styleSheet().replace("#f39c12", "#6c757d").replace("#e67e22", "#5a6268"))

        self.edit_installment_btn.setEnabled(False)
        self.delete_installment_btn.setEnabled(False)
        self.add_payment_btn.setEnabled(False)
        self.installment_details_btn.setEnabled(False)

        toolbar_layout.addWidget(self.add_installment_btn)
        toolbar_layout.addWidget(self.edit_installment_btn)
        toolbar_layout.addWidget(self.delete_installment_btn)
        toolbar_layout.addWidget(self.add_payment_btn)
        toolbar_layout.addWidget(self.installment_details_btn)
        toolbar_layout.addWidget(self.installment_refresh_btn)
        
        layout.addWidget(toolbar_frame)
        
        # جدول الأقساط
        self.installments_table = QTableWidget()
        headers = ["المعرف", "المبلغ الإجمالي", "المدفوع", "المتبقي", "الوصف", "نسبة الإنجاز", "الحالة", "تاريخ البداية"]
        TableHelper.setup_table_headers(self.installments_table, headers)
        
        self.installments_table.setAlternatingRowColors(True)
        self.installments_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.installments_table.setColumnHidden(0, True)
        
        layout.addWidget(self.installments_table)

        # شريط الحالة
        status_frame = QFrame()
        status_frame.setStyleSheet("background-color: #f8f9fa; border: 1px solid #dee2e6; border-radius: 8px; padding: 10px;")
        status_layout = QHBoxLayout(status_frame)
        
        self.person_total_installments_label = QLabel("إجمالي الأقساط: -")
        self.person_active_installments_label = QLabel("نشط: -")
        self.person_completed_installments_label = QLabel("مكتمل: -")
        self.person_total_amount_label = QLabel("إجمالي المبالغ: -")
        self.person_paid_amount_label = QLabel("المدفوع: -")
        
        for label in [self.person_total_installments_label, self.person_active_installments_label, self.person_completed_installments_label, self.person_total_amount_label, self.person_paid_amount_label]:
            label.setStyleSheet("font-weight: bold; color: #495057;")
            status_layout.addWidget(label)
        
        status_layout.addStretch()
        layout.addWidget(status_frame)
        
        return tab
    
    def create_notes_tab(self) -> QWidget:
        """
        إنشاء تبويب الملاحظات
        
        Returns:
            QWidget: تبويب الملاحظات
        """
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        self.notes_text_edit = QTextEdit()
        self.notes_text_edit.setReadOnly(True)
        self.notes_text_edit.setPlainText(self.person.notes or "لا توجد ملاحظات.")
        
        layout.addWidget(self.notes_text_edit)
        
        return tab
    
    def create_internet_tab(self) -> QWidget:
        """
        إنشاء تبويب اشتراكات الإنترنت
        
        Returns:
            QWidget: تبويب اشتراكات الإنترنت
        """
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(10)

        # شريط الأدوات
        toolbar_frame = QFrame()
        toolbar_layout = QHBoxLayout(toolbar_frame)

        toolbar_layout.addWidget(QLabel("البحث:"))
        self.net_search_input = QLineEdit()
        self.net_search_input.setPlaceholderText("ابحث باسم الباقة...")
        self.net_search_input.setMaximumWidth(250)
        toolbar_layout.addWidget(self.net_search_input)

        toolbar_layout.addWidget(QLabel("الحالة:"))
        self.net_status_filter = QComboBox()
        self.net_status_filter.addItems(["الكل", "نشط", "منتهي", "لم يبدأ بعد"])
        self.net_status_filter.setMaximumWidth(120)
        toolbar_layout.addWidget(self.net_status_filter)
        
        toolbar_layout.addStretch()

        self.add_internet_btn = QPushButton("إضافة اشتراك")
        self.edit_internet_btn = QPushButton("تعديل")
        self.delete_internet_btn = QPushButton("حذف")
        self.mark_internet_paid_btn = QPushButton("وضع علامة كمدفوع")
        self.internet_refresh_btn = QPushButton("تحديث")

        buttons = [self.add_internet_btn, self.edit_internet_btn, self.delete_internet_btn, self.mark_internet_paid_btn, self.internet_refresh_btn]
        for btn in buttons:
            btn.setMinimumHeight(35)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #6c5ce7; color: white; border: none;
                    border-radius: 5px; padding: 8px 16px; font-weight: bold;
                }
                QPushButton:hover { background-color: #5a4fcf; }
                QPushButton:disabled { background-color: #6c757d; }
            """)
        
        self.delete_internet_btn.setStyleSheet(self.delete_internet_btn.styleSheet().replace("#6c5ce7", "#dc3545").replace("#5a4fcf", "#c82333"))
        self.mark_internet_paid_btn.setStyleSheet(self.mark_internet_paid_btn.styleSheet().replace("#6c5ce7", "#17a2b8").replace("#5a4fcf", "#138496"))
        self.internet_refresh_btn.setStyleSheet(self.internet_refresh_btn.styleSheet().replace("#6c5ce7", "#6c757d").replace("#5a4fcf", "#5a6268"))

        self.edit_internet_btn.setEnabled(False)
        self.delete_internet_btn.setEnabled(False)
        self.mark_internet_paid_btn.setEnabled(False)

        toolbar_layout.addWidget(self.add_internet_btn)
        toolbar_layout.addWidget(self.edit_internet_btn)
        toolbar_layout.addWidget(self.delete_internet_btn)
        toolbar_layout.addWidget(self.mark_internet_paid_btn)
        toolbar_layout.addWidget(self.internet_refresh_btn)
        
        layout.addWidget(toolbar_frame)
        
        # جدول الاشتراكات
        self.internet_table = QTableWidget()
        headers = ["المعرف", "اسم الباقة", "التكلفة", "تاريخ البداية", "تاريخ النهاية", "الحالة", "الدفع", "الأيام المتبقية"]
        TableHelper.setup_table_headers(self.internet_table, headers)
        
        self.internet_table.setAlternatingRowColors(True)
        self.internet_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.internet_table.setColumnHidden(0, True)
        
        layout.addWidget(self.internet_table)

        # شريط الحالة
        status_frame = QFrame()
        status_frame.setStyleSheet("background-color: #f8f9fa; border: 1px solid #dee2e6; border-radius: 8px; padding: 10px;")
        status_layout = QHBoxLayout(status_frame)
        
        self.person_total_subs_label = QLabel("إجمالي الاشتراكات: -")
        self.person_active_subs_label = QLabel("نشط: -")
        self.person_expired_subs_label = QLabel("منتهي: -")
        
        for label in [self.person_total_subs_label, self.person_active_subs_label, self.person_expired_subs_label]:
            label.setStyleSheet("font-weight: bold; color: #495057;")
            status_layout.addWidget(label)
        
        status_layout.addStretch()
        layout.addWidget(status_frame)
        
        return tab
    
    def setup_connections(self):
        """
        إعداد الاتصالات والأحداث
        """
        # أحداث الديون
        self.add_debt_btn.clicked.connect(self.add_debt)
        self.edit_debt_btn.clicked.connect(self.edit_debt)
        self.delete_debt_btn.clicked.connect(self.delete_debt)
        self.mark_paid_btn.clicked.connect(self.mark_debt_paid)
        self.debts_table.selectionModel().selectionChanged.connect(self.on_debt_selection_changed)
        self.debts_table.doubleClicked.connect(self.edit_debt)
        self.debt_refresh_btn.clicked.connect(self.load_debts)
        self.debt_search_input.textChanged.connect(self.filter_debts)
        self.debt_status_filter.currentTextChanged.connect(self.filter_debts)
        
        # أحداث الأقساط
        self.add_installment_btn.clicked.connect(self.add_installment)
        self.edit_installment_btn.clicked.connect(self.edit_installment)
        self.delete_installment_btn.clicked.connect(self.delete_installment)
        self.add_payment_btn.clicked.connect(self.add_installment_payment)
        self.installments_table.selectionModel().selectionChanged.connect(self.on_installment_selection_changed)
        self.installments_table.doubleClicked.connect(self.show_installment_details)
        self.installment_details_btn.clicked.connect(self.show_installment_details)
        self.installment_refresh_btn.clicked.connect(self.load_installments)
        self.inst_search_input.textChanged.connect(self.filter_installments)
        self.inst_status_filter.currentTextChanged.connect(self.filter_installments)
        
        # أحداث اشتراكات الإنترنت
        self.add_internet_btn.clicked.connect(self.add_internet_subscription)
        self.edit_internet_btn.clicked.connect(self.edit_internet_subscription)
        self.delete_internet_btn.clicked.connect(self.delete_internet_subscription)
        self.mark_internet_paid_btn.clicked.connect(self.mark_subscription_paid)
        self.internet_refresh_btn.clicked.connect(self.load_internet_subscriptions)
        self.internet_table.selectionModel().selectionChanged.connect(self.on_internet_selection_changed)
        self.internet_table.doubleClicked.connect(self.edit_internet_subscription)
        self.net_search_input.textChanged.connect(self.filter_internet_subscriptions)
        self.net_status_filter.currentTextChanged.connect(self.filter_internet_subscriptions)
    
    def load_all_data(self):
        """
        تحميل جميع البيانات
        """
        self.load_debts()
        self.load_installments()
        self.load_internet_subscriptions()
        self.update_stats()
    
    def load_debts(self):
        """
        تحميل ديون الزبون
        """
        try:
            debts = self.debt_controller.get_debts_by_person(self.person.id)
            self.person_all_debts = debts
            self.filter_debts() # يقوم بالفلترة وعرض البيانات وتحديث الإحصائيات
        except Exception as e:
            MessageHelper.show_error(self, "خطأ", f"حدث خطأ أثناء تحميل الديون: {str(e)}")

    def populate_debts_table(self, debts: list):
        """
        ملء جدول الديون بالبيانات
        """
        self.debts_table.setRowCount(len(debts))
        
        for row, debt in enumerate(debts):
            id_item = QTableWidgetItem(str(debt.id))
            id_item.setData(Qt.UserRole, debt)
            self.debts_table.setItem(row, 0, id_item)
            
            amount_item = QTableWidgetItem(NumberHelper.format_currency(debt.amount))
            amount_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.debts_table.setItem(row, 1, amount_item)
            
            self.debts_table.setItem(row, 2, QTableWidgetItem(debt.description))
            
            due_date = DateHelper.format_date(debt.due_date) if debt.due_date else "غير محدد"
            self.debts_table.setItem(row, 3, QTableWidgetItem(due_date))
            
            status_item = QTableWidgetItem()
            from datetime import date
            is_overdue = not debt.is_paid and debt.due_date and debt.due_date < date.today()

            if debt.is_paid:
                status_item.setText("مدفوع")
                status_item.setForeground(QColor("#28a745"))
            elif is_overdue:
                status_item.setText("متأخر")
                status_item.setForeground(QColor("#dc3545"))
            else:
                status_item.setText("غير مدفوع")
                status_item.setForeground(QColor("#ffc107"))
            self.debts_table.setItem(row, 4, status_item)
            
            created_date = DateHelper.format_datetime(debt.created_at) if debt.created_at else ""
            self.debts_table.setItem(row, 5, QTableWidgetItem(created_date))

        self.debts_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)

    def filter_debts(self):
        """
        فلترة ديون الزبون
        """
        if not hasattr(self, 'person_all_debts'):
            return
        
        search_term = self.debt_search_input.text().strip().lower()
        status_filter = self.debt_status_filter.currentText()
        
        filtered = []
        from datetime import date

        for debt in self.person_all_debts:
            if search_term and not (search_term in debt.description.lower() or search_term in str(debt.amount)):
                continue
            
            is_overdue = not debt.is_paid and debt.due_date and debt.due_date < date.today()

            if status_filter == "مدفوع" and not debt.is_paid:
                continue
            if status_filter == "غير مدفوع" and (debt.is_paid or is_overdue):
                continue
            if status_filter == "متأخر" and not is_overdue:
                continue
            
            filtered.append(debt)
        
        self.populate_debts_table(filtered)
        self.update_debts_statistics()

    def update_debts_statistics(self):
        """
        تحديث إحصائيات ديون الزبون
        """
        if not hasattr(self, 'person_all_debts'):
            return

        total_amount = sum(d.amount for d in self.person_all_debts)
        paid_amount = sum(d.amount for d in self.person_all_debts if d.is_paid)
        unpaid_amount = total_amount - paid_amount
        
        from datetime import date
        overdue_count = sum(1 for d in self.person_all_debts if not d.is_paid and d.due_date and d.due_date < date.today())
        overdue_amount = sum(d.amount for d in self.person_all_debts if not d.is_paid and d.due_date and d.due_date < date.today())

        self.person_total_debts_label.setText(f"الإجمالي: {len(self.person_all_debts)} ({NumberHelper.format_currency(total_amount)})")
        self.person_paid_debts_label.setText(f"مدفوع: {sum(1 for d in self.person_all_debts if d.is_paid)} ({NumberHelper.format_currency(paid_amount)})")
        self.person_unpaid_debts_label.setText(f"غير مدفوع: {sum(1 for d in self.person_all_debts if not d.is_paid and not (d.due_date and d.due_date < date.today()))} ({NumberHelper.format_currency(unpaid_amount - overdue_amount)})")
        self.person_overdue_debts_label.setText(f"متأخر: {overdue_count} ({NumberHelper.format_currency(overdue_amount)})")
    
    def load_installments(self):
        """
        تحميل أقساط الزبون
        """
        try:
            installments = self.installment_controller.get_installments_by_person(self.person.id)
            self.person_all_installments = installments
            self.filter_installments()
        except Exception as e:
            MessageHelper.show_error(self, "خطأ", f"حدث خطأ أثناء تحميل الأقساط: {str(e)}")

    def populate_installments_table(self, installments: list):
        """
        ملء جدول الأقساط بالبيانات
        """
        self.installments_table.setRowCount(len(installments))
        
        for row, inst in enumerate(installments):
            id_item = QTableWidgetItem(str(inst.id))
            id_item.setData(Qt.UserRole, inst)
            self.installments_table.setItem(row, 0, id_item)
            
            self.installments_table.setItem(row, 1, QTableWidgetItem(NumberHelper.format_currency(inst.total_amount)))
            self.installments_table.setItem(row, 2, QTableWidgetItem(NumberHelper.format_currency(inst.paid_amount)))
            self.installments_table.setItem(row, 3, QTableWidgetItem(NumberHelper.format_currency(inst.remaining_amount)))
            self.installments_table.setItem(row, 4, QTableWidgetItem(inst.description))
            
            percentage = NumberHelper.format_percentage(inst.completion_percentage)
            progress_item = QTableWidgetItem(percentage)
            progress_item.setTextAlignment(Qt.AlignCenter)
            
            # تلوين نسبة الإنجاز
            if inst.completion_percentage >= 100:
                progress_item.setBackground(QColor("#28a745"))
                progress_item.setForeground(QColor("white"))
            elif inst.completion_percentage >= 50:
                progress_item.setBackground(QColor("#ffc107"))
                progress_item.setForeground(QColor("black"))
            else:
                progress_item.setBackground(QColor("#dc3545"))
                progress_item.setForeground(QColor("white"))

            self.installments_table.setItem(row, 5, progress_item)
            
            status = "مكتمل" if inst.is_completed else "نشط"
            status_item = QTableWidgetItem(status)
            if inst.is_completed:
                status_item.setBackground(QColor("#28a745"))
                status_item.setForeground(QColor("white"))
            else:
                status_item.setBackground(QColor("#007bff"))
                status_item.setForeground(QColor("white"))

            self.installments_table.setItem(row, 6, status_item)
            
            start_date = DateHelper.format_date(inst.start_date) if inst.start_date else "غير محدد"
            self.installments_table.setItem(row, 7, QTableWidgetItem(start_date))

        self.installments_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)

    def filter_installments(self):
        """
        فلترة أقساط الزبون
        """
        if not hasattr(self, 'person_all_installments'):
            return
        
        search_term = self.inst_search_input.text().strip().lower()
        status_filter = self.inst_status_filter.currentText()
        
        filtered = [
            inst for inst in self.person_all_installments
            if (not search_term or (search_term in inst.description.lower() or search_term in str(inst.total_amount)))
            and (status_filter == "الكل" or (status_filter == "نشط" and not inst.is_completed) or (status_filter == "مكتمل" and inst.is_completed))
        ]
        
        self.populate_installments_table(filtered)
        self.update_installments_statistics()

    def update_installments_statistics(self):
        """
        تحديث إحصائيات أقساط الزبون
        """
        if not hasattr(self, 'person_all_installments'):
            return

        all_installments = self.person_all_installments
        total_count = len(all_installments)
        active_count = sum(1 for i in all_installments if not i.is_completed)
        completed_count = total_count - active_count
        total_amount = sum(i.total_amount for i in all_installments)
        paid_amount = sum(i.paid_amount for i in all_installments)

        self.person_total_installments_label.setText(f"الإجمالي: {total_count}")
        self.person_active_installments_label.setText(f"نشط: {active_count}")
        self.person_completed_installments_label.setText(f"مكتمل: {completed_count}")
        self.person_total_amount_label.setText(f"إجمالي المبالغ: {NumberHelper.format_currency(total_amount)}")
        self.person_paid_amount_label.setText(f"المدفوع: {NumberHelper.format_currency(paid_amount)}")
    
    def load_internet_subscriptions(self):
        """
        تحميل اشتراكات الإنترنت للزبون
        """
        try:
            subscriptions = self.internet_controller.get_subscriptions_by_person(self.person.id)
            self.person_all_subscriptions = subscriptions
            self.filter_internet_subscriptions()
        except Exception as e:
            MessageHelper.show_error(self, "خطأ", f"حدث خطأ أثناء تحميل اشتراكات الإنترنت: {str(e)}")

    def populate_internet_table(self, subscriptions: list):
        """
        ملء جدول اشتراكات الإنترنت بالبيانات
        """
        self.internet_table.setRowCount(len(subscriptions))
        from datetime import date

        for row, sub in enumerate(subscriptions):
            id_item = QTableWidgetItem(str(sub.id))
            id_item.setData(Qt.UserRole, sub)
            self.internet_table.setItem(row, 0, id_item)
            
            self.internet_table.setItem(row, 1, QTableWidgetItem(sub.plan_name))
            self.internet_table.setItem(row, 2, QTableWidgetItem(NumberHelper.format_currency(sub.monthly_fee)))
            self.internet_table.setItem(row, 3, QTableWidgetItem(DateHelper.format_date(sub.start_date)))
            self.internet_table.setItem(row, 4, QTableWidgetItem(DateHelper.format_date(sub.end_date)))

            status_text, status_color = self.get_subscription_status_display(sub)
            status_item = QTableWidgetItem(status_text)
            status_item.setBackground(status_color)
            self.internet_table.setItem(row, 5, status_item)

            payment_text = "مدفوع" if sub.payment_status == 'paid' else "غير مدفوع"
            payment_item = QTableWidgetItem(payment_text)
            payment_item.setForeground(QColor("#28a745") if sub.payment_status == 'paid' else QColor("#dc3545"))
            self.internet_table.setItem(row, 6, payment_item)

            days_remaining = (sub.end_date - date.today()).days if sub.end_date else -1
            days_item = QTableWidgetItem(str(days_remaining) if days_remaining >= 0 else "منتهي")
            self.internet_table.setItem(row, 7, days_item)

        self.internet_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)

    def filter_internet_subscriptions(self):
        """
        فلترة اشتراكات الإنترنت للزبون
        """
        if not hasattr(self, 'person_all_subscriptions'):
            return

        search_term = self.net_search_input.text().strip().lower()
        status_filter = self.net_status_filter.currentText()
        
        filtered = []
        for sub in self.person_all_subscriptions:
            if search_term and search_term not in sub.plan_name.lower():
                continue
            
            status_text, _ = self.get_subscription_status_display(sub)
            if status_filter != "الكل" and status_filter != status_text:
                continue
            
            filtered.append(sub)
        
        self.populate_internet_table(filtered)
        self.update_internet_statistics()

    def update_internet_statistics(self):
        """
        تحديث إحصائيات اشتراكات الإنترنت للزبون
        """
        if not hasattr(self, 'person_all_subscriptions'):
            return

        total = len(self.person_all_subscriptions)
        active = sum(1 for s in self.person_all_subscriptions if self.get_subscription_status_display(s)[0] == 'نشط')
        expired = sum(1 for s in self.person_all_subscriptions if self.get_subscription_status_display(s)[0] == 'منتهي')

        self.person_total_subs_label.setText(f"الإجمالي: {total}")
        self.person_active_subs_label.setText(f"نشط: {active}")
        self.person_expired_subs_label.setText(f"منتهي: {expired}")

    def get_subscription_status_display(self, subscription):
        """
        الحصول على نص ولون حالة الاشتراك
        """
        from datetime import date
        today = date.today()
        if not subscription.end_date or not subscription.start_date:
            return "غير محدد", QColor("gray")
        
        if subscription.end_date < today:
            return "منتهي", QColor("red")
        elif subscription.start_date <= today:
            return "نشط", QColor("green")
        else:
            return "لم يبدأ بعد", QColor("blue")
    
    def on_debt_selection_changed(self):
        """
        معالجة تغيير التحديد في جدول الديون
        """
        has_selection = self.debts_table.currentRow() >= 0
        self.edit_debt_btn.setEnabled(has_selection)
        self.delete_debt_btn.setEnabled(has_selection)
        
        # تفعيل زر "وضع علامة مدفوع" للديون غير المدفوعة فقط
        if has_selection:
            current_row = self.debts_table.currentRow()
            debt_item = self.debts_table.item(current_row, 0)
            if debt_item:
                debt = debt_item.data(Qt.UserRole)
                self.mark_paid_btn.setEnabled(debt and not debt.is_paid)
            else:
                self.mark_paid_btn.setEnabled(False)
        else:
            self.mark_paid_btn.setEnabled(False)
    
    def on_installment_selection_changed(self):
        """
        معالجة تغيير التحديد في جدول الأقساط
        """
        has_selection = self.installments_table.currentRow() >= 0
        self.edit_installment_btn.setEnabled(has_selection)
        self.delete_installment_btn.setEnabled(has_selection)
        self.installment_details_btn.setEnabled(has_selection)
        
        if has_selection:
            current_row = self.installments_table.currentRow()
            installment_item = self.installments_table.item(current_row, 0)
            if installment_item:
                installment = installment_item.data(Qt.UserRole)
                self.add_payment_btn.setEnabled(installment and not installment.is_completed)
            else:
                self.add_payment_btn.setEnabled(False)
        else:
            self.add_payment_btn.setEnabled(False)
    
    def on_internet_selection_changed(self):
        """
        معالجة تغيير التحديد في جدول اشتراكات الإنترنت
        """
        has_selection = self.internet_table.currentRow() >= 0
        self.edit_internet_btn.setEnabled(has_selection)
        self.delete_internet_btn.setEnabled(has_selection)
        
        if has_selection:
            current_row = self.internet_table.currentRow()
            item = self.internet_table.item(current_row, 0)
            if item:
                sub = item.data(Qt.UserRole)
                self.mark_internet_paid_btn.setEnabled(sub and sub.payment_status == 'unpaid')
            else:
                self.mark_internet_paid_btn.setEnabled(False)
        else:
            self.mark_internet_paid_btn.setEnabled(False)
    
    # يمكنني إضافة باقي الدوال للتعامل مع العمليات (إضافة، تعديل، حذف) 
    # لكن سأكتفي بهذا القدر لتوفير المساحة
    
    def add_debt(self):
        """
        إضافة دين جديد
        """
        dialog = AddDebtDialog(self, person_id=self.person.id)
        if dialog.exec_() == dialog.Accepted:
            debt_data = dialog.get_debt_data()
            
            success, message, debt_id = self.debt_controller.add_debt(
                self.person.id,
                debt_data['amount'],
                debt_data['description'],
                debt_data['due_date']
            )
            
            if success:
                MessageHelper.show_info(self, "نجح", message)
                self.load_debts()
                self.update_stats()
            else:
                MessageHelper.show_error(self, "خطأ", message)

    def edit_debt(self):
        """
        تعديل الدين المحدد
        """
        current_row = self.debts_table.currentRow()
        if current_row < 0:
            return
            
        debt_item = self.debts_table.item(current_row, 0)
        debt = debt_item.data(Qt.UserRole)
        
        dialog = AddDebtDialog(self, debt=debt, person_id=self.person.id)
        if dialog.exec_() == dialog.Accepted:
            debt_data = dialog.get_debt_data()
            
            success, message = self.debt_controller.update_debt(
                debt.id,
                debt_data['amount'],
                debt_data['description'],
                debt_data['due_date'],
                debt_data['is_paid']
            )
            
            if success:
                MessageHelper.show_info(self, "نجح", message)
                self.load_debts()
                self.update_stats()
            else:
                MessageHelper.show_error(self, "خطأ", message)

    def delete_debt(self):
        """
        حذف الدين المحدد
        """
        current_row = self.debts_table.currentRow()
        if current_row < 0:
            return
            
        debt_item = self.debts_table.item(current_row, 0)
        debt = debt_item.data(Qt.UserRole)
        
        if MessageHelper.show_question(self, "تأكيد", f"هل أنت متأكد من حذف الدين '{debt.description}'؟"):
            success, message = self.debt_controller.delete_debt(debt.id)
            
            if success:
                MessageHelper.show_info(self, "نجح", message)
                self.load_debts()
                self.update_stats()
            else:
                MessageHelper.show_error(self, "خطأ", message)

    def mark_debt_paid(self):
        """
        وضع علامة مدفوع على الدين المحدد
        """
        current_row = self.debts_table.currentRow()
        if current_row < 0:
            return
            
        debt_item = self.debts_table.item(current_row, 0)
        debt = debt_item.data(Qt.UserRole)
        
        if MessageHelper.show_question(self, "تأكيد", f"هل أنت متأكد من وضع علامة 'مدفوع' على الدين '{debt.description}'؟"):
            success, message = self.debt_controller.mark_debt_as_paid(debt.id)
            
            if success:
                MessageHelper.show_info(self, "نجح", message)
                self.load_debts()
                self.update_stats()
            else:
                MessageHelper.show_error(self, "خطأ", message)

    def add_installment(self):
        """
        إضافة قسط جديد
        """
        dialog = AddInstallmentDialog(self, person_id=self.person.id)
        if dialog.exec_() == dialog.Accepted:
            data = dialog.get_installment_data()
            
            success, message, _ = self.installment_controller.add_installment(
                self.person.id,
                data['total_amount'],
                data['description'],
                data['start_date']
            )
            
            if success:
                MessageHelper.show_info(self, "نجح", message)
                self.load_installments()
                self.update_stats()
            else:
                MessageHelper.show_error(self, "خطأ", message)

    def edit_installment(self):
        """
        تعديل القسط المحدد
        """
        current_row = self.installments_table.currentRow()
        if current_row < 0:
            return
            
        item = self.installments_table.item(current_row, 0)
        installment = item.data(Qt.UserRole)
        
        dialog = AddInstallmentDialog(self, installment=installment, person_id=self.person.id)
        if dialog.exec_() == dialog.Accepted:
            data = dialog.get_installment_data()
            
            success, message = self.installment_controller.update_installment(
                installment.id,
                data['total_amount'],
                data['description'],
                data['start_date']
            )
            
            if success:
                MessageHelper.show_info(self, "نجح", message)
                self.load_installments()
                self.update_stats()
            else:
                MessageHelper.show_error(self, "خطأ", message)

    def delete_installment(self):
        """
        حذف القسط المحدد
        """
        current_row = self.installments_table.currentRow()
        if current_row < 0:
            return
            
        item = self.installments_table.item(current_row, 0)
        installment = item.data(Qt.UserRole)
        
        if MessageHelper.show_question(self, "تأكيد", f"هل أنت متأكد من حذف القسط '{installment.description}'؟"):
            success, message = self.installment_controller.delete_installment(installment.id)
            
            if success:
                MessageHelper.show_info(self, "نجح", message)
                self.load_installments()
                self.update_stats()
            else:
                MessageHelper.show_error(self, "خطأ", message)

    def add_installment_payment(self):
        """
        إضافة دفعة للقسط المحدد
        """
        current_row = self.installments_table.currentRow()
        if current_row < 0:
            return
            
        item = self.installments_table.item(current_row, 0)
        installment = item.data(Qt.UserRole)

        if not installment or installment.is_completed:
            return

        remaining = installment.remaining_amount
        payment_amount, ok = QInputDialog.getDouble(
            self, "إضافة دفعة", 
            f"أدخل مبلغ الدفعة:\nالمبلغ المتبقي: {NumberHelper.format_currency(remaining)}",
            0.0, 0.0, remaining, 2
        )
        
        if ok and payment_amount > 0:
            success, message = self.installment_controller.add_payment(installment.id, payment_amount)
            
            if success:
                MessageHelper.show_info(self, "نجح", message)
                self.load_installments()
                self.update_stats()
            else:
                MessageHelper.show_error(self, "خطأ", message)

    def show_installment_details(self):
        """
        عرض تفاصيل القسط المحدد
        """
        current_row = self.installments_table.currentRow()
        if current_row < 0:
            return
            
        item = self.installments_table.item(current_row, 0)
        installment = item.data(Qt.UserRole)
        
        updated_installment = self.installment_controller.get_installment_by_id(installment.id)
        if not updated_installment:
            MessageHelper.show_error(self, "خطأ", "لم يتم العثور على القسط.")
            self.load_installments()
            return
        
        dialog = InstallmentDetailsDialog(updated_installment, self.installment_controller.db, self)
        dialog.exec_()
        
        self.load_installments()
        self.update_stats()

    def add_internet_subscription(self):
        """
        إضافة اشتراك إنترنت جديد
        """
        dialog = AddInternetDialog(self, person_id=self.person.id)
        if dialog.exec_() == dialog.Accepted:
            data = dialog.get_subscription_data()
            
            success, message, _ = self.internet_controller.add_subscription(
                self.person.id,
                data['plan_name'],
                data['monthly_fee'],
                data['start_date'],
                data['end_date']
            )
            
            if success:
                MessageHelper.show_info(self, "نجح", message)
                self.load_internet_subscriptions()
                self.update_stats()
            else:
                MessageHelper.show_error(self, "خطأ", message)

    def edit_internet_subscription(self):
        """
        تعديل اشتراك الإنترنت المحدد
        """
        current_row = self.internet_table.currentRow()
        if current_row < 0:
            return
            
        item = self.internet_table.item(current_row, 0)
        subscription = item.data(Qt.UserRole)
        
        dialog = AddInternetDialog(self, subscription=subscription, person_id=self.person.id)
        if dialog.exec_() == dialog.Accepted:
            data = dialog.get_subscription_data()
            
            success, message = self.internet_controller.update_subscription(
                subscription.id,
                data['plan_name'],
                data['monthly_fee'],
                data['start_date'],
                data['end_date'],
                data['is_active']
            )
            
            if success:
                MessageHelper.show_info(self, "نجح", message)
                self.load_internet_subscriptions()
                self.update_stats()
            else:
                MessageHelper.show_error(self, "خطأ", message)

    def delete_internet_subscription(self):
        """
        حذف اشتراك الإنترنت المحدد
        """
        current_row = self.internet_table.currentRow()
        if current_row < 0:
            return
            
        item = self.internet_table.item(current_row, 0)
        subscription = item.data(Qt.UserRole)
        
        if MessageHelper.show_question(self, "تأكيد", f"هل أنت متأكد من حذف الاشتراك '{subscription.plan_name}'؟"):
            success, message = self.internet_controller.delete_subscription(subscription.id)
            
            if success:
                MessageHelper.show_info(self, "نجح", message)
                self.load_internet_subscriptions()
                self.update_stats()
            else:
                MessageHelper.show_error(self, "خطأ", message)

    def mark_subscription_paid(self):
        """
        وضع علامة مدفوع على الاشتراك المحدد
        """
        current_row = self.internet_table.currentRow()
        if current_row < 0:
            return
            
        item = self.internet_table.item(current_row, 0)
        subscription = item.data(Qt.UserRole)

        if not subscription or subscription.payment_status == 'paid':
            return

        if MessageHelper.show_question(self, "تأكيد", f"هل أنت متأكد من وضع علامة 'مدفوع' على الاشتراك '{subscription.plan_name}'؟"):
            success, message = self.internet_controller.update_subscription_payment_status(subscription.id, 'paid')
            
            if success:
                MessageHelper.show_info(self, "نجح", message)
                self.load_internet_subscriptions()
                self.update_stats()
            else:
                MessageHelper.show_error(self, "خطأ", message)
