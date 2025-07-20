# -*- coding: utf-8 -*-
"""
منطق إدارة الأقساط
يحتوي على العمليات والقواعد الخاصة بالأقساط
"""

from typing import List, Optional, Tuple
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
                       description: str, start_date: Optional[date] = None) -> Tuple[bool, str, Optional[int]]:
        """
        إضافة قسط جديد
        
        Args:
            person_id: معرف الزبون
            total_amount: المبلغ الإجمالي
            description: وصف القسط
            start_date: تاريخ البداية
            
        Returns:
            tuple: (نجح, رسالة, معرف القسط الجديد)
        """
        # التحقق من صحة البيانات
        if not person_id:
            return False, "الرجاء تحديد زبون.", None
        if total_amount <= 0:
            return False, "المبلغ الإجمالي يجب أن يكون أكبر من صفر.", None
        if not description.strip():
            return False, "وصف القسط مطلوب.", None

        # إنشاء القسط
        installment = Installment(
            person_id=person_id,
            total_amount=total_amount,
            description=description.strip(),
            start_date=start_date
        )
        
        installment_id = self.queries.create_installment(installment)
        
        if installment_id:
            return True, "تم إضافة القسط بنجاح", installment_id
        else:
            return False, "حدث خطأ أثناء إضافة القسط", None
    
    def update_installment(self, installment_id: int, total_amount: float,
                          description: str, start_date: Optional[date]) -> Tuple[bool, str]:
        """
        تحديث قسط
        
        Args:
            installment_id: معرف القسط
            total_amount: المبلغ الإجمالي الجديد
            description: الوصف الجديد
            start_date: تاريخ البداية الجديد
            
        Returns:
            tuple: (نجح, رسالة)
        """
        # التحقق من وجود القسط
        existing_installment = self.get_installment_by_id(installment_id)
        if not existing_installment:
            return False, "القسط غير موجود"
        
        # التحقق من صحة البيانات
        if total_amount <= 0:
            return False, "المبلغ الإجمالي يجب أن يكون أكبر من صفر."
        if not description.strip():
            return False, "وصف القسط مطلوب."
        
        # التحقق من أن المبلغ المدفوع لا يتجاوز المبلغ الإجمالي الجديد
        if existing_installment.paid_amount > total_amount:
            return False, "المبلغ الإجمالي الجديد لا يمكن أن يكون أقل من المبلغ المدفوع حالياً."

        # تحديث البيانات
        updated_installment = Installment(
            id=installment_id,
            person_id=existing_installment.person_id,
            total_amount=total_amount,
            description=description.strip(),
            start_date=start_date
        )
        
        if self.queries.update_installment(updated_installment):
            return True, "تم تحديث القسط بنجاح"
        else:
            return False, "حدث خطأ أثناء تحديث القسط"
    
    def add_payment(self, installment_id: int, payment_amount: float, payment_date: Optional[date] = None) -> Tuple[bool, str]:
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
        
        # التحقق من أن الدفعة الجديدة لا تجعل المبلغ المدفوع يتجاوز الإجمالي
        if (existing_installment.paid_amount + payment_amount) > existing_installment.total_amount:
            return False, f"مبلغ الدفعة كبير جداً. المبلغ المتبقي هو {existing_installment.remaining_amount}"
            
        # إضافة الدفعة إلى جدول الدفعات
        payment = Payment(
            installment_id=installment_id,
            amount=payment_amount,
            payment_date=payment_date if payment_date else date.today()
        )
        payment_id = self.payment_queries.create_payment(payment)
        
        if payment_id:
            return True, "تمت إضافة الدفعة بنجاح"
        else:
            return False, "فشل تسجيل الدفعة"
    
    def delete_installment(self, installment_id: int) -> Tuple[bool, str]:
        """
        حذف قسط وجميع الدفعات المرتبطة به
        
        Args:
            installment_id: معرف القسط
            
        Returns:
            tuple: (نجح, رسالة)
        """
        # التحقق من وجود القسط
        existing_installment = self.get_installment_by_id(installment_id)
        if not existing_installment:
            return False, "القسط غير موجود"
        
        # أولاً، حذف جميع الدفعات المرتبطة بهذا القسط
        payments_deleted, payments_message = self.payment_queries.delete_payments_by_installment_id(installment_id)
        if not payments_deleted:
            return False, f"فشل حذف الدفعات المرتبطة: {payments_message}"

        # ثانياً، حذف القسط نفسه
        if self.queries.delete_installment(installment_id):
            return True, "تم حذف القسط وجميع دفعاته بنجاح"
        else:
            return False, "حدث خطأ أثناء حذف القسط بعد حذف الدفعات"
    
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
        return self.queries.get_installment_by_id(installment_id)
    
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
