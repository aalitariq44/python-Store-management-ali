# -*- coding: utf-8 -*-
"""
واجهة عرض جميع اشتراكات الإنترنت في النظام
تحتوي على عرض وإدارة جميع الاشتراكات مع بيانات الزبائن
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QTableWidget, QTableWidgetItem, QLineEdit,
                             QLabel, QHeaderView, QFrame, QComboBox, QCheckBox)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from datetime import date
from controllers.internet_controller import InternetController
from controllers.person_controller import PersonController
from database.models import InternetSubscription
from utils.helpers import MessageHelper, AppHelper, TableHelper, DateHelper, NumberHelper
from views.dialogs.add_internet_dialog import AddInternetDialog


class InternetView(QMainWindow):
    """
    واجهة عرض جميع اشتراكات الإنترنت
    """
    
    def __init__(self):
        super().__init__()
        self.internet_controller = InternetController()
        self.person_controller = PersonController()
        self.selected_subscription = None
        self.auto_refresh_timer = QTimer()
        self.init_ui()
        self.setup_connections()
        self.load_internet_subscriptions()
        self.setup_auto_refresh()
    
    def init_ui(self):
        """
        تهيئة واجهة المستخدم
        """
        self.setWindowTitle("إدارة اشتراكات الإنترنت")
        self.setMinimumSize(1500, 750)
        AppHelper.center_window(self, 1600, 850)
        
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
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #6c5ce7, stop:1 #74b9ff);
                border-radius: 10px;
                padding: 20px;
            }
        """)
        
        title_layout = QVBoxLayout(title_frame)
        
        title_label = QLabel("إدارة اشتراكات الإنترنت")
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
        
        subtitle_label = QLabel("عرض وإدارة جميع اشتراكات الإنترنت والباقات")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("""
            QLabel {
                color: #ddd;
                font-size: 24px;
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
        self.search_input.setPlaceholderText("ابحث باسم الباقة أو اسم الزبون...")
        self.search_input.setMaximumWidth(300)
        
        # فلتر الحالة
        status_label = QLabel("الحالة:")
        self.status_filter = QComboBox()
        self.status_filter.addItems(["الكل", "نشط", "منتهي"])
        self.status_filter.setMaximumWidth(120)
        
        # خيار التحديث التلقائي
        self.auto_refresh_checkbox = QCheckBox("التحديث التلقائي (30 ثانية)")
        self.auto_refresh_checkbox.setChecked(True)
        
        # الأزرار
        self.add_btn = QPushButton("إضافة اشتراك")
        self.edit_btn = QPushButton("تعديل")
        self.delete_btn = QPushButton("حذف")
        self.refresh_btn = QPushButton("تحديث")
        self.mark_paid_btn = QPushButton("وضع علامة كمدفوع")
        
        # تنسيق الأزرار
        buttons = [self.add_btn, self.edit_btn, self.delete_btn, self.refresh_btn, self.mark_paid_btn]
        for btn in buttons:
            btn.setMinimumHeight(35)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #6c5ce7;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    padding: 8px 16px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #5a4fcf;
                }
                QPushButton:disabled {
                    background-color: #6c757d;
                }
            """)
        
        # تلوين أزرار خاصة
        self.edit_btn.setStyleSheet(self.edit_btn.styleSheet().replace("#6c5ce7", "#28a745").replace("#5a4fcf", "#218838"))
        self.delete_btn.setStyleSheet(self.delete_btn.styleSheet().replace("#6c5ce7", "#dc3545").replace("#5a4fcf", "#c82333"))
        self.mark_paid_btn.setStyleSheet(self.mark_paid_btn.styleSheet().replace("#6c5ce7", "#17a2b8").replace("#5a4fcf", "#138496"))
        
        # تعطيل الأزرار في البداية
        self.edit_btn.setEnabled(False)
        self.delete_btn.setEnabled(False)
        self.mark_paid_btn.setEnabled(False)
        
        # ترتيب العناصر
        toolbar_layout.addWidget(search_label)
        toolbar_layout.addWidget(self.search_input)
        toolbar_layout.addWidget(status_label)
        toolbar_layout.addWidget(self.status_filter)
        toolbar_layout.addWidget(self.auto_refresh_checkbox)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.add_btn)
        toolbar_layout.addWidget(self.edit_btn)
        toolbar_layout.addWidget(self.delete_btn)
        toolbar_layout.addWidget(self.mark_paid_btn)
        toolbar_layout.addWidget(self.refresh_btn)
        
        layout.addWidget(toolbar_frame)
    
    def add_table(self, layout: QVBoxLayout):
        """
        إضافة جدول الاشتراكات
        """
        # إطار الجدول
        table_frame = QFrame()
        table_layout = QVBoxLayout(table_frame)
        
        # عنوان الجدول
        table_title = QLabel("قائمة اشتراكات الإنترنت")
        table_title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #495057;
                margin-bottom: 10px;
            }
        """)
        table_layout.addWidget(table_title)
        
        # الجدول
        self.table = QTableWidget()
        headers = ["المعرف", "اسم الزبون", "اسم الباقة", "التكلفة الشهرية", 
                  "تاريخ البداية", "تاريخ النهاية", "الحالة", "حالة الدفع", "الأيام المتبقية", "آخر تحديث"]
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
                background-color: #6c5ce7;
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
        
        self.total_subscriptions_label = QLabel("إجمالي الاشتراكات: -")
        self.active_subscriptions_label = QLabel("نشط: -")
        self.expired_subscriptions_label = QLabel("منتهي: -")
        self.paid_subscriptions_label = QLabel("مدفوع: -")
        self.unpaid_subscriptions_label = QLabel("غير مدفوع: -")
        self.total_revenue_label = QLabel("إجمالي الإيرادات: -")
        
        for label in [self.total_subscriptions_label, self.active_subscriptions_label, 
                     self.expired_subscriptions_label, self.paid_subscriptions_label, 
                     self.unpaid_subscriptions_label, self.total_revenue_label]:
            label.setStyleSheet("""
                QLabel {
                    font-weight: bold;
                    color: #495057;
                }
            """)
        
        status_layout.addWidget(self.total_subscriptions_label)
        status_layout.addWidget(self.active_subscriptions_label)
        status_layout.addWidget(self.expired_subscriptions_label)
        status_layout.addWidget(self.paid_subscriptions_label)
        status_layout.addWidget(self.unpaid_subscriptions_label)
        status_layout.addWidget(self.total_revenue_label)
        status_layout.addStretch()
        
        layout.addWidget(status_frame)
    
    def setup_connections(self):
        """
        إعداد الاتصالات والأحداث
        """
        # أحداث الأزرار
        self.add_btn.clicked.connect(self.add_internet_subscription)
        self.edit_btn.clicked.connect(self.edit_internet_subscription)
        self.delete_btn.clicked.connect(self.delete_internet_subscription)
        self.refresh_btn.clicked.connect(self.load_internet_subscriptions)
        self.mark_paid_btn.clicked.connect(self.mark_as_paid)
        
        # أحداث الجدول
        self.table.selectionModel().selectionChanged.connect(self.on_selection_changed)
        self.table.doubleClicked.connect(self.edit_internet_subscription)
        
        # أحداث البحث والفلترة
        self.search_input.textChanged.connect(self.filter_subscriptions)
        self.status_filter.currentTextChanged.connect(self.filter_subscriptions)
        
        # أحداث التحديث التلقائي
        self.auto_refresh_checkbox.toggled.connect(self.toggle_auto_refresh)
    
    def setup_auto_refresh(self):
        """
        إعداد التحديث التلقائي
        """
        self.auto_refresh_timer.timeout.connect(self.load_internet_subscriptions)
        if self.auto_refresh_checkbox.isChecked():
            self.auto_refresh_timer.start(30000)  # 30 ثانية
    
    def toggle_auto_refresh(self, enabled: bool):
        """
        تفعيل/إيقاف التحديث التلقائي
        """
        if enabled:
            self.auto_refresh_timer.start(30000)
        else:
            self.auto_refresh_timer.stop()
    
    def load_internet_subscriptions(self):
        """
        تحميل قائمة اشتراكات الإنترنت
        """
        try:
            subscriptions = self.internet_controller.get_all_subscriptions()
            self.all_subscriptions = subscriptions  # حفظ النسخة الأصلية للفلترة
            self.populate_table(subscriptions)
            self.update_statistics()
        except Exception as e:
            MessageHelper.show_error(self, "خطأ", f"حدث خطأ أثناء تحميل البيانات: {str(e)}")
    
    def populate_table(self, subscriptions: list):
        """
        ملء الجدول بالبيانات
        """
        self.table.setRowCount(len(subscriptions))
        
        for row, subscription in enumerate(subscriptions):
            # إخفاء المعرف في عمود مخفي
            id_item = QTableWidgetItem(str(subscription.id))
            id_item.setData(Qt.UserRole, subscription)
            self.table.setItem(row, 0, id_item)
            
            # اسم الزبون
            self.table.setItem(row, 1, QTableWidgetItem(subscription.person_name))
            
            # اسم الباقة
            self.table.setItem(row, 2, QTableWidgetItem(subscription.plan_name))

            # التكلفة الشهرية
            cost_item = QTableWidgetItem(NumberHelper.format_currency(subscription.monthly_fee))
            cost_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(row, 3, cost_item)
            
            # تاريخ البداية
            start_date_str = DateHelper.format_date(subscription.start_date) if subscription.start_date else "غير محدد"
            self.table.setItem(row, 4, QTableWidgetItem(start_date_str))
            
            # تاريخ النهاية
            end_date_str = DateHelper.format_date(subscription.end_date) if subscription.end_date else "غير محدد"
            self.table.setItem(row, 5, QTableWidgetItem(end_date_str))
            
            # الحالة
            status_text, status_color = self.get_status_display(subscription)
            status_item = QTableWidgetItem(status_text)
            status_item.setTextAlignment(Qt.AlignCenter)
            status_item.setBackground(status_color)
            status_item.setForeground(Qt.black)
            self.table.setItem(row, 6, status_item)
            
            # حالة الدفع
            payment_status_text = "مدفوع" if subscription.payment_status == 'paid' else "غير مدفوع"
            payment_status_color = Qt.green if subscription.payment_status == 'paid' else Qt.red
            payment_status_item = QTableWidgetItem(payment_status_text)
            payment_status_item.setTextAlignment(Qt.AlignCenter)
            payment_status_item.setBackground(payment_status_color)
            payment_status_item.setForeground(Qt.black)
            self.table.setItem(row, 7, payment_status_item)

            # الأيام المتبقية
            days_remaining = 0
            if subscription.end_date and isinstance(subscription.end_date, date):
                days_remaining = (subscription.end_date - date.today()).days
            
            days_item = QTableWidgetItem(str(days_remaining) if days_remaining >= 0 else "منتهي")
            days_item.setTextAlignment(Qt.AlignCenter)
            
            # تلوين الأيام المتبقية
            if days_remaining < 0:
                days_item.setBackground(Qt.red)
                days_item.setForeground(Qt.black)
            elif days_remaining <= 7:
                days_item.setBackground(Qt.yellow)
                days_item.setForeground(Qt.black)
            else:
                days_item.setBackground(Qt.green)
                days_item.setForeground(Qt.black)

            self.table.setItem(row, 8, days_item)
            
            # آخر تحديث
            last_updated = DateHelper.format_date(subscription.updated_at) if subscription.updated_at else "غير متوفر"
            self.table.setItem(row, 9, QTableWidgetItem(last_updated))
        
        # ضبط عرض الأعمدة
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # اسم الزبون
        header.setSectionResizeMode(2, QHeaderView.Stretch)  # اسم الباقة
    
    def get_status_display(self, subscription):
        """
        الحصول على نص ولون الحالة بناءً على التواريخ
        """
        today = date.today()
        start = subscription.start_date
        end = subscription.end_date

        if not isinstance(start, date) or not isinstance(end, date):
            return "غير محدد", Qt.gray

        if end < today:
            return "منتهي", Qt.red
        elif start <= today <= end:
            return "نشط", Qt.green
        else: # start > today
            return "لم يبدأ بعد", Qt.blue
    
    def filter_subscriptions(self):
        """
        فلترة الاشتراكات حسب البحث والحالة
        """
        if not hasattr(self, 'all_subscriptions'):
            return
        
        search_term = self.search_input.text().strip().lower()
        status_filter = self.status_filter.currentText()
        
        filtered_subscriptions = []
        today = date.today()

        for subscription in self.all_subscriptions:
            # فلترة النص
            plan_name = subscription.plan_name or ""
            person_name = subscription.person_name or ""
            if search_term:
                if not (search_term in plan_name.lower() or
                       search_term in person_name.lower() or
                       search_term in str(subscription.monthly_fee)):
                    continue
            
            # فلترة الحالة
            status_text, _ = self.get_status_display(subscription)

            if status_filter != "الكل":
                if status_filter == "نشط" and status_text != "نشط":
                    continue
                elif status_filter == "منتهي" and status_text != "منتهي":
                    continue
            
            filtered_subscriptions.append(subscription)
        
        self.populate_table(filtered_subscriptions)
    
    def update_statistics(self):
        """
        تحديث الإحصائيات
        """
        try:
            stats = self.internet_controller.get_subscription_statistics()
            
            self.total_subscriptions_label.setText(f"إجمالي الاشتراكات: {stats.get('total_subscriptions_count', 0)}")
            self.active_subscriptions_label.setText(f"نشط: {stats.get('active_subscriptions_count', 0)}")
            self.expired_subscriptions_label.setText(f"منتهي: {stats.get('expired_subscriptions_count', 0)}")
            self.paid_subscriptions_label.setText(f"مدفوع: {stats.get('paid_count', 0)}")
            self.unpaid_subscriptions_label.setText(f"غير مدفوع: {stats.get('unpaid_count', 0)}")
            self.total_revenue_label.setText(f"إجمالي الإيرادات: {NumberHelper.format_currency(stats.get('total_monthly_revenue', 0))}")
            
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
            id_item = self.table.item(current_row, 0)
            if id_item:
                self.selected_subscription = id_item.data(Qt.UserRole)
                # تفعيل زر الدفع فقط إذا كان الاشتراك غير مدفوع
                self.mark_paid_btn.setEnabled(self.selected_subscription.payment_status == 'unpaid')
            else:
                self.selected_subscription = None
                self.mark_paid_btn.setEnabled(False)
        else:
            self.selected_subscription = None
            self.mark_paid_btn.setEnabled(False)
    
    def mark_as_paid(self):
        """
        وضع علامة على الاشتراك كمدفوع
        """
        if not self.selected_subscription:
            return
        
        reply = MessageHelper.show_question(
            self, "تأكيد الدفع",
            f"هل أنت متأكد من أن هذا الاشتراك قد تم دفعه؟\n"
            f"الباقة: {self.selected_subscription.plan_name}\n"
            f"الزبون: {self.selected_subscription.person_name}"
        )
        
        if reply:
            success, message = self.internet_controller.update_subscription_payment_status(
                self.selected_subscription.id, 'paid'
            )
            
            if success:
                MessageHelper.show_info(self, "نجح", message)
                self.load_internet_subscriptions()
            else:
                MessageHelper.show_error(self, "خطأ", message)
    
    def add_internet_subscription(self):
        """
        إضافة اشتراك إنترنت جديد
        """
        persons = self.person_controller.get_all_persons()
        if not persons:
            MessageHelper.show_warning(self, "تنبيه", "يجب إضافة زبائن أولاً قبل إضافة اشتراكات الإنترنت")
            return
        
        dialog = AddInternetDialog(self)
        if dialog.exec_() == dialog.Accepted:
            internet_data = dialog.get_subscription_data()
            
            person_id = internet_data.get('person_id')
            if not person_id:
                MessageHelper.show_error(self, "خطأ", "لم يتم اختيار زبون.")
                return

            success, message, internet_id = self.internet_controller.add_subscription(
                person_id,
                internet_data['plan_name'],
                internet_data['monthly_fee'],
                internet_data['start_date'],
                internet_data['end_date'],
                internet_data['payment_status']
            )
            
            if success:
                MessageHelper.show_info(self, "نجح", message)
                self.load_internet_subscriptions()
            else:
                MessageHelper.show_error(self, "خطأ", message)
    
    def edit_internet_subscription(self):
        """
        تعديل اشتراك إنترنت
        """
        if not self.selected_subscription:
            return
        
        dialog = AddInternetDialog(self, self.selected_subscription)
        if dialog.exec_() == dialog.Accepted:
            internet_data = dialog.get_subscription_data()
            
            # is_active is now determined by dates, so it's not passed
            success, message = self.internet_controller.update_subscription(
                self.selected_subscription.id,
                internet_data['plan_name'],
                internet_data['monthly_fee'],
                internet_data['start_date'],
                internet_data['end_date'],
                internet_data['payment_status']
            )
            
            if success:
                MessageHelper.show_info(self, "نجح", message)
                self.load_internet_subscriptions()
            else:
                MessageHelper.show_error(self, "خطأ", message)
    
    def delete_internet_subscription(self):
        """
        حذف اشتراك إنترنت
        """
        if not self.selected_subscription:
            return
        
        reply = MessageHelper.show_question(
            self, "تأكيد الحذف",
            f"هل أنت متأكد من حذف هذا الاشتراك؟\n"
            f"الباقة: {self.selected_subscription.plan_name}\n"
            f"الزبون: {self.selected_subscription.person_name}\n"
            f"التكلفة: {NumberHelper.format_currency(self.selected_subscription.monthly_fee)}"
        )
        
        if reply:
            success, message = self.internet_controller.delete_subscription(self.selected_subscription.id)
            
            if success:
                MessageHelper.show_info(self, "نجح", message)
                self.load_internet_subscriptions()
            else:
                MessageHelper.show_error(self, "خطأ", message)
    
    def add_internet_subscription(self):
        """
        إضافة اشتراك إنترنت جديد
        """
        persons = self.person_controller.get_all_persons()
        if not persons:
            MessageHelper.show_warning(self, "تنبيه", "يجب إضافة زبائن أولاً قبل إضافة اشتراكات الإنترنت")
            return
        
        dialog = AddInternetDialog(self)
        if dialog.exec_() == dialog.Accepted:
            internet_data = dialog.get_subscription_data()
            
            person_id = internet_data.get('person_id')
            if not person_id:
                MessageHelper.show_error(self, "خطأ", "لم يتم اختيار زبون.")
                return

            success, message, internet_id = self.internet_controller.add_subscription(
                person_id,
                internet_data['plan_name'],
                internet_data['monthly_fee'],
                internet_data['start_date'],
                internet_data['end_date'],
                internet_data['payment_status']
            )
            
            if success:
                MessageHelper.show_info(self, "نجح", message)
                self.load_internet_subscriptions()
            else:
                MessageHelper.show_error(self, "خطأ", message)
    
    def edit_internet_subscription(self):
        """
        تعديل اشتراك إنترنت
        """
        if not self.selected_subscription:
            return
        
        dialog = AddInternetDialog(self, self.selected_subscription)
        if dialog.exec_() == dialog.Accepted:
            internet_data = dialog.get_subscription_data()
            
            # is_active is now determined by dates, so it's not passed
            success, message = self.internet_controller.update_subscription(
                self.selected_subscription.id,
                internet_data['plan_name'],
                internet_data['monthly_fee'],
                internet_data['start_date'],
                internet_data['end_date'],
                internet_data['payment_status']
            )
            
            if success:
                MessageHelper.show_info(self, "نجح", message)
                self.load_internet_subscriptions()
            else:
                MessageHelper.show_error(self, "خطأ", message)
    
    def delete_internet_subscription(self):
        """
        حذف اشتراك إنترنت
        """
        if not self.selected_subscription:
            return
        
        reply = MessageHelper.show_question(
            self, "تأكيد الحذف",
            f"هل أنت متأكد من حذف هذا الاشتراك؟\n"
            f"الباقة: {self.selected_subscription.plan_name}\n"
            f"الزبون: {self.selected_subscription.person_name}\n"
            f"التكلفة: {NumberHelper.format_currency(self.selected_subscription.monthly_fee)}"
        )
        
        if reply:
            success, message = self.internet_controller.delete_subscription(self.selected_subscription.id)
            
            if success:
                MessageHelper.show_info(self, "نجح", message)
                self.load_internet_subscriptions()
            else:
                MessageHelper.show_error(self, "خطأ", message)
