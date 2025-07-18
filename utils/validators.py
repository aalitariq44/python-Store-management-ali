# -*- coding: utf-8 -*-
"""
التحقق من صحة البيانات المدخلة
يحتوي على كلاسات للتحقق من صحة البيانات قبل إدراجها في قاعدة البيانات
"""

import re
from typing import Optional, Tuple
from datetime import date


class PersonValidator:
    """
    التحقق من صحة بيانات الزبائن
    """
    
    @staticmethod
    def validate_person_data(name: str, phone: str, address: str, notes: str) -> Tuple[bool, str]:
        """
        التحقق من صحة بيانات الزبون
        
        Args:
            name: اسم الزبون
            phone: رقم الهاتف
            address: العنوان
            notes: ملاحظات
            
        Returns:
            tuple: (صحيح, رسالة الخطأ)
        """
        # التحقق من الاسم
        if not name or not name.strip():
            return False, "اسم الزبون مطلوب"
        
        if len(name.strip()) < 2:
            return False, "اسم الزبون يجب أن يكون أكثر من حرفين"
        
        if len(name.strip()) > 100:
            return False, "اسم الزبون طويل جداً"
        
        # التحقق من رقم الهاتف
        if phone and phone.strip():
            if not PersonValidator.is_valid_phone(phone.strip()):
                return False, "رقم الهاتف غير صحيح"
        
        # التحقق من العنوان
        if address and len(address.strip()) > 200:
            return False, "العنوان طويل جداً"
        
        # التحقق من الملاحظات
        if notes and len(notes.strip()) > 500:
            return False, "الملاحظات طويلة جداً"
        
        return True, ""
    
    @staticmethod
    def is_valid_phone(phone: str) -> bool:
        """
        التحقق من صحة رقم الهاتف
        
        Args:
            phone: رقم الهاتف
            
        Returns:
            True إذا كان الرقم صحيح
        """
        # نمط بسيط لأرقام الهاتف (يمكن تعديله حسب الحاجة)
        pattern = r'^[\d\s\-\+\(\)]{7,20}$'
        return bool(re.match(pattern, phone))


class DebtValidator:
    """
    التحقق من صحة بيانات الديون
    """
    
    @staticmethod
    def validate_debt_data(person_id: int, amount: float, description: str, 
                          due_date: Optional[date]) -> Tuple[bool, str]:
        """
        التحقق من صحة بيانات الدين
        
        Args:
            person_id: معرف الزبون
            amount: مبلغ الدين
            description: وصف الدين
            due_date: تاريخ الاستحقاق
            
        Returns:
            tuple: (صحيح, رسالة الخطأ)
        """
        # التحقق من معرف الزبون
        if not person_id or person_id <= 0:
            return False, "معرف الزبون غير صحيح"
        
        # التحقق من المبلغ
        if amount <= 0:
            return False, "مبلغ الدين يجب أن يكون أكبر من صفر"
        
        if amount > 999999999:
            return False, "مبلغ الدين كبير جداً"
        
        # التحقق من الوصف
        if not description or not description.strip():
            return False, "وصف الدين مطلوب"
        
        if len(description.strip()) > 200:
            return False, "وصف الدين طويل جداً"
        
        # التحقق من تاريخ الاستحقاق
        if due_date and due_date < date.today():
            return False, "تاريخ الاستحقاق لا يمكن أن يكون في الماضي"
        
        return True, ""


class InstallmentValidator:
    """
    التحقق من صحة بيانات الأقساط
    """
    
    VALID_FREQUENCIES = ['monthly', 'weekly', 'yearly']
    
    @staticmethod
    def validate_installment_data(person_id: int, total_amount: float, 
                                 installment_amount: float, frequency: str,
                                 description: str, start_date: Optional[date],
                                 end_date: Optional[date]) -> Tuple[bool, str]:
        """
        التحقق من صحة بيانات القسط
        
        Args:
            person_id: معرف الزبون
            total_amount: المبلغ الإجمالي
            installment_amount: مبلغ القسط
            frequency: دورية القسط
            description: وصف القسط
            start_date: تاريخ البداية
            end_date: تاريخ النهاية
            
        Returns:
            tuple: (صحيح, رسالة الخطأ)
        """
        # التحقق من معرف الزبون
        if not person_id or person_id <= 0:
            return False, "معرف الزبون غير صحيح"
        
        # التحقق من المبلغ الإجمالي
        if total_amount <= 0:
            return False, "المبلغ الإجمالي يجب أن يكون أكبر من صفر"
        
        if total_amount > 999999999:
            return False, "المبلغ الإجمالي كبير جداً"
        
        # التحقق من مبلغ القسط
        if installment_amount > total_amount:
            return False, "مبلغ القسط لا يمكن أن يكون أكبر من المبلغ الإجمالي"
        
        # التحقق من الدورية
        if frequency not in InstallmentValidator.VALID_FREQUENCIES:
            return False, f"دورية القسط يجب أن تكون إحدى القيم التالية: {', '.join(InstallmentValidator.VALID_FREQUENCIES)}"
        
        # التحقق من الوصف
        if not description or not description.strip():
            return False, "وصف القسط مطلوب"
        
        if len(description.strip()) > 200:
            return False, "وصف القسط طويل جداً"
        
        # التحقق من التواريخ
        if start_date and end_date and start_date >= end_date:
            return False, "تاريخ البداية يجب أن يكون قبل تاريخ النهاية"
        
        return True, ""


class InternetSubscriptionValidator:
    """
    التحقق من صحة بيانات اشتراكات الإنترنت
    """
    
    @staticmethod
    def validate_subscription_data(person_id: int, plan_name: str, monthly_fee: float,
                                  start_date: Optional[date],
                                  end_date: Optional[date]) -> Tuple[bool, str]:
        """
        التحقق من صحة بيانات الاشتراك
        
        Args:
            person_id: معرف الزبون
            plan_name: اسم الباقة
            monthly_fee: الرسوم الشهرية
            start_date: تاريخ البداية
            end_date: تاريخ النهاية
            
        Returns:
            tuple: (صحيح, رسالة الخطأ)
        """
        # التحقق من معرف الزبون
        if not person_id or person_id <= 0:
            return False, "معرف الزبون غير صحيح"
        
        # التحقق من اسم الباقة
        if not plan_name or not plan_name.strip():
            return False, "اسم الباقة مطلوب"
        
        if len(plan_name.strip()) > 100:
            return False, "اسم الباقة طويل جداً"
        
        # التحقق من الرسوم الشهرية
        if monthly_fee < 0:
            return False, "الرسوم الشهرية لا يمكن أن تكون سالبة"
        
        if monthly_fee > 999999:
            return False, "الرسوم الشهرية كبيرة جداً"
        
        # التحقق من التواريخ
        if start_date and end_date and start_date >= end_date:
            return False, "تاريخ البداية يجب أن يكون قبل تاريخ النهاية"
        
        return True, ""
