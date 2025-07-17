# -*- coding: utf-8 -*-
"""
منطق إدارة الأقساط
يحتوي على العمليات والقواعد الخاصة بالأقساط
"""

from typing import List, Optional
from datetime import date
from database.database_connection import DatabaseConnection
from database.queries import InstallmentQueries, PaymentQueries
from database.models import Installment, Payment


class InstallmentController:
    """
    كنترولر إدارة الأقساط
    """
    
    def __init__(self):
        self.db = DatabaseConnection()
        self.queries = InstallmentQueries(self.db)
        self.payment_queries = PaymentQueries(self.db)
    
    def add_installment(self, person_id: int, total_amount: float,
                       frequency: str, description: str, start_date: Optional[date] = None) -> tuple[bool, str, Optional[int]]:
        """
        إضافة قسط جديد
        
        Args:
            person_id: معرف الزبون
            total_amount: المبلغ الإجمالي
            frequency: دورية القسط (monthly, weekly, yearly)
            description: وصف القسط
            start_date: تاريخ البداية
            
        Returns:
            tuple: (نجح, رسالة, معرف القسط الجديد)
        """
        # التحقق من صحة البيانات
        from utils.validators import InstallmentValidator
        validator = InstallmentValidator()
        is_valid, error_message = validator.validate_installment_data(
            person_id, total_amount, 0, frequency, description,
            start_date, None
        )
        if not is_valid:
            return False, error_message, None
        
        # إنشاء القسط
        installment = Installment(
            person_id=person_id,
            total_amount=total_amount,
            paid_amount=0.0,
            installment_amount=0,
            frequency=frequency,
            description=description.strip(),
            start_date=start_date,
            end_date=None,
            is_completed=False
        )
        
        installment_id = self.queries.create_installment(installment)
        
        if installment_id:
            return True, "تم إضافة القسط بنجاح", installment_id
        else:
            return False, "حدث خطأ أثناء إضافة القسط", None
    
    def update_installment(self, installment_id: int, total_amount: float,
                          frequency: str, description: str,
                          start_date: Optional[date], paid_amount: float = -1) -> tuple[bool, str]:
        """
        تحديث قسط
        
        Args:
            installment_id: معرف القسط
            total_amount: المبلغ الإجمالي الجديد
            frequency: دورية القسط الجديدة
            description: الوصف الجديد
            start_date: تاريخ البداية الجديد
            paid_amount: المبلغ المدفوع الجديد (اختياري)
            
        Returns:
            tuple: (نجح, رسالة)
        """
        # التحقق من وجود القسط
        existing_installment = self.get_installment_by_id(installment_id)
        if not existing_installment:
            return False, "القسط غير موجود"
        
        # التحقق من صحة البيانات
        from utils.validators import InstallmentValidator
        validator = InstallmentValidator()
        is_valid, error_message = validator.validate_installment_data(
            existing_installment.person_id, total_amount, 0,
            frequency, description, start_date, None
        )
        if not is_valid:
            return False, error_message
        
        # استخدام المبلغ المدفوع الحالي إذا لم يتم توفيره
        current_paid_amount = paid_amount if paid_amount != -1 else existing_installment.paid_amount
        
        # التحقق من أن المبلغ المدفوع لا يتجاوز المبلغ الإجمالي
        if current_paid_amount > total_amount:
            return False, "المبلغ المدفوع لا يمكن أن يتجاوز المبلغ الإجمالي"
        
        # تحديد حالة الإكمال
        is_completed = current_paid_amount >= total_amount
        
        # تحديث البيانات
        updated_installment = Installment(
            id=installment_id,
            person_id=existing_installment.person_id,
            total_amount=total_amount,
            paid_amount=current_paid_amount,
            installment_amount=0,
            frequency=frequency,
            description=description.strip(),
            start_date=start_date,
            end_date=None,
            is_completed=is_completed
        )
        
        if self.queries.update_installment(updated_installment):
            return True, "تم تحديث القسط بنجاح"
        else:
            return False, "حدث خطأ أثناء تحديث القسط"
    
    def add_payment(self, installment_id: int, payment_amount: float, payment_date: Optional[date] = None) -> tuple[bool, str]:
        """
        إضافة دفعة للقسط
        
        Args:
            installment_id: معرف القسط
            payment_amount: مبلغ الدفعة
            payment_date: تاريخ الدفعة
            
        Returns:
            tuple: (نجح, رسالة)
        """
        existing_installment = self.get_installment_by_id(installment_id)
        if not existing_installment:
            return False, "القسط غير موجود"
        
        if payment_amount <= 0:
            return False, "مبلغ الدفعة يجب أن يكون أكبر من صفر"
        
        new_paid_amount = existing_installment.paid_amount + payment_amount
        
        if new_paid_amount > existing_installment.total_amount:
            return False, "مبلغ الدفعة يتجاوز المبلغ المتبقي"
            
        # إضافة الدفعة إلى جدول الدفعات
        payment = Payment(
            installment_id=installment_id,
            amount=payment_amount,
            payment_date=payment_date if payment_date else date.today()
        )
        payment_id = self.payment_queries.create_payment(payment)
        
        if not payment_id:
            return False, "فشل تسجيل الدفعة"

        # تحديث القسط
        return self.update_installment(
            installment_id, existing_installment.total_amount,
            existing_installment.frequency,
            existing_installment.description, existing_installment.start_date,
            paid_amount=new_paid_amount
        )
    
    def delete_installment(self, installment_id: int) -> tuple[bool, str]:
        """
        حذف قسط
        
        Args:
            installment_id: معرف القسط
            
        Returns:
            tuple: (نجح, رسالة)
        """
        # التحقق من وجود القسط
        existing_installment = self.get_installment_by_id(installment_id)
        if not existing_installment:
            return False, "القسط غير موجود"
        
        if self.queries.delete_installment(installment_id):
            return True, "تم حذف القسط بنجاح"
        else:
            return False, "حدث خطأ أثناء حذف القسط"
    
    def get_all_installments(self) -> List[Installment]:
        """
        الحصول على جميع الأقساط
        
        Returns:
            قائمة بجميع الأقساط
        """
        return self.queries.get_all_installments()
    
    def get_installments_by_person(self, person_id: int) -> List[Installment]:
        """
        الحصول على أقساط زبون معين
        
        Args:
            person_id: معرف الزبون
            
        Returns:
            قائمة بأقساط الزبون
        """
        return self.queries.get_installments_by_person(person_id)
    
    def get_installment_by_id(self, installment_id: int) -> Optional[Installment]:
        """
        الحصول على قسط بالمعرف
        
        Args:
            installment_id: معرف القسط
            
        Returns:
            القسط أو None
        """
        all_installments = self.get_all_installments()
        for installment in all_installments:
            if installment.id == installment_id:
                return installment
        return None
    
    def get_active_installments(self) -> List[Installment]:
        """
        الحصول على الأقساط النشطة (غير المكتملة)
        
        Returns:
            قائمة بالأقساط النشطة
        """
        all_installments = self.get_all_installments()
        return [inst for inst in all_installments if not inst.is_completed]
    
    def get_completed_installments(self) -> List[Installment]:
        """
        الحصول على الأقساط المكتملة
        
        Returns:
            قائمة بالأقساط المكتملة
        """
        all_installments = self.get_all_installments()
        return [inst for inst in all_installments if inst.is_completed]
    
    def search_installments(self, search_term: str) -> List[Installment]:
        """
        البحث في الأقساط
        
        Args:
            search_term: نص البحث
            
        Returns:
            قائمة بالأقساط المطابقة للبحث
        """
        if not search_term.strip():
            return self.get_all_installments()
        
        all_installments = self.get_all_installments()
        search_term = search_term.strip().lower()
        
        return [inst for inst in all_installments 
                if (search_term in inst.description.lower() or
                    search_term in inst.person_name.lower() or
                    search_term in str(inst.total_amount))]
    
    def get_installment_statistics(self) -> dict:
        """
        الحصول على إحصائيات الأقساط
        
        Returns:
            قاموس بالإحصائيات
        """
        all_installments = self.get_all_installments()
        active_installments = [inst for inst in all_installments if not inst.is_completed]
        completed_installments = [inst for inst in all_installments if inst.is_completed]
        
        return {
            'total_installments_count': len(all_installments),
            'active_installments_count': len(active_installments),
            'completed_installments_count': len(completed_installments),
            'total_amount': sum(inst.total_amount for inst in all_installments),
            'total_paid_amount': sum(inst.paid_amount for inst in all_installments),
            'total_remaining_amount': sum(inst.remaining_amount for inst in active_installments),
            'average_completion_rate': sum(inst.completion_percentage for inst in all_installments) / len(all_installments) if all_installments else 0
        }
