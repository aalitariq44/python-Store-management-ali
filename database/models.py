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
    paid_amount: float = 0.0
    installment_amount: float = 0.0
    frequency: str = "monthly"  # monthly, weekly, yearly
    description: str = ""
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_completed: bool = False
    created_at: Optional[datetime] = None
    person_name: str = ""  # للعرض في القوائم العامة
    
    @property
    def remaining_amount(self) -> float:
        """
        المبلغ المتبقي
        """
        return self.total_amount - self.paid_amount
    
    @property
    def completion_percentage(self) -> float:
        """
        نسبة الإنجاز
        """
        if self.total_amount == 0:
            return 0.0
        return (self.paid_amount / self.total_amount) * 100
    
    def __str__(self):
        return f"{self.description} - {self.paid_amount}/{self.total_amount}"


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
