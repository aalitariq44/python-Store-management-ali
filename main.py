# -*- coding: utf-8 -*-
"""
نقطة تشغيل التطبيق الرئيسية
نظام إدارة المتجر - إدارة الزبائن والديون والأقساط واشتراكات الإنترنت
"""

import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# إضافة مسار المشروع إلى sys.path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from views.main_window import MainWindow


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
        
        # إنشاء النافذة الرئيسية
        main_window = MainWindow()
        main_window.show()
        
        # تشغيل التطبيق
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"خطأ في تشغيل التطبيق: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
