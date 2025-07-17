# -*- coding: utf-8 -*-
"""
ملف اختبار بسيط لنظام التسجيل
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.database_connection import DatabaseConnection
from auth.controllers.auth_controller import AuthController

def main():
    print("=== اختبار نظام التسجيل ===")
    
    # إنشاء اتصال قاعدة البيانات
    db_connection = DatabaseConnection()
    
    # إنشاء كنترولر التسجيل
    auth_controller = AuthController(db_connection)
    
    # التحقق من الإعداد الأولي
    is_first_time = auth_controller.is_first_time_setup()
    print(f"هل هذه اول مرة؟ {is_first_time}")
    
    print("=== انتهى الاختبار ===")

if __name__ == "__main__":
    main()
