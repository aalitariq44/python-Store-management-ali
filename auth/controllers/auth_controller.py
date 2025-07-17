# -*- coding: utf-8 -*-
"""
كنترولر تسجيل الدخول
يتعامل مع عمليات التحقق من كلمة المرور وإدارة إعدادات التسجيل
"""

from typing import Optional, Tuple
from datetime import datetime
from database.database_connection import DatabaseConnection
from database.models import AuthSettings


class AuthController:
    """
    كنترولر تسجيل الدخول
    """
    
    def __init__(self, db_connection: DatabaseConnection):
        """
        تهيئة كنترولر تسجيل الدخول
        
        Args:
            db_connection: اتصال قاعدة البيانات
        """
        self.db_connection = db_connection
    
    def is_first_time_setup(self) -> bool:
        """
        التحقق من أن هذه أول مرة لتشغيل التطبيق
        
        Returns:
            True إذا كانت أول مرة، False خلاف ذلك
        """
        try:
            conn = self.db_connection.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM auth_settings")
            count = cursor.fetchone()[0]
            
            return count == 0
            
        except Exception as e:
            print(f"خطأ في التحقق من الإعداد الأولي: {str(e)}")
            return True
    
    def setup_first_password(self, password: str, confirm_password: str) -> Tuple[bool, str]:
        """
        إعداد كلمة المرور لأول مرة
        
        Args:
            password: كلمة المرور
            confirm_password: تأكيد كلمة المرور
            
        Returns:
            tuple: (نجح العملية, رسالة)
        """
        try:
            # التحقق من تطابق كلمتي المرور
            if password != confirm_password:
                return False, "كلمتا المرور غير متطابقتان"
            
            # التحقق من أن كلمة المرور ليست فارغة
            if not password.strip():
                return False, "كلمة المرور لا يمكن أن تكون فارغة"
            
            # التحقق من أن هذه أول مرة
            if not self.is_first_time_setup():
                return False, "تم إعداد كلمة المرور مسبقاً"
            
            # حفظ كلمة المرور
            conn = self.db_connection.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO auth_settings (password, is_first_time, created_at, updated_at)
                VALUES (?, ?, ?, ?)
            """, (password, False, datetime.now(), datetime.now()))
            
            conn.commit()
            return True, "تم إعداد كلمة المرور بنجاح"
            
        except Exception as e:
            print(f"خطأ في إعداد كلمة المرور: {str(e)}")
            return False, f"خطأ في إعداد كلمة المرور: {str(e)}"
    
    def verify_password(self, password: str) -> Tuple[bool, str]:
        """
        التحقق من كلمة المرور
        
        Args:
            password: كلمة المرور المدخلة
            
        Returns:
            tuple: (نجح التحقق, رسالة)
        """
        try:
            conn = self.db_connection.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT password FROM auth_settings ORDER BY id DESC LIMIT 1")
            result = cursor.fetchone()
            
            if not result:
                return False, "لم يتم إعداد كلمة المرور بعد"
            
            stored_password = result[0]
            
            if password == stored_password:
                return True, "تم التحقق من كلمة المرور بنجاح"
            else:
                return False, "كلمة المرور غير صحيحة"
                
        except Exception as e:
            print(f"خطأ في التحقق من كلمة المرور: {str(e)}")
            return False, f"خطأ في التحقق من كلمة المرور: {str(e)}"
    
    def change_password(self, old_password: str, new_password: str, confirm_new_password: str) -> Tuple[bool, str]:
        """
        تغيير كلمة المرور
        
        Args:
            old_password: كلمة المرور القديمة
            new_password: كلمة المرور الجديدة
            confirm_new_password: تأكيد كلمة المرور الجديدة
            
        Returns:
            tuple: (نجح التغيير, رسالة)
        """
        try:
            # التحقق من كلمة المرور القديمة
            is_valid, message = self.verify_password(old_password)
            if not is_valid:
                return False, "كلمة المرور القديمة غير صحيحة"
            
            # التحقق من تطابق كلمة المرور الجديدة
            if new_password != confirm_new_password:
                return False, "كلمة المرور الجديدة وتأكيدها غير متطابقتان"
            
            # التحقق من أن كلمة المرور الجديدة ليست فارغة
            if not new_password.strip():
                return False, "كلمة المرور الجديدة لا يمكن أن تكون فارغة"
            
            # التحقق من أن كلمة المرور الجديدة مختلفة عن القديمة
            if old_password == new_password:
                return False, "كلمة المرور الجديدة يجب أن تكون مختلفة عن القديمة"
            
            # تحديث كلمة المرور
            conn = self.db_connection.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE auth_settings 
                SET password = ?, updated_at = ?
                WHERE id = (SELECT id FROM auth_settings ORDER BY id DESC LIMIT 1)
            """, (new_password, datetime.now()))
            
            conn.commit()
            return True, "تم تغيير كلمة المرور بنجاح"
            
        except Exception as e:
            print(f"خطأ في تغيير كلمة المرور: {str(e)}")
            return False, f"خطأ في تغيير كلمة المرور: {str(e)}"
    
    def get_auth_settings(self) -> Optional[AuthSettings]:
        """
        الحصول على إعدادات التسجيل
        
        Returns:
            AuthSettings أو None
        """
        try:
            conn = self.db_connection.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, password, is_first_time, created_at, updated_at
                FROM auth_settings 
                ORDER BY id DESC 
                LIMIT 1
            """)
            
            result = cursor.fetchone()
            if result:
                return AuthSettings(
                    id=result[0],
                    password=result[1],
                    is_first_time=bool(result[2]),
                    created_at=datetime.fromisoformat(result[3]) if result[3] else None,
                    updated_at=datetime.fromisoformat(result[4]) if result[4] else None
                )
            
            return None
            
        except Exception as e:
            print(f"خطأ في الحصول على إعدادات التسجيل: {str(e)}")
            return None
