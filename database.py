# ملف قاعدة البيانات - Database Module
# يحتوي على إنشاء الجداول والعمليات الأساسية على قاعدة البيانات

import sqlite3
import os
from datetime import datetime

class DatabaseManager:
    """مدير قاعدة البيانات - يتولى إنشاء وإدارة قاعدة البيانات"""
    
    def __init__(self, db_name="store_management.db"):
        """تهيئة قاعدة البيانات"""
        self.db_name = db_name
        self.init_database()
    
    def get_connection(self):
        """إنشاء اتصال مع قاعدة البيانات"""
        return sqlite3.connect(self.db_name)
    
    def init_database(self):
        """إنشاء جداول قاعدة البيانات"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # جدول الزبائن
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS persons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT,
                address TEXT,
                created_date TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول الديون
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS debts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                person_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                debt_date TEXT DEFAULT CURRENT_TIMESTAMP,
                is_paid INTEGER DEFAULT 0,
                FOREIGN KEY (person_id) REFERENCES persons (id) ON DELETE CASCADE
            )
        ''')
        
        # جدول الأقساط
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS installments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                person_id INTEGER NOT NULL,
                total_amount REAL NOT NULL,
                paid_amount REAL DEFAULT 0,
                installment_amount REAL NOT NULL,
                due_date TEXT,
                description TEXT,
                is_completed INTEGER DEFAULT 0,
                created_date TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (person_id) REFERENCES persons (id) ON DELETE CASCADE
            )
        ''')
        
        # جدول اشتراكات الإنترنت
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS internet_subscriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                person_id INTEGER NOT NULL,
                plan_name TEXT NOT NULL,
                monthly_cost REAL NOT NULL,
                start_date TEXT,
                end_date TEXT,
                is_active INTEGER DEFAULT 1,
                description TEXT,
                FOREIGN KEY (person_id) REFERENCES persons (id) ON DELETE CASCADE
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def execute_query(self, query, params=None):
        """تنفيذ استعلام على قاعدة البيانات"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def fetch_all(self, query, params=None):
        """جلب جميع النتائج من الاستعلام"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()
        finally:
            conn.close()
    
    def fetch_one(self, query, params=None):
        """جلب نتيجة واحدة من الاستعلام"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchone()
        finally:
            conn.close()
