# -*- coding: utf-8 -*-
"""
تعريف النماذج (Models) للبيانات
يحتوي على كلاسات تمثل الكيانات في قاعدة البيانات
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime, date


@dataclass
class Person:
    """
    نموذج الزبون
    """
    id: Optional[int] = None
    name: str = ""
    phone: str = ""
    address: str = ""
    notes: str = ""
    created_at: Optional[datetime] = None
    
    def __str__(self):
        return f"{self.name} - {self.phone}"


@dataclass
class Debt:
    """
    نموذج الدين
    """
    id: Optional[int] = None
    person_id: int = 0
    amount: float = 0.0
    description: str = ""
    due_date: Optional[date] = None
    is_paid: bool = False
    created_at: Optional[datetime] = None
    person_name: str = ""  # للعرض في القوائم العامة
    
    def __str__(self):
        status = "مدفوع" if self.is_paid else "غير مدفوع"
        return f"{self.description} - {self.amount} - {status}"


@dataclass
class Installment:
    """
    نموذج القسط
    """
    id: Optional[int] = None
    person_id: int = 0
    total_amount: float = 0.0
    description: str = ""
    start_date: Optional[date] = None
    created_at: Optional[datetime] = None
    person_name: str = ""  # للعرض في القوائم العامة

    # الحقل التالي يتم حسابه ديناميكياً ولا يتم تخزينه في قاعدة البيانات
    # This field is calculated dynamically and not stored in the database
    paid_amount: float = 0.0

    @property
    def remaining_amount(self) -> float:
        """
        المبلغ المتبقي
        """
        return self.total_amount - self.paid_amount

    @property
    def is_completed(self) -> bool:
        """
        هل القسط مكتمل
        """
        return self.remaining_amount <= 0

    @property
    def completion_percentage(self) -> float:
        """
        نسبة الإنجاز
        """
        if self.total_amount == 0:
            return 100.0
        percentage = (self.paid_amount / self.total_amount) * 100
        return min(percentage, 100.0)

    def __str__(self):
        status = "مكتمل" if self.is_completed else "غير مكتمل"
        return f"{self.description} - {self.paid_amount}/{self.total_amount} ({status})"


@dataclass
class InternetSubscription:
    """
    نموذج اشتراك الإنترنت
    """
    id: Optional[int] = None
    person_id: int = 0
    plan_name: str = ""
    monthly_fee: float = 0.0
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_active: bool = True
    payment_status: str = "unpaid"  # 'paid' or 'unpaid'
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    person_name: str = ""  # للعرض في القوائم العامة
    
    def __str__(self):
        status = "نشط" if self.is_active else "غير نشط"
        return f"{self.plan_name} - {status}"


@dataclass
class Payment:
    """
    نموذج الدفعة
    """
    id: Optional[int] = None
    installment_id: int = 0
    amount: float = 0.0
    payment_date: Optional[date] = None
    created_at: Optional[datetime] = None


@dataclass
class AuthSettings:
    """
    نموذج إعدادات التسجيل
    """
    id: Optional[int] = None
    password: str = ""
    is_first_time: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __str__(self):
        return "إعدادات كلمة المرور"
