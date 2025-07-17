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
        
        subtitle_label = QLabel("عرض وإدارة جميع اشتراكات الإنترنت مع معلومات السرعة والباقات")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("""
            QLabel {
                color: #ddd;
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
        self.search_input.setPlaceholderText("ابحث في الوصف أو اسم الزبون أو السرعة...")
        self.search_input.setMaximumWidth(300)
        
        # فلتر الحالة
        status_label = QLabel("الحالة:")
        self.status_filter = QComboBox()
        self.status_filter.addItems(["الكل", "نشط", "منتهي الصلاحية", "معطل"])
        self.status_filter.setMaximumWidth(120)
        
        # فلتر السرعة
        speed_label = QLabel("السرعة:")
        self.speed_filter = QComboBox()
        self.speed_filter.addItems(["الكل", "1 ميجا", "2 ميجا", "5 ميجا", "10 ميجا", "20 ميجا"])
        self.speed_filter.setMaximumWidth(120)
        
        # خيار التحديث التلقائي
        self.auto_refresh_checkbox = QCheckBox("التحديث التلقائي (30 ثانية)")
        self.auto_refresh_checkbox.setChecked(True)
        
        # الأزرار
        self.add_btn = QPushButton("إضافة اشتراك")
        self.edit_btn = QPushButton("تعديل")
        self.delete_btn = QPushButton("حذف")
        self.activate_btn = QPushButton("تفعيل")
        self.deactivate_btn = QPushButton("إيقاف")
        self.refresh_btn = QPushButton("تحديث")
        
        # تنسيق الأزرار
        buttons = [self.add_btn, self.edit_btn, self.delete_btn, 
                  self.activate_btn, self.deactivate_btn, self.refresh_btn]
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
        self.activate_btn.setStyleSheet(self.activate_btn.styleSheet().replace("#6c5ce7", "#17a2b8").replace("#5a4fcf", "#138496"))
        self.deactivate_btn.setStyleSheet(self.deactivate_btn.styleSheet().replace("#6c5ce7", "#fd7e14").replace("#5a4fcf", "#e8630a"))
        
        # تعطيل الأزرار في البداية
        self.edit_btn.setEnabled(False)
        self.delete_btn.setEnabled(False)
        self.activate_btn.setEnabled(False)
        self.deactivate_btn.setEnabled(False)
        
        # ترتيب العناصر
        toolbar_layout.addWidget(search_label)
        toolbar_layout.addWidget(self.search_input)
        toolbar_layout.addWidget(status_label)
        toolbar_layout.addWidget(self.status_filter)
        toolbar_layout.addWidget(speed_label)
        toolbar_layout.addWidget(self.speed_filter)
        toolbar_layout.addWidget(self.auto_refresh_checkbox)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.add_btn)
        toolbar_layout.addWidget(self.edit_btn)
        toolbar_layout.addWidget(self.delete_btn)
        toolbar_layout.addWidget(self.activate_btn)
        toolbar_layout.addWidget(self.deactivate_btn)
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
                font-size: 16px;
                font-weight: bold;
                color: #495057;
                margin-bottom: 10px;
            }
        """)
        table_layout.addWidget(table_title)
        
        # الجدول
        self.table = QTableWidget()
        headers = ["المعرف", "اسم الزبون", "السرعة", "التكلفة الشهرية", "الوصف", 
                  "تاريخ البداية", "تاريخ النهاية", "الحالة", "الأيام المتبقية", "آخر تحديث"]
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
        self.expired_subscriptions_label = QLabel("منتهي الصلاحية: -")
        self.disabled_subscriptions_label = QLabel("معطل: -")
        self.total_revenue_label = QLabel("إجمالي الإيرادات: -")
        
        for label in [self.total_subscriptions_label, self.active_subscriptions_label, 
                     self.expired_subscriptions_label, self.disabled_subscriptions_label,
                     self.total_revenue_label]:
            label.setStyleSheet("""
                QLabel {
                    font-weight: bold;
                    color: #495057;
                }
            """)
        
        status_layout.addWidget(self.total_subscriptions_label)
        status_layout.addWidget(self.active_subscriptions_label)
        status_layout.addWidget(self.expired_subscriptions_label)
        status_layout.addWidget(self.disabled_subscriptions_label)
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
        self.activate_btn.clicked.connect(self.activate_subscription)
        self.deactivate_btn.clicked.connect(self.deactivate_subscription)
        self.refresh_btn.clicked.connect(self.load_internet_subscriptions)
        
        # أحداث الجدول
        self.table.selectionModel().selectionChanged.connect(self.on_selection_changed)
        self.table.doubleClicked.connect(self.edit_internet_subscription)
        
        # أحداث البحث والفلترة
        self.search_input.textChanged.connect(self.filter_subscriptions)
        self.status_filter.currentTextChanged.connect(self.filter_subscriptions)
        self.speed_filter.currentTextChanged.connect(self.filter_subscriptions)
        
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
            
            # السرعة
            speed_text = f"{subscription.speed} ميجا"
            speed_item = QTableWidgetItem(speed_text)
            speed_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 2, speed_item)
            
            # التكلفة الشهرية
            cost_item = QTableWidgetItem(NumberHelper.format_currency(subscription.monthly_fee))
            cost_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(row, 3, cost_item)
            
            # الوصف
            self.table.setItem(row, 4, QTableWidgetItem(subscription.description))
            
            # تاريخ البداية
            start_date = DateHelper.format_date(subscription.start_date) if subscription.start_date else "غير محدد"
            self.table.setItem(row, 5, QTableWidgetItem(start_date))
            
            # تاريخ النهاية
            end_date = DateHelper.format_date(subscription.end_date) if subscription.end_date else "غير محدد"
            self.table.setItem(row, 6, QTableWidgetItem(end_date))
            
            # الحالة
            status_text, status_color = self.get_status_display(subscription)
            status_item = QTableWidgetItem(status_text)
            status_item.setTextAlignment(Qt.AlignCenter)
            status_item.setBackground(status_color)
            status_item.setForeground(Qt.white)
            self.table.setItem(row, 7, status_item)
            
            # الأيام المتبقية
            days_remaining = subscription.days_remaining if hasattr(subscription, 'days_remaining') else 0
            days_item = QTableWidgetItem(str(days_remaining) if days_remaining > 0 else "انتهى")
            days_item.setTextAlignment(Qt.AlignCenter)
            
            # تلوين الأيام المتبقية
            if days_remaining <= 0:
                days_item.setBackground(Qt.red)
                days_item.setForeground(Qt.white)
            elif days_remaining <= 7:
                days_item.setBackground(Qt.yellow)
                days_item.setForeground(Qt.black)
            elif days_remaining <= 30:
                days_item.setBackground(Qt.blue)
                days_item.setForeground(Qt.white)
            else:
                days_item.setBackground(Qt.green)
                days_item.setForeground(Qt.white)
            
            self.table.setItem(row, 8, days_item)
            
            # آخر تحديث
            last_updated = DateHelper.format_date(subscription.updated_at) if subscription.updated_at else "غير متوفر"
            self.table.setItem(row, 9, QTableWidgetItem(last_updated))
        
        # ضبط عرض الأعمدة
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # اسم الزبون
        header.setSectionResizeMode(4, QHeaderView.Stretch)  # الوصف
    
    def get_status_display(self, subscription):
        """
        الحصول على نص ولون الحالة
        """
        if not subscription.is_active:
            return "معطل", Qt.gray
        elif hasattr(subscription, 'is_expired') and subscription.is_expired:
            return "منتهي الصلاحية", Qt.red
        else:
            return "نشط", Qt.green
    
    def filter_subscriptions(self):
        """
        فلترة الاشتراكات حسب البحث والحالة والسرعة
        """
        if not hasattr(self, 'all_subscriptions'):
            return
        
        search_term = self.search_input.text().strip().lower()
        status_filter = self.status_filter.currentText()
        speed_filter = self.speed_filter.currentText()
        
        filtered_subscriptions = []
        
        for subscription in self.all_subscriptions:
            # فلترة النص
            if search_term:
                if not (search_term in subscription.description.lower() or
                       search_term in subscription.person_name.lower() or
                       search_term in str(subscription.speed) or
                       search_term in str(subscription.monthly_fee)):
                    continue
            
            # فلترة الحالة
            if status_filter != "الكل":
                if status_filter == "نشط" and (not subscription.is_active or 
                    (hasattr(subscription, 'is_expired') and subscription.is_expired)):
                    continue
                elif status_filter == "منتهي الصلاحية" and (not hasattr(subscription, 'is_expired') or 
                    not subscription.is_expired):
                    continue
                elif status_filter == "معطل" and subscription.is_active:
                    continue
            
            # فلترة السرعة
            if speed_filter != "الكل":
                expected_speed = speed_filter.replace(" ميجا", "")
                if str(subscription.speed) != expected_speed:
                    continue
            
            filtered_subscriptions.append(subscription)
        
        self.populate_table(filtered_subscriptions)
    
    def update_statistics(self):
        """
        تحديث الإحصائيات
        """
        try:
            stats = self.internet_controller.get_subscription_statistics()
            
            self.total_subscriptions_label.setText(f"إجمالي الاشتراكات: {stats['total_subscriptions_count']}")
            self.active_subscriptions_label.setText(f"نشط: {stats['active_subscriptions_count']}")
            self.expired_subscriptions_label.setText(f"منتهي الصلاحية: {stats['expired_subscriptions_count']}")
            self.disabled_subscriptions_label.setText(f"معطل: {stats['disabled_subscriptions_count']}")
            self.total_revenue_label.setText(f"إجمالي الإيرادات: {NumberHelper.format_currency(stats['total_monthly_revenue'])}")
            
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
            # الحصول على الاشتراك المحدد
            id_item = self.table.item(current_row, 0)
            if id_item:
                self.selected_subscription = id_item.data(Qt.UserRole)
                # تفعيل/تعطيل أزرار التفعيل والإيقاف
                self.activate_btn.setEnabled(
                    self.selected_subscription and not self.selected_subscription.is_active
                )
                self.deactivate_btn.setEnabled(
                    self.selected_subscription and self.selected_subscription.is_active
                )
            else:
                self.selected_subscription = None
                self.activate_btn.setEnabled(False)
                self.deactivate_btn.setEnabled(False)
        else:
            self.selected_subscription = None
            self.activate_btn.setEnabled(False)
            self.deactivate_btn.setEnabled(False)
    
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
            internet_data = dialog.get_internet_data()
            
            # هنا نحتاج person_id - يمكن تحسين هذا لاحقاً
            if persons:
                person_id = persons[0].id  # مؤقت - يختار أول زبون
                
                success, message, internet_id = self.internet_controller.add_subscription(
                    person_id,
                    internet_data['plan_name'],
                    internet_data['monthly_fee'],
                    internet_data['speed'],
                    internet_data['start_date'],
                    internet_data['end_date']
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
            internet_data = dialog.get_internet_data()
            
            success, message = self.internet_controller.update_subscription(
                self.selected_subscription.id,
                internet_data['plan_name'],
                internet_data['monthly_fee'],
                internet_data['speed'],
                internet_data['start_date'],
                internet_data['end_date'],
                self.selected_subscription.is_active
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
            f"الوصف: {self.selected_subscription.description}\n"
            f"السرعة: {self.selected_subscription.speed} ميجا\n"
            f"التكلفة: {NumberHelper.format_currency(self.selected_subscription.monthly_fee)}"
        )
        
        if reply:
            success, message = self.internet_controller.delete_subscription(self.selected_subscription.id)
            
            if success:
                MessageHelper.show_info(self, "نجح", message)
                self.load_internet_subscriptions()
            else:
                MessageHelper.show_error(self, "خطأ", message)
    
    def activate_subscription(self):
        """
        تفعيل اشتراك الإنترنت
        """
        if not self.selected_subscription or self.selected_subscription.is_active:
            return
        
        success, message = self.internet_controller.activate_subscription(self.selected_subscription.id)
        
        if success:
            MessageHelper.show_info(self, "نجح", message)
            self.load_internet_subscriptions()
        else:
            MessageHelper.show_error(self, "خطأ", message)
    
    def deactivate_subscription(self):
        """
        إيقاف اشتراك الإنترنت
        """
        if not self.selected_subscription or not self.selected_subscription.is_active:
            return
        
        reply = MessageHelper.show_question(
            self, "تأكيد الإيقاف",
            f"هل أنت متأكد من إيقاف هذا الاشتراك؟\n"
            f"الوصف: {self.selected_subscription.description}\n"
            f"سيتم إيقاف الخدمة فوراً."
        )
        
        if reply:
            success, message = self.internet_controller.deactivate_subscription(self.selected_subscription.id)
            
            if success:
                MessageHelper.show_info(self, "نجح", message)
                self.load_internet_subscriptions()
            else:
                MessageHelper.show_error(self, "خطأ", message)
