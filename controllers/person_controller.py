# -*- coding: utf-8 -*-
"""
منطق إدارة الزبائن
يحتوي على العمليات والقواعد الخاصة بالزبائن
"""

from typing import List, Optional
from database.database_connection import DatabaseConnection
from database.queries import PersonQueries
from database.models import Person


class PersonController:
    """
    كنترولر إدارة الزبائن
    """
    
    def __init__(self):
        self.db = DatabaseConnection()
        self.queries = PersonQueries(self.db)
    
    def add_person(self, name: str, phone: str, address: str, notes: str) -> tuple[bool, str, Optional[int]]:
        """
        إضافة زبون جديد
        
        Args:
            name: اسم الزبون
            phone: رقم الهاتف
            address: العنوان
            notes: ملاحظات
            
        Returns:
            tuple: (نجح, رسالة, معرف الزبون الجديد)
        """
        # التحقق من صحة البيانات
        from utils.validators import PersonValidator
        validator = PersonValidator()
        is_valid, error_message = validator.validate_person_data(name, phone, address, notes)
        if not is_valid:
            return False, error_message, None
        
        # التحقق من عدم تكرار رقم الهاتف
        if self.is_phone_exists(phone):
            return False, "رقم الهاتف مُستخدم مسبقاً", None
        
        # إنشاء الزبون
        person = Person(name=name.strip(), phone=phone.strip(), address=address.strip(), notes=notes.strip())
        person_id = self.queries.create_person(person)
        
        if person_id:
            return True, "تم إضافة الزبون بنجاح", person_id
        else:
            return False, "حدث خطأ أثناء إضافة الزبون", None
    
    def update_person(self, person_id: int, name: str, phone: str, address: str, notes: str) -> tuple[bool, str]:
        """
        تحديث بيانات زبون
        
        Args:
            person_id: معرف الزبون
            name: الاسم الجديد
            phone: رقم الهاتف الجديد
            address: العنوان الجديد
            notes: الملاحظات الجديدة
            
        Returns:
            tuple: (نجح, رسالة)
        """
        # التحقق من وجود الزبون
        existing_person = self.queries.get_person_by_id(person_id)
        if not existing_person:
            return False, "الزبون غير موجود"
        
        # التحقق من صحة البيانات
        from utils.validators import PersonValidator
        validator = PersonValidator()
        is_valid, error_message = validator.validate_person_data(name, phone, address, notes)
        if not is_valid:
            return False, error_message
        
        # التحقق من عدم تكرار رقم الهاتف (إذا تم تغييره)
        if phone.strip() != existing_person.phone and self.is_phone_exists(phone):
            return False, "رقم الهاتف مُستخدم مسبقاً"
        
        # تحديث البيانات
        updated_person = Person(
            id=person_id,
            name=name.strip(),
            phone=phone.strip(),
            address=address.strip(),
            notes=notes.strip()
        )
        
        if self.queries.update_person(updated_person):
            return True, "تم تحديث بيانات الزبون بنجاح"
        else:
            return False, "حدث خطأ أثناء تحديث البيانات"
    
    def delete_person(self, person_id: int) -> tuple[bool, str]:
        """
        حذف زبون
        
        Args:
            person_id: معرف الزبون
            
        Returns:
            tuple: (نجح, رسالة)
        """
        # التحقق من وجود الزبون
        existing_person = self.queries.get_person_by_id(person_id)
        if not existing_person:
            return False, "الزبون غير موجود"
        
        # حذف الزبون (سيتم حذف البيانات المرتبطة تلقائياً بسبب CASCADE)
        if self.queries.delete_person(person_id):
            return True, "تم حذف الزبون بنجاح"
        else:
            return False, "حدث خطأ أثناء حذف الزبون"
    
    def get_all_persons(self) -> List[Person]:
        """
        الحصول على جميع الزبائن
        
        Returns:
            قائمة بجميع الزبائن
        """
        return self.queries.get_all_persons()
    
    def get_person_by_id(self, person_id: int) -> Optional[Person]:
        """
        الحصول على زبون بالمعرف
        
        Args:
            person_id: معرف الزبون
            
        Returns:
            الزبون أو None
        """
        return self.queries.get_person_by_id(person_id)
    
    def search_persons(self, search_term: str) -> List[Person]:
        """
        البحث في الزبائن
        
        Args:
            search_term: نص البحث
            
        Returns:
            قائمة بالزبائن المطابقين للبحث
        """
        if not search_term.strip():
            return self.get_all_persons()
        
        return self.queries.search_persons(search_term.strip())
    
    def is_phone_exists(self, phone: str, exclude_id: int = None) -> bool:
        """
        التحقق من وجود رقم الهاتف
        
        Args:
            phone: رقم الهاتف
            exclude_id: معرف الزبون المُستثنى من البحث (للتحديث)
            
        Returns:
            True إذا كان الرقم موجود
        """
        all_persons = self.get_all_persons()
        for person in all_persons:
            if person.phone == phone.strip() and person.id != exclude_id:
                return True
        return False
    
    def get_person_statistics(self, person_id: int) -> dict:
        """
        الحصول على إحصائيات الزبون
        
        Args:
            person_id: معرف الزبون
            
        Returns:
            قاموس بالإحصائيات
        """
        from .debt_controller import DebtController
        from .installment_controller import InstallmentController
        from .internet_controller import InternetController
        
        debt_controller = DebtController()
        installment_controller = InstallmentController()
        internet_controller = InternetController()
        
        debts = debt_controller.get_debts_by_person(person_id)
        installments = installment_controller.get_installments_by_person(person_id)
        subscriptions = internet_controller.get_subscriptions_by_person(person_id)
        
        # حساب الإحصائيات
        total_debts = sum(debt.amount for debt in debts if not debt.is_paid)
        paid_debts = sum(debt.amount for debt in debts if debt.is_paid)
        
        total_installments_amount = sum(inst.total_amount for inst in installments)
        paid_installments_amount = sum(inst.paid_amount for inst in installments)
        
        active_subscriptions = [sub for sub in subscriptions if sub.is_active]
        monthly_internet_fees = sum(sub.monthly_fee for sub in active_subscriptions)
        
        return {
            'debts_count': len(debts),
            'total_debts': total_debts,
            'paid_debts': paid_debts,
            'installments_count': len(installments),
            'total_installments_amount': total_installments_amount,
            'paid_installments_amount': paid_installments_amount,
            'subscriptions_count': len(subscriptions),
            'active_subscriptions_count': len(active_subscriptions),
            'monthly_internet_fees': monthly_internet_fees
        }
