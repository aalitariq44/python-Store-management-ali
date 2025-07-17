# -*- coding: utf-8 -*-
"""
ملف اختبار نظام التسجيل
"""

import sys
from PyQt5.QtWidgets import QApplication
from database.database_connection import DatabaseConnection
from auth.controllers.auth_controller import AuthController

def test_auth_system():
    """
    اختبار نظام التسجيل
    """
    # إنشاء اتصال قاعدة البيانات
    db_connection = DatabaseConnection()
    
    # إنشاء كنترولر التسجيل
    auth_controller = AuthController(db_connection)
    
    # التحقق من الإعداد الأولي
    is_first_time = auth_controller.is_first_time_setup()
    print(f"هل هذه أول مرة؟ {is_first_time}")
    
    if is_first_time:
        print("إعداد كلمة المرور لأول مرة...")
        # محاولة إعداد كلمة المرور
        success, message = auth_controller.setup_first_password("123456", "123456")
        print(f"نتيجة الإعداد: {success} - {message}")
    
    # اختبار التحقق من كلمة المرور
    print("اختبار التحقق من كلمة المرور...")
    success, message = auth_controller.verify_password("123456")
    print(f"نتيجة التحقق: {success} - {message}")
    
    # اختبار تغيير كلمة المرور
    print("اختبار تغيير كلمة المرور...")
    success, message = auth_controller.change_password("123456", "789012", "789012")
    print(f"نتيجة التغيير: {success} - {message}")
    
    # اختبار التحقق من كلمة المرور الجديدة
    print("اختبار التحقق من كلمة المرور الجديدة...")
    success, message = auth_controller.verify_password("789012")
    print(f"نتيجة التحقق: {success} - {message}")

if __name__ == "__main__":
    test_auth_system()
