# -*- coding: utf-8 -*-
"""
النافذة الرئيسية للتطبيق
تحتوي على القوائم الرئيسية والتنقل بين الأقسام
"""

import sys
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QFrame, QApplication, QMenuBar, QMenu, QAction)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap, QIcon
from utils.helpers import AppHelper, MessageHelper


class MainWindow(QMainWindow):
    """
    النافذة الرئيسية للتطبيق
    """
    
    def __init__(self):
        super().__init__()
        self.auth_controller = None
        self.init_ui()
        self.setup_menu()
    
    def set_auth_controller(self, auth_controller):
        """
        تعيين كنترولر التسجيل
        
        Args:
            auth_controller: كنترولر التسجيل
        """
        self.auth_controller = auth_controller
    
    def init_ui(self):
        """
        تهيئة واجهة المستخدم
        """
        self.setWindowTitle("نظام إدارة محل كاظم السعدي")
        self.setMinimumSize(1000, 700)
        
        # توسيط النافذة
        AppHelper.center_window(self, 1200, 800)
        
        # إنشاء القطعة المركزية
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # التخطيط الرئيسي
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # إضافة العنوان
        self.add_title(main_layout)
        
        # إضافة الأزرار الرئيسية
        self.add_main_buttons(main_layout)
        
        # إضافة معلومات الحالة
        self.add_status_info(main_layout)
    
    def setup_menu(self):
        """
        إعداد شريط القوائم
        """
        menubar = self.menuBar()
        
        # قائمة الملف
        file_menu = menubar.addMenu('ملف')
        
        exit_action = QAction('خروج', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # قائمة العرض
        view_menu = menubar.addMenu('عرض')
        
        persons_action = QAction('إدارة الزبائن', self)
        persons_action.triggered.connect(self.open_persons_view)
        view_menu.addAction(persons_action)
        
        debts_action = QAction('عرض الديون', self)
        debts_action.triggered.connect(self.open_debts_view)
        view_menu.addAction(debts_action)
        
        installments_action = QAction('عرض الأقساط', self)
        installments_action.triggered.connect(self.open_installments_view)
        view_menu.addAction(installments_action)
        
        internet_action = QAction('عرض اشتراكات الإنترنت', self)
        internet_action.triggered.connect(self.open_internet_view)
        view_menu.addAction(internet_action)
        
        # قائمة الإعدادات
        settings_menu = menubar.addMenu('إعدادات')
        
        password_settings_action = QAction('إعدادات كلمة المرور', self)
        password_settings_action.triggered.connect(self.open_password_settings)
        settings_menu.addAction(password_settings_action)
        
        # قائمة المساعدة
        help_menu = menubar.addMenu('مساعدة')
        
        about_action = QAction('حول البرنامج', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def add_title(self, layout: QVBoxLayout):
        """
        إضافة عنوان التطبيق
        
        Args:
            layout: التخطيط
        """
        title_frame = QFrame()
        title_frame.setStyleSheet("""
            QFrame {
                background-color: #2c3e50;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        
        title_layout = QVBoxLayout(title_frame)
        
        # العنوان الرئيسي
        title_label = QLabel("نظام إدارة محل كاظم السعدي")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 28px;
                font-weight: bold;
                background: transparent;
            }
        """)
        title_layout.addWidget(title_label)
        
        # العنوان الفرعي
        subtitle_label = QLabel("إدارة شاملة للزبائن والديون والأقساط واشتراكات الإنترنت")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("""
            QLabel {
                color: #ecf0f1;
                font-size: 14px;
                background: transparent;
                margin-top: 10px;
            }
        """)
        title_layout.addWidget(subtitle_label)
        
        layout.addWidget(title_frame)
    
    def add_main_buttons(self, layout: QVBoxLayout):
        """
        إضافة الأزرار الرئيسية
        
        Args:
            layout: التخطيط
        """
        buttons_frame = QFrame()
        buttons_layout = QVBoxLayout(buttons_frame)
        
        # الصف الأول من الأزرار
        row1_layout = QHBoxLayout()
        row1_layout.setSpacing(20)
        
        # زر إدارة الزبائن
        persons_btn = self.create_main_button(
            "إدارة الزبائن",
            "إضافة وتعديل وحذف الزبائن",
            "#3498db",
            self.open_persons_view
        )
        row1_layout.addWidget(persons_btn)
        
        # زر عرض الديون
        debts_btn = self.create_main_button(
            "عرض الديون",
            "إدارة جميع الديون في النظام",
            "#e74c3c",
            self.open_debts_view
        )
        row1_layout.addWidget(debts_btn)
        
        buttons_layout.addLayout(row1_layout)
        
        # الصف الثاني من الأزرار
        row2_layout = QHBoxLayout()
        row2_layout.setSpacing(20)
        
        # زر عرض الأقساط
        installments_btn = self.create_main_button(
            "عرض الأقساط",
            "إدارة جميع الأقساط في النظام",
            "#f39c12",
            self.open_installments_view
        )
        row2_layout.addWidget(installments_btn)
        
        # زر عرض اشتراكات الإنترنت
        internet_btn = self.create_main_button(
            "اشتراكات الإنترنت",
            "إدارة جميع اشتراكات الإنترنت",
            "#27ae60",
            self.open_internet_view
        )
        row2_layout.addWidget(internet_btn)
        
        buttons_layout.addLayout(row2_layout)
        
        layout.addWidget(buttons_frame)
    
    def create_main_button(self, title: str, description: str, color: str, callback) -> QPushButton:
        """
        إنشاء زر رئيسي
        
        Args:
            title: عنوان الزر
            description: وصف الزر
            color: لون الزر
            callback: الدالة المُستدعاة عند الضغط
            
        Returns:
            QPushButton: الزر المُنشأ
        """
        btn = QPushButton()
        btn.setMinimumHeight(120)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
                text-align: center;
                padding: 20px;
            }}
            QPushButton:hover {{
                background-color: {self.darken_color(color)};
            }}
            QPushButton:pressed {{
                background-color: {self.darken_color(color, 0.3)};
            }}
        """)
        
        # تنسيق النص
        btn.setText(f"{title}\n{description}")
        btn.clicked.connect(callback)
        
        return btn
    
    def darken_color(self, color: str, factor: float = 0.2) -> str:
        """
        جعل اللون أغمق
        
        Args:
            color: اللون الأصلي
            factor: معامل التغميق
            
        Returns:
            اللون المُغمق
        """
        # تحويل مبسط للألوان (يمكن تحسينه)
        color_map = {
            "#3498db": "#2980b9",
            "#e74c3c": "#c0392b", 
            "#f39c12": "#e67e22",
            "#27ae60": "#229954"
        }
        return color_map.get(color, color)
    
    def add_status_info(self, layout: QVBoxLayout):
        """
        إضافة معلومات الحالة
        
        Args:
            layout: التخطيط
        """
        status_frame = QFrame()
        status_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        
        status_layout = QVBoxLayout(status_frame)
        
        status_label = QLabel("معلومات النظام")
        status_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #495057;
                margin-bottom: 10px;
            }
        """)
        status_layout.addWidget(status_label)
        
        # يمكن إضافة إحصائيات سريعة هنا لاحقاً
        info_label = QLabel("مرحباً بك في نظام إدارة محل كاظم السعدي. اختر أحد الخيارات أعلاه للبدء.")
        info_label.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-size: 12px;
            }
        """)
        status_layout.addWidget(info_label)
        
        layout.addWidget(status_frame)
    
    def open_persons_view(self):
        """
        فتح واجهة إدارة الزبائن
        """
        try:
            from views.persons_view import PersonsView
            self.persons_window = PersonsView()
            self.persons_window.show()
        except Exception as e:
            MessageHelper.show_error(self, "خطأ", f"حدث خطأ في فتح واجهة الزبائن: {str(e)}")
    
    def open_debts_view(self):
        """
        فتح واجهة عرض الديون
        """
        try:
            from views.debts_view import DebtsView
            self.debts_window = DebtsView()
            self.debts_window.show()
        except Exception as e:
            MessageHelper.show_error(self, "خطأ", f"حدث خطأ في فتح واجهة الديون: {str(e)}")
    
    def open_installments_view(self):
        """
        فتح واجهة عرض الأقساط
        """
        try:
            from views.installments_view import InstallmentsView
            self.installments_window = InstallmentsView()
            self.installments_window.show()
        except Exception as e:
            MessageHelper.show_error(self, "خطأ", f"حدث خطأ في فتح واجهة الأقساط: {str(e)}")
    
    def open_internet_view(self):
        """
        فتح واجهة عرض اشتراكات الإنترنت
        """
        try:
            from views.internet_view import InternetView
            self.internet_window = InternetView()
            self.internet_window.show()
        except Exception as e:
            MessageHelper.show_error(self, "خطأ", f"حدث خطأ في فتح واجهة الإنترنت: {str(e)}")
    
    def show_about(self):
        """
        عرض معلومات حول البرنامج
        """
        about_text = """
        نظام إدارة محل كاظم السعدي
        الإصدار 1.0
        
        نظام شامل لإدارة:
        • الزبائن
        • الديون
        • الأقساط
        • اشتراكات الإنترنت
        
        تم تطويره باستخدام Python و PyQt5
        """
        MessageHelper.show_info(self, "حول البرنامج", about_text)
    
    def open_password_settings(self):
        """
        فتح نافذة إعدادات كلمة المرور
        """
        if not self.auth_controller:
            MessageHelper.show_error(self, "خطأ", "لم يتم تهيئة نظام التسجيل")
            return
        
        try:
            from auth.views.password_settings_dialog import PasswordSettingsDialog
            dialog = PasswordSettingsDialog(self.auth_controller, self)
            dialog.exec_()
        except Exception as e:
            MessageHelper.show_error(self, "خطأ", f"خطأ في فتح إعدادات كلمة المرور: {str(e)}")
    
    def closeEvent(self, event):
        """
        معالجة حدث إغلاق النافذة
        
        Args:
            event: حدث الإغلاق
        """
        reply = MessageHelper.show_question(
            self, "تأكيد الخروج", "هل تريد إغلاق التطبيق؟"
        )
        
        if reply:
            event.accept()
        else:
            event.ignore()


def main():
    """
    الدالة الرئيسية لتشغيل التطبيق
    """
    app = QApplication(sys.argv)
    app.setLayoutDirection(Qt.RightToLeft)  # دعم اللغة العربية
    
    # تعيين الخط
    font = QFont("Arial", 10)
    app.setFont(font)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
