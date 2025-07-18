# -*- coding: utf-8 -*-
"""
نافذة تفاصيل الزبون
تعرض جميع البيانات المرتبطة بالزبون في تبويبات منفصلة
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QTableWidget, QTableWidgetItem, QLineEdit,
                             QLabel, QHeaderView, QFrame, QTabWidget, QTextEdit)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from database.models import Person
from controllers.person_controller import PersonController
from controllers.debt_controller import DebtController
from controllers.installment_controller import InstallmentController
from controllers.internet_controller import InternetController
from utils.helpers import MessageHelper, AppHelper, TableHelper, DateHelper, NumberHelper
from views.dialogs.add_debt_dialog import AddDebtDialog
from views.dialogs.add_installment_dialog import AddInstallmentDialog
from views.dialogs.add_internet_dialog import AddInternetDialog


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
                font-size: 18px;
                font-weight: bold;
                background: transparent;
            }
        """)
        person_info.addWidget(name_label)
        
        phone_label = QLabel(f"الهاتف: {self.person.phone or 'غير محدد'}")
        phone_label.setStyleSheet("""
            QLabel {
                color: #e3f2fd;
                font-size: 14px;
                background: transparent;
            }
        """)
        person_info.addWidget(phone_label)
        
        address_label = QLabel(f"العنوان: {self.person.address or 'غير محدد'}")
        address_label.setStyleSheet("""
            QLabel {
                color: #e3f2fd;
                font-size: 14px;
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
                    font-size: 12px;
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
                        font-size: 12px;
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
                    font-size: 12px;
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
        
        # شريط الأدوات
        toolbar = QHBoxLayout()
        
        self.add_debt_btn = QPushButton("إضافة دين")
        self.edit_debt_btn = QPushButton("تعديل")
        self.delete_debt_btn = QPushButton("حذف")
        self.mark_paid_btn = QPushButton("وضع علامة مدفوع")
        
        # تنسيق الأزرار
        for btn in [self.add_debt_btn, self.edit_debt_btn, self.delete_debt_btn, self.mark_paid_btn]:
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
        
        self.delete_debt_btn.setStyleSheet(self.delete_debt_btn.styleSheet().replace("#007bff", "#dc3545").replace("#0056b3", "#c82333"))
        self.mark_paid_btn.setStyleSheet(self.mark_paid_btn.styleSheet().replace("#007bff", "#28a745").replace("#0056b3", "#218838"))
        
        # تعطيل الأزرار في البداية
        self.edit_debt_btn.setEnabled(False)
        self.delete_debt_btn.setEnabled(False)
        self.mark_paid_btn.setEnabled(False)
        
        toolbar.addWidget(self.add_debt_btn)
        toolbar.addWidget(self.edit_debt_btn)
        toolbar.addWidget(self.delete_debt_btn)
        toolbar.addWidget(self.mark_paid_btn)
        toolbar.addStretch()
        
        layout.addLayout(toolbar)
        
        # جدول الديون
        self.debts_table = QTableWidget()
        headers = ["المعرف", "المبلغ", "الوصف", "تاريخ الاستحقاق", "الحالة", "تاريخ الإضافة"]
        TableHelper.setup_table_headers(self.debts_table, headers)
        
        self.debts_table.setAlternatingRowColors(True)
        self.debts_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.debts_table.setColumnHidden(0, True)  # إخفاء عمود المعرف
        
        layout.addWidget(self.debts_table)
        
        return tab
    
    def create_installments_tab(self) -> QWidget:
        """
        إنشاء تبويب الأقساط
        
        Returns:
            QWidget: تبويب الأقساط
        """
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # شريط الأدوات
        toolbar = QHBoxLayout()
        
        self.add_installment_btn = QPushButton("إضافة قسط")
        self.edit_installment_btn = QPushButton("تعديل")
        self.delete_installment_btn = QPushButton("حذف")
        self.add_payment_btn = QPushButton("إضافة دفعة")
        
        # تنسيق الأزرار
        for btn in [self.add_installment_btn, self.edit_installment_btn, self.delete_installment_btn, self.add_payment_btn]:
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
        
        self.delete_installment_btn.setStyleSheet(self.delete_installment_btn.styleSheet().replace("#f39c12", "#dc3545").replace("#e67e22", "#c82333"))
        self.add_payment_btn.setStyleSheet(self.add_payment_btn.styleSheet().replace("#f39c12", "#28a745").replace("#e67e22", "#218838"))
        
        # تعطيل الأزرار في البداية
        self.edit_installment_btn.setEnabled(False)
        self.delete_installment_btn.setEnabled(False)
        self.add_payment_btn.setEnabled(False)
        
        toolbar.addWidget(self.add_installment_btn)
        toolbar.addWidget(self.edit_installment_btn)
        toolbar.addWidget(self.delete_installment_btn)
        toolbar.addWidget(self.add_payment_btn)
        toolbar.addStretch()
        
        layout.addLayout(toolbar)
        
        # جدول الأقساط
        self.installments_table = QTableWidget()
        headers = ["المعرف", "المبلغ الإجمالي", "الدورية", "الوصف", "نسبة الإنجاز", "الحالة"]
        TableHelper.setup_table_headers(self.installments_table, headers)
        
        self.installments_table.setAlternatingRowColors(True)
        self.installments_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.installments_table.setColumnHidden(0, True)  # إخفاء عمود المعرف
        
        layout.addWidget(self.installments_table)
        
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
        
        # شريط الأدوات
        toolbar = QHBoxLayout()
        
        self.add_internet_btn = QPushButton("إضافة اشتراك")
        self.edit_internet_btn = QPushButton("تعديل")
        self.delete_internet_btn = QPushButton("حذف")
        self.toggle_active_btn = QPushButton("تفعيل/إلغاء")
        
        # تنسيق الأزرار
        for btn in [self.add_internet_btn, self.edit_internet_btn, self.delete_internet_btn, self.toggle_active_btn]:
            btn.setMinimumHeight(35)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #27ae60;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    padding: 8px 16px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #229954;
                }
                QPushButton:disabled {
                    background-color: #6c757d;
                }
            """)
        
        self.delete_internet_btn.setStyleSheet(self.delete_internet_btn.styleSheet().replace("#27ae60", "#dc3545").replace("#229954", "#c82333"))
        
        # تعطيل الأزرار في البداية
        self.edit_internet_btn.setEnabled(False)
        self.delete_internet_btn.setEnabled(False)
        self.toggle_active_btn.setEnabled(False)
        
        toolbar.addWidget(self.add_internet_btn)
        toolbar.addWidget(self.edit_internet_btn)
        toolbar.addWidget(self.delete_internet_btn)
        toolbar.addWidget(self.toggle_active_btn)
        toolbar.addStretch()
        
        layout.addLayout(toolbar)
        
        # جدول اشتراكات الإنترنت
        self.internet_table = QTableWidget()
        headers = ["المعرف", "اسم الباقة", "الرسوم الشهرية", "السرعة", "تاريخ البداية", "تاريخ النهاية", "الحالة"]
        TableHelper.setup_table_headers(self.internet_table, headers)
        
        self.internet_table.setAlternatingRowColors(True)
        self.internet_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.internet_table.setColumnHidden(0, True)  # إخفاء عمود المعرف
        
        layout.addWidget(self.internet_table)
        
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
        
        # أحداث الأقساط
        self.add_installment_btn.clicked.connect(self.add_installment)
        self.edit_installment_btn.clicked.connect(self.edit_installment)
        self.delete_installment_btn.clicked.connect(self.delete_installment)
        self.add_payment_btn.clicked.connect(self.add_installment_payment)
        self.installments_table.selectionModel().selectionChanged.connect(self.on_installment_selection_changed)
        
        # أحداث اشتراكات الإنترنت
        self.add_internet_btn.clicked.connect(self.add_internet_subscription)
        self.edit_internet_btn.clicked.connect(self.edit_internet_subscription)
        self.delete_internet_btn.clicked.connect(self.delete_internet_subscription)
        self.toggle_active_btn.clicked.connect(self.toggle_internet_subscription)
        self.internet_table.selectionModel().selectionChanged.connect(self.on_internet_selection_changed)
    
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
            
            self.debts_table.setRowCount(len(debts))
            
            for row, debt in enumerate(debts):
                # إخفاء المعرف في عمود مخفي
                id_item = QTableWidgetItem(str(debt.id))
                id_item.setData(Qt.UserRole, debt)
                self.debts_table.setItem(row, 0, id_item)
                
                # المبلغ
                amount_item = QTableWidgetItem(NumberHelper.format_currency(debt.amount))
                amount_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.debts_table.setItem(row, 1, amount_item)
                
                # الوصف
                self.debts_table.setItem(row, 2, QTableWidgetItem(debt.description))
                
                # تاريخ الاستحقاق
                due_date = DateHelper.format_date(debt.due_date) if debt.due_date else "غير محدد"
                self.debts_table.setItem(row, 3, QTableWidgetItem(due_date))
                
                # الحالة
                status = "مدفوع" if debt.is_paid else "غير مدفوع"
                status_item = QTableWidgetItem(status)
                if debt.is_paid:
                    status_item.setBackground(Qt.green)
                    status_item.setForeground(Qt.white)
                else:
                    status_item.setBackground(Qt.red)
                    status_item.setForeground(Qt.white)
                self.debts_table.setItem(row, 4, status_item)
                
                # تاريخ الإضافة
                created_date = DateHelper.format_datetime(debt.created_at) if debt.created_at else ""
                self.debts_table.setItem(row, 5, QTableWidgetItem(created_date))
            
        except Exception as e:
            MessageHelper.show_error(self, "خطأ", f"حدث خطأ أثناء تحميل الديون: {str(e)}")
    
    def load_installments(self):
        """
        تحميل أقساط الزبون
        """
        try:
            installments = self.installment_controller.get_installments_by_person(self.person.id)
            
            self.installments_table.setRowCount(len(installments))
            
            for row, installment in enumerate(installments):
                # إخفاء المعرف في عمود مخفي
                id_item = QTableWidgetItem(str(installment.id))
                id_item.setData(Qt.UserRole, installment)
                self.installments_table.setItem(row, 0, id_item)
                
                # المبلغ الإجمالي
                total_item = QTableWidgetItem(NumberHelper.format_currency(installment.total_amount))
                total_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.installments_table.setItem(row, 1, total_item)
                
                # الدورية
                frequency_map = {"monthly": "شهري", "weekly": "أسبوعي", "yearly": "سنوي"}
                frequency_text = frequency_map.get(installment.frequency, installment.frequency)
                self.installments_table.setItem(row, 2, QTableWidgetItem(frequency_text))
                
                # الوصف
                self.installments_table.setItem(row, 3, QTableWidgetItem(installment.description))
                
                # نسبة الإنجاز
                percentage = NumberHelper.format_percentage(installment.completion_percentage)
                self.installments_table.setItem(row, 4, QTableWidgetItem(percentage))
                
                # الحالة
                status = "مكتمل" if installment.is_completed else "نشط"
                status_item = QTableWidgetItem(status)
                if installment.is_completed:
                    status_item.setBackground(Qt.green)
                    status_item.setForeground(Qt.white)
                else:
                    status_item.setBackground(Qt.blue)
                    status_item.setForeground(Qt.white)
                self.installments_table.setItem(row, 5, status_item)
            
        except Exception as e:
            MessageHelper.show_error(self, "خطأ", f"حدث خطأ أثناء تحميل الأقساط: {str(e)}")
    
    def load_internet_subscriptions(self):
        """
        تحميل اشتراكات الإنترنت للزبون
        """
        try:
            subscriptions = self.internet_controller.get_subscriptions_by_person(self.person.id)
            
            self.internet_table.setRowCount(len(subscriptions))
            
            for row, subscription in enumerate(subscriptions):
                # إخفاء المعرف في عمود مخفي
                id_item = QTableWidgetItem(str(subscription.id))
                id_item.setData(Qt.UserRole, subscription)
                self.internet_table.setItem(row, 0, id_item)
                
                # اسم الباقة
                self.internet_table.setItem(row, 1, QTableWidgetItem(subscription.plan_name))
                
                # الرسوم الشهرية
                fee_item = QTableWidgetItem(NumberHelper.format_currency(subscription.monthly_fee))
                fee_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.internet_table.setItem(row, 2, fee_item)
                
                # السرعة
                self.internet_table.setItem(row, 3, QTableWidgetItem(subscription.speed or "غير محدد"))
                
                # تاريخ البداية
                start_date = DateHelper.format_date(subscription.start_date) if subscription.start_date else "غير محدد"
                self.internet_table.setItem(row, 4, QTableWidgetItem(start_date))
                
                # تاريخ النهاية
                end_date = DateHelper.format_date(subscription.end_date) if subscription.end_date else "غير محدد"
                self.internet_table.setItem(row, 5, QTableWidgetItem(end_date))
                
                # الحالة
                status = "نشط" if subscription.is_active else "غير نشط"
                status_item = QTableWidgetItem(status)
                if subscription.is_active:
                    status_item.setBackground(Qt.green)
                    status_item.setForeground(Qt.white)
                else:
                    status_item.setBackground(Qt.red)
                    status_item.setForeground(Qt.white)
                self.internet_table.setItem(row, 6, status_item)
            
        except Exception as e:
            MessageHelper.show_error(self, "خطأ", f"حدث خطأ أثناء تحميل اشتراكات الإنترنت: {str(e)}")
    
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
        
        # تفعيل زر "إضافة دفعة" للأقساط غير المكتملة فقط
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
        self.toggle_active_btn.setEnabled(has_selection)
    
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
        
        if MessageHelper.confirm(self, "تأكيد", f"هل أنت متأكد من حذف الدين '{debt.description}'؟"):
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
        
        if MessageHelper.confirm(self, "تأكيد", f"هل أنت متأكد من وضع علامة 'مدفوع' على الدين '{debt.description}'؟"):
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
                data['frequency'],
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
                data['frequency'],
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
        
        if MessageHelper.confirm(self, "تأكيد", f"هل أنت متأكد من حذف القسط '{installment.description}'؟"):
            success, message = self.installment_controller.delete_installment(installment.id)
            
            if success:
                MessageHelper.show_info(self, "نجح", message)
                self.load_installments()
                self.update_stats()
            else:
                MessageHelper.show_error(self, "خطأ", message)

    def add_installment_payment(self):
        # هذه الوظيفة تتطلب نافذة جديدة لإضافة دفعة، سيتم تبسيطها حاليًا
        MessageHelper.show_info(self, "غير متاح", "وظيفة إضافة دفعة غير متاحة حاليًا.")

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
                data['speed'],
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
                data['speed'],
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
        
        if MessageHelper.confirm(self, "تأكيد", f"هل أنت متأكد من حذف الاشتراك '{subscription.plan_name}'؟"):
            success, message = self.internet_controller.delete_subscription(subscription.id)
            
            if success:
                MessageHelper.show_info(self, "نجح", message)
                self.load_internet_subscriptions()
                self.update_stats()
            else:
                MessageHelper.show_error(self, "خطأ", message)

    def toggle_internet_subscription(self):
        """
        تفعيل أو إلغاء تفعيل اشتراك الإنترنت
        """
        current_row = self.internet_table.currentRow()
        if current_row < 0:
            return
            
        item = self.internet_table.item(current_row, 0)
        subscription = item.data(Qt.UserRole)
        
        if subscription.is_active:
            action_text = "إلغاء تفعيل"
            if MessageHelper.confirm(self, "تأكيد", f"هل أنت متأكد من {action_text} الاشتراك '{subscription.plan_name}'؟"):
                success, message = self.internet_controller.deactivate_subscription(subscription.id)
            else:
                return
        else:
            action_text = "تفعيل"
            if MessageHelper.confirm(self, "تأكيد", f"هل أنت متأكد من {action_text} الاشتراك '{subscription.plan_name}'؟"):
                success, message = self.internet_controller.activate_subscription(subscription.id)
            else:
                return

        if success:
            MessageHelper.show_info(self, "نجح", message)
            self.load_internet_subscriptions()
            self.update_stats()
        else:
            MessageHelper.show_error(self, "خطأ", message)
