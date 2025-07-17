# -*- coding: utf-8 -*-
"""
نقطة تشغيل التطبيق الرئيسية
نظام إدارة المتجر - إدارة الزبائن والديون والأقساط واشتراكات الإنترنت
"""

import sys
import os
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# إضافة مسار المشروع إلى sys.path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from views.main_window import MainWindow
from database.database_connection import DatabaseConnection
from auth.controllers.auth_controller import AuthController
from auth.views.login_dialog import LoginDialog
from auth.views.first_time_setup_dialog import FirstTimeSetupDialog


def setup_application():
    """
    إعداد التطبيق
    """
    app = QApplication(sys.argv)
    
    # إعداد اللغة والاتجاه
    app.setLayoutDirection(Qt.RightToLeft)
    
    # إعداد الخط
    font = QFont("Arial", 10)
    app.setFont(font)
    
    # إعداد اسم التطبيق
    app.setApplicationName("نظام إدارة المتجر")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("Store Management")
    
    return app


def main():
    """
    الدالة الرئيسية لتشغيل التطبيق
    """
    try:
        # إنشاء التطبيق
        app = setup_application()
        
        # إنشاء اتصال قاعدة البيانات
        db_connection = DatabaseConnection()
        
        # إنشاء كنترولر التسجيل
        auth_controller = AuthController(db_connection)
        
        # التحقق من الإعداد الأولي
        if auth_controller.is_first_time_setup():
            # عرض شاشة الإعداد الأولي
            setup_dialog = FirstTimeSetupDialog(auth_controller)
            if setup_dialog.exec_() != setup_dialog.Accepted:
                # إذا ألغى المستخدم الإعداد، إنهاء التطبيق
                sys.exit(0)
        
        # عرض شاشة تسجيل الدخول
        login_dialog = LoginDialog(auth_controller)
        if login_dialog.exec_() != login_dialog.Accepted:
            # إذا ألغى المستخدم تسجيل الدخول، إنهاء التطبيق
            sys.exit(0)
        
        # إنشاء النافذة الرئيسية
        main_window = MainWindow()
        
        # إضافة قائمة إعدادات كلمة المرور إلى النافذة الرئيسية
        main_window.set_auth_controller(auth_controller)
        
        main_window.show()
        
        # تشغيل التطبيق
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"خطأ في تشغيل التطبيق: {str(e)}")
        QMessageBox.critical(None, "خطأ", f"خطأ في تشغيل التطبيق: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
