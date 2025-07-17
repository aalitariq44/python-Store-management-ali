#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ملف تشغيل نظام إدارة المتجر
Store Management System Launcher
"""

import sys
import os

# إضافة مسار المشروع للبحث عن الوحدات
project_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_path)

try:
    # تجربة استيراد PyQt5
    from PyQt5.QtWidgets import QApplication, QMessageBox
    from PyQt5.QtCore import Qt
    
    print("✅ تم تحميل PyQt5 بنجاح")
    
    # استيراد المكونات الرئيسية
    from main import MainWindow
    
    def run_application():
        """تشغيل التطبيق الرئيسي"""
        print("🚀 جاري تشغيل نظام إدارة المتجر...")
        
        app = QApplication(sys.argv)
        
        # تطبيق الاتجاه العربي
        app.setLayoutDirection(Qt.RightToLeft)
        
        # إنشاء النافذة الرئيسية
        window = MainWindow()
        window.show()
        
        print("✅ تم تشغيل التطبيق بنجاح")
        print("📝 يمكنك الآن استخدام النظام")
        
        # تشغيل حلقة الأحداث
        sys.exit(app.exec_())
    
    if __name__ == "__main__":
        run_application()
        
except ImportError as e:
    print(f"❌ خطأ في استيراد PyQt5: {e}")
    print("📦 يرجى تثبيت PyQt5 أولاً:")
    print("   pip install PyQt5==5.15.9")
    
except Exception as e:
    print(f"❌ خطأ في تشغيل التطبيق: {e}")
    print("🔧 تأكد من سلامة ملفات المشروع")
