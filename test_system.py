# ملف اختبار النظام - System Test
# يقوم بفحص جميع مكونات النظام والتأكد من عملها

import sys
import os

def test_imports():
    """اختبار استيراد جميع الوحدات"""
    print("🔍 اختبار استيراد الوحدات...")
    
    try:
        # اختبار PyQt5
        from PyQt5.QtWidgets import QApplication
        print("✅ PyQt5 - تم الاستيراد بنجاح")
        
        # اختبار وحدة قاعدة البيانات
        from database import DatabaseManager
        print("✅ database.py - تم الاستيراد بنجاح")
        
        # اختبار النماذج
        from models import Person, Debt, Installment, InternetSubscription
        print("✅ models.py - تم الاستيراد بنجاح")
        
        # اختبار نوافذ الحوار
        from dialogs import PersonDialog, DebtDialog, InstallmentDialog, SubscriptionDialog
        print("✅ dialogs.py - تم الاستيراد بنجاح")
        
        # اختبار نافذة تفاصيل الزبون
        from person_details_window import PersonDetailsWindow
        print("✅ person_details_window.py - تم الاستيراد بنجاح")
        
        # اختبار الواجهات العامة
        from general_views import AllDebtsWindow, AllInstallmentsWindow, AllSubscriptionsWindow
        print("✅ general_views.py - تم الاستيراد بنجاح")
        
        # اختبار النافذة الرئيسية
        from main import MainWindow
        print("✅ main.py - تم الاستيراد بنجاح")
        
        return True
        
    except ImportError as e:
        print(f"❌ خطأ في الاستيراد: {e}")
        return False
    except Exception as e:
        print(f"❌ خطأ عام: {e}")
        return False

def test_database():
    """اختبار قاعدة البيانات"""
    print("\n🗄️ اختبار قاعدة البيانات...")
    
    try:
        from database import DatabaseManager
        from models import Person, Debt, Installment, InternetSubscription
        
        # إنشاء قاعدة بيانات تجريبية
        db = DatabaseManager("test_db.db")
        print("✅ تم إنشاء قاعدة البيانات")
        
        # اختبار النماذج
        person_model = Person(db)
        debt_model = Debt(db)
        installment_model = Installment(db)
        subscription_model = InternetSubscription(db)
        print("✅ تم إنشاء النماذج")
        
        # اختبار إضافة زبون
        person_id = person_model.add_person("زبون تجريبي", "0501234567", "عنوان تجريبي")
        if person_id:
            print("✅ تم إضافة زبون تجريبي")
        
        # اختبار جلب الزبائن
        persons = person_model.get_all_persons()
        if persons:
            print(f"✅ تم جلب {len(persons)} زبون")
        
        # حذف قاعدة البيانات التجريبية
        if os.path.exists("test_db.db"):
            os.remove("test_db.db")
            print("✅ تم حذف قاعدة البيانات التجريبية")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في قاعدة البيانات: {e}")
        return False

def test_file_structure():
    """اختبار هيكل الملفات"""
    print("\n📁 اختبار هيكل الملفات...")
    
    required_files = [
        "main.py",
        "database.py", 
        "models.py",
        "dialogs.py",
        "person_details_window.py",
        "general_views.py",
        "requirements.txt",
        "README.md"
    ]
    
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} - موجود")
        else:
            print(f"❌ {file} - غير موجود")
            missing_files.append(file)
    
    if not missing_files:
        print("✅ جميع الملفات المطلوبة موجودة")
        return True
    else:
        print(f"❌ ملفات مفقودة: {missing_files}")
        return False

def main():
    """تشغيل جميع الاختبارات"""
    print("🧪 بدء اختبار نظام إدارة المتجر")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 3
    
    # اختبار الاستيراد
    if test_imports():
        tests_passed += 1
    
    # اختبار هيكل الملفات
    if test_file_structure():
        tests_passed += 1
    
    # اختبار قاعدة البيانات
    if test_database():
        tests_passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 نتائج الاختبار: {tests_passed}/{total_tests}")
    
    if tests_passed == total_tests:
        print("🎉 جميع الاختبارات نجحت! النظام جاهز للاستخدام")
        print("\n🚀 لتشغيل النظام:")
        print("   python launcher.py")
        print("   أو")
        print("   python main.py")
    else:
        print("⚠️ بعض الاختبارات فشلت. يرجى مراجعة الأخطاء أعلاه")

if __name__ == "__main__":
    main()
