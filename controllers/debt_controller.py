# -*- coding: utf-8 -*-
"""
منطق إدارة الديون
يحتوي على العمليات والقواعد الخاصة بالديون
"""

from typing import List, Optional
from datetime import date
from database.database_connection import DatabaseConnection
from database.queries import DebtQueries
from database.models import Debt


class DebtController:
    """
    كنترولر إدارة الديون
    """
    
    def __init__(self):
        self.db = DatabaseConnection()
        self.queries = DebtQueries(self.db)
    
    def add_debt(self, person_id: int, amount: float, description: str, 
                 due_date: Optional[date] = None) -> tuple[bool, str, Optional[int]]:
        """
        إضافة دين جديد
        
        Args:
            person_id: معرف الزبون
            amount: مبلغ الدين
            description: وصف الدين
            due_date: تاريخ الاستحقاق
            
        Returns:
            tuple: (نجح, رسالة, معرف الدين الجديد)
        """
        # التحقق من صحة البيانات
        from utils.validators import DebtValidator
        validator = DebtValidator()
        is_valid, error_message = validator.validate_debt_data(
            person_id, amount, description, due_date
        )
        if not is_valid:
            return False, error_message, None
        
        # إنشاء الدين
        debt = Debt(
            person_id=person_id,
            amount=amount,
            description=description.strip(),
            due_date=due_date,
            is_paid=False
        )
        
        debt_id = self.queries.create_debt(debt)
        
        if debt_id:
            return True, "تم إضافة الدين بنجاح", debt_id
        else:
            return False, "حدث خطأ أثناء إضافة الدين", None
    
    def update_debt(self, debt_id: int, amount: float, description: str, 
                    due_date: Optional[date], is_paid: bool) -> tuple[bool, str]:
        """
        تحديث دين
        
        Args:
            debt_id: معرف الدين
            amount: المبلغ الجديد
            description: الوصف الجديد
            due_date: تاريخ الاستحقاق الجديد
            is_paid: حالة الدفع
            
        Returns:
            tuple: (نجح, رسالة)
        """
        # التحقق من وجود الدين
        existing_debt = self.get_debt_by_id(debt_id)
        if not existing_debt:
            return False, "الدين غير موجود"
        
        # التحقق من صحة البيانات
        from utils.validators import DebtValidator
        validator = DebtValidator()
        is_valid, error_message = validator.validate_debt_data(
            existing_debt.person_id, amount, description, due_date
        )
        if not is_valid:
            return False, error_message
        
        # تحديث البيانات
        updated_debt = Debt(
            id=debt_id,
            person_id=existing_debt.person_id,
            amount=amount,
            description=description.strip(),
            due_date=due_date,
            is_paid=is_paid
        )
        
        if self.queries.update_debt(updated_debt):
            return True, "تم تحديث الدين بنجاح"
        else:
            return False, "حدث خطأ أثناء تحديث الدين"
    
    def delete_debt(self, debt_id: int) -> tuple[bool, str]:
        """
        حذف دين
        
        Args:
            debt_id: معرف الدين
            
        Returns:
            tuple: (نجح, رسالة)
        """
        # التحقق من وجود الدين
        existing_debt = self.get_debt_by_id(debt_id)
        if not existing_debt:
            return False, "الدين غير موجود"
        
        if self.queries.delete_debt(debt_id):
            return True, "تم حذف الدين بنجاح"
        else:
            return False, "حدث خطأ أثناء حذف الدين"
    
    def mark_debt_as_paid(self, debt_id: int) -> tuple[bool, str]:
        """
        وضع علامة مدفوع على الدين
        
        Args:
            debt_id: معرف الدين
            
        Returns:
            tuple: (نجح, رسالة)
        """
        existing_debt = self.get_debt_by_id(debt_id)
        if not existing_debt:
            return False, "الدين غير موجود"
        
        if existing_debt.is_paid:
            return False, "الدين مدفوع مسبقاً"
        
        return self.update_debt(
            debt_id, existing_debt.amount, existing_debt.description,
            existing_debt.due_date, True
        )
    
    def get_all_debts(self) -> List[Debt]:
        """
        الحصول على جميع الديون
        
        Returns:
            قائمة بجميع الديون
        """
        return self.queries.get_all_debts()
    
    def get_debts_by_person(self, person_id: int) -> List[Debt]:
        """
        الحصول على ديون زبون معين
        
        Args:
            person_id: معرف الزبون
            
        Returns:
            قائمة بديون الزبون
        """
        return self.queries.get_debts_by_person(person_id)
    
    def get_debt_by_id(self, debt_id: int) -> Optional[Debt]:
        """
        الحصول على دين بالمعرف
        
        Args:
            debt_id: معرف الدين
            
        Returns:
            الدين أو None
        """
        all_debts = self.get_all_debts()
        for debt in all_debts:
            if debt.id == debt_id:
                return debt
        return None
    
    def get_unpaid_debts(self) -> List[Debt]:
        """
        الحصول على الديون غير المدفوعة
        
        Returns:
            قائمة بالديون غير المدفوعة
        """
        all_debts = self.get_all_debts()
        return [debt for debt in all_debts if not debt.is_paid]
    
    def get_overdue_debts(self) -> List[Debt]:
        """
        الحصول على الديون المتأخرة
        
        Returns:
            قائمة بالديون المتأخرة
        """
        today = date.today()
        unpaid_debts = self.get_unpaid_debts()
        
        return [debt for debt in unpaid_debts 
                if debt.due_date and debt.due_date < today]
    
    def search_debts(self, search_term: str) -> List[Debt]:
        """
        البحث في الديون
        
        Args:
            search_term: نص البحث
            
        Returns:
            قائمة بالديون المطابقة للبحث
        """
        if not search_term.strip():
            return self.get_all_debts()
        
        all_debts = self.get_all_debts()
        search_term = search_term.strip().lower()
        
        return [debt for debt in all_debts 
                if (search_term in debt.description.lower() or
                    search_term in debt.person_name.lower() or
                    search_term in str(debt.amount))]
    
    def get_debt_statistics(self) -> dict:
        """
        الحصول على إحصائيات الديون
        
        Returns:
            قاموس بالإحصائيات
        """
        all_debts = self.get_all_debts()
        unpaid_debts = [debt for debt in all_debts if not debt.is_paid]
        paid_debts = [debt for debt in all_debts if debt.is_paid]
        overdue_debts = self.get_overdue_debts()
        
        return {
            'total_debts_count': len(all_debts),
            'unpaid_debts_count': len(unpaid_debts),
            'paid_debts_count': len(paid_debts),
            'overdue_debts_count': len(overdue_debts),
            'total_unpaid_amount': sum(debt.amount for debt in unpaid_debts),
            'total_paid_amount': sum(debt.amount for debt in paid_debts),
            'total_overdue_amount': sum(debt.amount for debt in overdue_debts)
        }
