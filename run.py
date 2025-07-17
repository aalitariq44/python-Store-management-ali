#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ملف تشغيل مبسط للتحقق من النظام
"""

import sys
import os

def check_requirements():
    """
    التحقق من المتطلبات الأساسية
    """
    print("🔍 فحص المتطلبات...")
    
    # التحقق من Python
    if sys.version_info < (3, 7):
        print("❌ خطأ: يتطلب Python 3.7 أو أحدث")
        return False
    print(f"✅ Python {sys.version.split()[0]}")
    
    # التحقق من PyQt5
    try:
        from PyQt5 import QtCore
        print(f"✅ PyQt5 {QtCore.PYQT_VERSION_STR}")
    except ImportError:
        print("❌ خطأ: PyQt5 غير مثبت")
        print("💡 قم بتثبيته باستخدام: pip install PyQt5")
        return False
    
    # التحقق من الملفات المطلوبة
    required_dirs = ['database', 'controllers', 'views', 'utils']
    for dir_name in required_dirs:
        if not os.path.exists(dir_name):
            print(f"❌ خطأ: مجلد {dir_name} غير موجود")
            return False
        print(f"✅ مجلد {dir_name}")
    
    return True

def main():
    """
    الدالة الرئيسية
    """
    print("🚀 نظام إدارة المتجر - فحص أولي")
    print("=" * 40)
    
    if not check_requirements():
        print("\n❌ فشل في التحقق من المتطلبات")
        input("اضغط Enter للخروج...")
        return
    
    print("\n✅ جميع المتطلبات متوفرة!")
    print("🎯 بدء تشغيل التطبيق...")
    
    try:
        # استيراد وتشغيل التطبيق
        from main import main as run_app
        run_app()
    except Exception as e:
        print(f"\n❌ خطأ في تشغيل التطبيق: {str(e)}")
        print("\n🔧 تفاصيل الخطأ:")
        import traceback
        traceback.print_exc()
        input("\nاضغط Enter للخروج...")

if __name__ == "__main__":
    main()
