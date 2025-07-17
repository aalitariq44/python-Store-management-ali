# ملف إضافة بيانات تجريبية - Sample Data
# يمكن تشغيل هذا الملف لإضافة بيانات تجريبية للتطبيق

from database import DatabaseManager
from models import Person, Debt, Installment, InternetSubscription
from datetime import datetime, timedelta

def add_sample_data():
    """إضافة بيانات تجريبية للتطبيق"""
    
    # إنشاء مدير قاعدة البيانات والنماذج
    db_manager = DatabaseManager()
    person_model = Person(db_manager)
    debt_model = Debt(db_manager)
    installment_model = Installment(db_manager)
    subscription_model = InternetSubscription(db_manager)
    
    print("جاري إضافة البيانات التجريبية...")
    
    # إضافة زبائن تجريبيين
    persons_data = [
        ("أحمد محمد", "0501234567", "الرياض - حي النخيل"),
        ("فاطمة علي", "0559876543", "جدة - حي الزهراء"),
        ("خالد عبدالله", "0501122334", "الدمام - الكورنيش"),
        ("نورا سعد", "0555667788", "مكة - العزيزية"),
        ("عبدالرحمن أحمد", "0504455667", "المدينة - طيبة")
    ]
    
    person_ids = []
    for name, phone, address in persons_data:
        person_id = person_model.add_person(name, phone, address)
        person_ids.append(person_id)
        print(f"تم إضافة الزبون: {name}")
    
    # إضافة ديون تجريبية
    debts_data = [
        (person_ids[0], 1500.00, "قطع غيار سيارة"),
        (person_ids[1], 800.50, "أجهزة منزلية"),
        (person_ids[2], 2200.00, "مواد بناء"),
        (person_ids[0], 950.75, "أدوات كهربائية"),
        (person_ids[3], 1200.00, "أثاث منزلي")
    ]
    
    for person_id, amount, description in debts_data:
        debt_model.add_debt(person_id, amount, description)
        print(f"تم إضافة دين بمبلغ {amount} ريال")
    
    # إضافة أقساط تجريبية
    today = datetime.now().date()
    installments_data = [
        (person_ids[1], 5000.00, 500.00, today + timedelta(days=30), "تقسيط جهاز تلفزيون"),
        (person_ids[2], 8000.00, 800.00, today + timedelta(days=15), "تقسيط أجهزة مطبخ"),
        (person_ids[3], 3000.00, 300.00, today + timedelta(days=45), "تقسيط هاتف ذكي"),
        (person_ids[4], 12000.00, 1000.00, today + timedelta(days=60), "تقسيط لابتوب")
    ]
    
    for person_id, total_amount, installment_amount, due_date, description in installments_data:
        installment_model.add_installment(person_id, total_amount, installment_amount, due_date.strftime("%Y-%m-%d"), description)
        print(f"تم إضافة قسط بمبلغ إجمالي {total_amount} ريال")
    
    # إضافة اشتراكات إنترنت تجريبية
    subscriptions_data = [
        (person_ids[0], "خطة الألياف الذهبية", 299.00, today.strftime("%Y-%m-%d"), (today + timedelta(days=365)).strftime("%Y-%m-%d"), "اشتراك سنوي"),
        (person_ids[1], "خطة الألياف الفضية", 199.00, today.strftime("%Y-%m-%d"), (today + timedelta(days=180)).strftime("%Y-%m-%d"), "اشتراك نصف سنوي"),
        (person_ids[2], "خطة DSL العادية", 99.00, today.strftime("%Y-%m-%d"), (today + timedelta(days=90)).strftime("%Y-%m-%d"), "اشتراك ربع سنوي"),
        (person_ids[4], "خطة الألياف البلاتينية", 399.00, today.strftime("%Y-%m-%d"), (today + timedelta(days=365)).strftime("%Y-%m-%d"), "أسرع خطة متاحة")
    ]
    
    for person_id, plan_name, monthly_cost, start_date, end_date, description in subscriptions_data:
        subscription_model.add_subscription(person_id, plan_name, monthly_cost, start_date, end_date, description)
        print(f"تم إضافة اشتراك إنترنت: {plan_name}")
    
    print("\n✅ تم إضافة جميع البيانات التجريبية بنجاح!")
    print("📊 ملخص البيانات المضافة:")
    print(f"   👥 الزبائن: {len(persons_data)}")
    print(f"   💰 الديون: {len(debts_data)}")
    print(f"   📋 الأقساط: {len(installments_data)}")
    print(f"   🌐 اشتراكات الإنترنت: {len(subscriptions_data)}")

if __name__ == "__main__":
    add_sample_data()
