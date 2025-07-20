# -*- coding: utf-8 -*-
"""
منطق إدارة اشتراكات الإنترنت
يحتوي على العمليات والقواعد الخاصة باشتراكات الإنترنت
"""

from typing import List, Optional, Tuple
from datetime import date
from database.database_connection import DatabaseConnection
from database.queries import InternetSubscriptionQueries
from database.models import InternetSubscription


class InternetController:
    """
    كنترولر إدارة اشتراكات الإنترنت
    """
    
    def __init__(self):
        self.db = DatabaseConnection()
        self.queries = InternetSubscriptionQueries(self.db)
    
    def add_subscription(self, person_id: int, plan_name: str, monthly_fee: float,
                        start_date: Optional[date] = None,
                        end_date: Optional[date] = None,
                        payment_status: str = 'unpaid') -> Tuple[bool, str, Optional[int]]:
        """
        إضافة اشتراك جديد
        
        Args:
            person_id: معرف الزبون
            plan_name: اسم الباقة
            monthly_fee: الرسوم الشهرية
            start_date: تاريخ البداية
            end_date: تاريخ النهاية
            payment_status: حالة الدفع
            
        Returns:
            tuple: (نجح, رسالة, معرف الاشتراك الجديد)
        """
        # التحقق من صحة البيانات
        from utils.validators import InternetSubscriptionValidator
        validator = InternetSubscriptionValidator()
        is_valid, error_message = validator.validate_subscription_data(
            person_id, plan_name, monthly_fee, start_date, end_date
        )
        if not is_valid:
            return False, error_message, None
        
        # تحديد الحالة بناءً على التاريخ
        is_active = False
        if start_date and end_date:
            today = date.today()
            is_active = start_date <= today <= end_date

        # إنشاء الاشتراك
        subscription = InternetSubscription(
            person_id=person_id,
            plan_name=plan_name.strip(),
            monthly_fee=monthly_fee,
            start_date=start_date,
            end_date=end_date,
            is_active=is_active,
            payment_status=payment_status
        )
        
        subscription_id = self.queries.create_subscription(subscription)
        
        if subscription_id:
            return True, "تم إضافة الاشتراك بنجاح", subscription_id
        else:
            return False, "حدث خطأ أثناء إضافة الاشتراك", None
    
    def update_subscription(self, subscription_id: int, plan_name: str, monthly_fee: float,
                           start_date: Optional[date], end_date: Optional[date],
                           payment_status: str) -> Tuple[bool, str]:
        """
        تحديث اشتراك
        
        Args:
            subscription_id: معرف الاشتراك
            plan_name: اسم الباقة الجديد
            monthly_fee: الرسوم الشهرية الجديدة
            start_date: تاريخ البداية الجديد
            end_date: تاريخ النهاية الجديد
            payment_status: حالة الدفع الجديدة
            
        Returns:
            tuple: (نجح, رسالة)
        """
        # التحقق من وجود الاشتراك
        existing_subscription = self.get_subscription_by_id(subscription_id)
        if not existing_subscription:
            return False, "الاشتراك غير موجود"
        
        # التحقق من صحة البيانات
        from utils.validators import InternetSubscriptionValidator
        validator = InternetSubscriptionValidator()
        is_valid, error_message = validator.validate_subscription_data(
            existing_subscription.person_id, plan_name, monthly_fee,
            start_date, end_date
        )
        if not is_valid:
            return False, error_message
        
        # تحديد الحالة بناءً على التاريخ
        is_active = False
        if start_date and end_date:
            today = date.today()
            is_active = start_date <= today <= end_date

        # تحديث البيانات
        updated_subscription = InternetSubscription(
            id=subscription_id,
            person_id=existing_subscription.person_id,
            plan_name=plan_name.strip(),
            monthly_fee=monthly_fee,
            start_date=start_date,
            end_date=end_date,
            is_active=is_active,
            payment_status=payment_status
        )
        
        if self.queries.update_subscription(updated_subscription):
            return True, "تم تحديث الاشتراك بنجاح"
        else:
            return False, "حدث خطأ أثناء تحديث الاشتراك"

    def update_subscription_payment_status(self, subscription_id: int, payment_status: str) -> Tuple[bool, str]:
        """
        تحديث حالة الدفع لاشتراك
        
        Args:
            subscription_id: معرف الاشتراك
            payment_status: حالة الدفع الجديدة ('paid' or 'unpaid')
            
        Returns:
            tuple: (نجح, رسالة)
        """
        if payment_status not in ['paid', 'unpaid']:
            return False, "حالة الدفع غير صالحة"
            
        if self.queries.update_subscription_payment_status(subscription_id, payment_status):
            return True, "تم تحديث حالة الدفع بنجاح"
        else:
            return False, "حدث خطأ أثناء تحديث حالة الدفع"

    def delete_subscription(self, subscription_id: int) -> Tuple[bool, str]:
        """
        حذف اشتراك
        
        Args:
            subscription_id: معرف الاشتراك
            
        Returns:
            tuple: (نجح, رسالة)
        """
        # التحقق من وجود الاشتراك
        existing_subscription = self.get_subscription_by_id(subscription_id)
        if not existing_subscription:
            return False, "الاشتراك غير موجود"
        
        if self.queries.delete_subscription(subscription_id):
            return True, "تم حذف الاشتراك بنجاح"
        else:
            return False, "حدث خطأ أثناء حذف الاشتراك"
    
    def get_all_subscriptions(self) -> List[InternetSubscription]:
        """
        الحصول على جميع الاشتراكات
        
        Returns:
            قائمة بجميع الاشتراكات
        """
        return self.queries.get_all_subscriptions()
    
    def get_subscriptions_by_person(self, person_id: int) -> List[InternetSubscription]:
        """
        الحصول على اشتراكات زبون معين
        
        Args:
            person_id: معرف الزبون
            
        Returns:
            قائمة باشتراكات الزبون
        """
        return self.queries.get_subscriptions_by_person(person_id)
    
    def get_subscription_by_id(self, subscription_id: int) -> Optional[InternetSubscription]:
        """
        الحصول على اشتراك بالمعرف
        
        Args:
            subscription_id: معرف الاشتراك
            
        Returns:
            الاشتراك أو None
        """
        all_subscriptions = self.get_all_subscriptions()
        for subscription in all_subscriptions:
            if subscription.id == subscription_id:
                return subscription
        return None
    
    def get_active_subscriptions(self) -> List[InternetSubscription]:
        """
        الحصول على الاشتراكات النشطة
        
        Returns:
            قائمة بالاشتراكات النشطة
        """
        all_subscriptions = self.get_all_subscriptions()
        return [sub for sub in all_subscriptions if sub.is_active]
    
    def get_inactive_subscriptions(self) -> List[InternetSubscription]:
        """
        الحصول على الاشتراكات غير النشطة
        
        Returns:
            قائمة بالاشتراكات غير النشطة
        """
        all_subscriptions = self.get_all_subscriptions()
        return [sub for sub in all_subscriptions if not sub.is_active]
    
    def get_expired_subscriptions(self) -> List[InternetSubscription]:
        """
        الحصول على الاشتراكات المنتهية الصلاحية
        
        Returns:
            قائمة بالاشتراكات المنتهية الصلاحية
        """
        today = date.today()
        all_subscriptions = self.get_all_subscriptions()
        
        return [sub for sub in all_subscriptions 
                if sub.end_date and sub.end_date < today]
    
    def search_subscriptions(self, search_term: str) -> List[InternetSubscription]:
        """
        البحث في الاشتراكات
        
        Args:
            search_term: نص البحث
            
        Returns:
            قائمة بالاشتراكات المطابقة للبحث
        """
        if not search_term.strip():
            return self.get_all_subscriptions()
        
        all_subscriptions = self.get_all_subscriptions()
        search_term = search_term.strip().lower()
        
        return [sub for sub in all_subscriptions 
                if (search_term in (sub.plan_name or "").lower() or
                    search_term in (sub.person_name or "").lower() or
                    search_term in str(sub.monthly_fee))]
    
    def get_subscription_statistics(self) -> dict:
        """
        الحصول على إحصائيات الاشتراكات
        
        Returns:
            قاموس بالإحصائيات
        """
        all_subscriptions = self.get_all_subscriptions()
        today = date.today()
        
        active_subscriptions = []
        expired_subscriptions = []
        
        for sub in all_subscriptions:
            if sub.start_date and sub.end_date:
                if sub.start_date <= today <= sub.end_date:
                    active_subscriptions.append(sub)
                elif sub.end_date < today:
                    expired_subscriptions.append(sub)
        
        paid_count = sum(1 for sub in all_subscriptions if sub.payment_status == 'paid')
        unpaid_count = len(all_subscriptions) - paid_count

        return {
            'total_subscriptions_count': len(all_subscriptions),
            'active_subscriptions_count': len(active_subscriptions),
            'expired_subscriptions_count': len(expired_subscriptions),
            'paid_count': paid_count,
            'unpaid_count': unpaid_count,
            'total_monthly_revenue': sum(sub.monthly_fee for sub in active_subscriptions),
            'average_monthly_fee': sum(sub.monthly_fee for sub in all_subscriptions) / len(all_subscriptions) if all_subscriptions else 0
        }
