# -*- coding: utf-8 -*-
"""
إدارة الاتصال مع قاعدة البيانات SQLite
يتعامل مع إنشاء الاتصال والجداول
"""

import sqlite3
import os
from typing import Optional


class DatabaseConnection:
    """
    كلاس لإدارة الاتصال مع قاعدة البيانات
    """
    
    def __init__(self, db_path: str = "store_management.db"):
        """
        تهيئة الاتصال مع قاعدة البيانات
        
        Args:
            db_path: مسار ملف قاعدة البيانات
        """
        self.db_path = db_path
        self.connection: Optional[sqlite3.Connection] = None
        self.create_database()
    
    def get_connection(self) -> sqlite3.Connection:
        """
        الحصول على اتصال مع قاعدة البيانات
        
        Returns:
            sqlite3.Connection: كائن الاتصال
        """
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row  # للحصول على النتائج كقاموس
        return self.connection
    
    def close_connection(self):
        """
        إغلاق الاتصال مع قاعدة البيانات
        """
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def create_database(self):
        """
        إنشاء قاعدة البيانات والجداول المطلوبة
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # جدول الزبائن
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS persons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT,
                address TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # جدول الديون
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS debts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                person_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                due_date DATE,
                is_paid BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (person_id) REFERENCES persons (id) ON DELETE CASCADE
            )
        """)
        
        # جدول الأقساط
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS installments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                person_id INTEGER NOT NULL,
                total_amount REAL NOT NULL,
                description TEXT,
                start_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (person_id) REFERENCES persons (id) ON DELETE CASCADE
            )
        """)
        
        # جدول اشتراكات الإنترنت
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS internet_subscriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                person_id INTEGER NOT NULL,
                plan_name TEXT NOT NULL,
                monthly_fee REAL NOT NULL,
                speed TEXT,
                start_date DATE,
                end_date DATE,
                is_active BOOLEAN DEFAULT TRUE,
                payment_status TEXT DEFAULT 'unpaid',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (person_id) REFERENCES persons (id) ON DELETE CASCADE
            )
        """)
        
        # جدول الدفعات
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                installment_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                payment_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (installment_id) REFERENCES installments (id) ON DELETE CASCADE
            )
        """)
        
        # جدول إعدادات التسجيل
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS auth_settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                password TEXT NOT NULL,
                is_first_time BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        self._migrate_schema(conn)

    def _migrate_schema(self, conn: sqlite3.Connection):
        """
        تطبيق التغييرات على مخطط قاعدة البيانات الموجودة لضمان التوافق.
        """
        cursor = conn.cursor()
        
        # --- ترحيل جدول الأقساط ---
        try:
            cursor.execute("PRAGMA table_info(installments)")
            columns = [row['name'] for row in cursor.fetchall()]
            
            # التحقق من وجود الأعمدة القديمة لتحديد ما إذا كان الترحيل مطلوبًا
            if 'paid_amount' in columns or 'installment_amount' in columns or 'frequency' in columns:
                print("Starting migration for 'installments' table...")
                
                # 1. إعادة تسمية الجدول الحالي
                cursor.execute("ALTER TABLE installments RENAME TO installments_old")
                
                # 2. إنشاء الجدول الجديد بالمخطط المحدث
                cursor.execute("""
                    CREATE TABLE installments (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        person_id INTEGER NOT NULL,
                        total_amount REAL NOT NULL,
                        description TEXT,
                        start_date DATE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (person_id) REFERENCES persons (id) ON DELETE CASCADE
                    )
                """)
                
                # 3. نسخ البيانات من الجدول القديم إلى الجديد
                cursor.execute("""
                    INSERT INTO installments (id, person_id, total_amount, description, start_date, created_at)
                    SELECT id, person_id, total_amount, description, start_date, created_at
                    FROM installments_old
                """)
                
                # 4. حذف الجدول القديم
                cursor.execute("DROP TABLE installments_old")
                
                conn.commit()
                print("Migration successful: 'installments' table has been updated.")
        except sqlite3.Error as e:
            print(f"Migration failed for 'installments' table: {e}")
            conn.rollback()

        # --- ترحيلات أخرى ---
        # التحقق من وجود عمود 'updated_at' في جدول 'internet_subscriptions'
        try:
            cursor.execute("PRAGMA table_info(internet_subscriptions)")
            columns = [row['name'] for row in cursor.fetchall()]
            
            if 'updated_at' not in columns:
                cursor.execute("ALTER TABLE internet_subscriptions ADD COLUMN updated_at TIMESTAMP")
                cursor.execute("UPDATE internet_subscriptions SET updated_at = created_at WHERE updated_at IS NULL")
                conn.commit()
                print("Migration successful: 'updated_at' column added to 'internet_subscriptions'.")
        except sqlite3.Error as e:
            print(f"Migration check failed for 'internet_subscriptions': {e}")
            conn.rollback()

        # التحقق من وجود عمود 'payment_status' في جدول 'internet_subscriptions'
        try:
            cursor.execute("PRAGMA table_info(internet_subscriptions)")
            columns = [row['name'] for row in cursor.fetchall()]
            
            if 'payment_status' not in columns:
                cursor.execute("ALTER TABLE internet_subscriptions ADD COLUMN payment_status TEXT DEFAULT 'unpaid'")
                conn.commit()
                print("Migration successful: 'payment_status' column added to 'internet_subscriptions'.")
        except sqlite3.Error as e:
            print(f"Migration check failed for 'internet_subscriptions' (payment_status): {e}")
            conn.rollback()

        # التحقق من وجود عمود 'notes' في جدول 'persons'
        try:
            cursor.execute("PRAGMA table_info(persons)")
            columns = [row['name'] for row in cursor.fetchall()]
            
            if 'notes' not in columns:
                cursor.execute("ALTER TABLE persons ADD COLUMN notes TEXT")
                conn.commit()
                print("Migration successful: 'notes' column added to 'persons'.")
        except sqlite3.Error as e:
            print(f"Migration check failed for 'persons': {e}")
            conn.rollback()

    def execute_query(self, query: str, params: tuple = None):
        """
        تنفيذ استعلام SQL
        
        Args:
            query: الاستعلام
            params: المعاملات
            
        Returns:
            النتائج أو None
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            conn.commit()
            return cursor.fetchall()
        
        except sqlite3.Error as e:
            print(f"خطأ في قاعدة البيانات: {e}")
            conn.rollback()
            return None
    
    def execute_insert(self, query: str, params: tuple = None):
        """
        تنفيذ استعلام إدراج والحصول على ID الصف المُدرج
        
        Args:
            query: الاستعلام
            params: المعاملات
            
        Returns:
            ID الصف المُدرج أو None
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            conn.commit()
            return cursor.lastrowid
        
        except sqlite3.Error as e:
            print(f"خطأ في قاعدة البيانات: {e}")
            conn.rollback()
            return None
