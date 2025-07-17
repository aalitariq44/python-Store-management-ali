# نماذج البيانات - Data Models
# يحتوي على الكلاسات التي تمثل البيانات في التطبيق

from database import DatabaseManager
from datetime import datetime

class Person:
    """نموذج الزبون"""
    
    def __init__(self, db_manager):
        self.db = db_manager
    
    def add_person(self, name, phone, address):
        """إضافة زبون جديد"""
        query = "INSERT INTO persons (name, phone, address) VALUES (?, ?, ?)"
        return self.db.execute_query(query, (name, phone, address))
    
    def update_person(self, person_id, name, phone, address):
        """تعديل بيانات الزبون"""
        query = "UPDATE persons SET name=?, phone=?, address=? WHERE id=?"
        return self.db.execute_query(query, (name, phone, address, person_id))
    
    def delete_person(self, person_id):
        """حذف زبون"""
        query = "DELETE FROM persons WHERE id=?"
        return self.db.execute_query(query, (person_id,))
    
    def get_all_persons(self):
        """جلب جميع الزبائن"""
        query = "SELECT * FROM persons ORDER BY name"
        return self.db.fetch_all(query)
    
    def get_person_by_id(self, person_id):
        """جلب زبون معين بالمعرف"""
        query = "SELECT * FROM persons WHERE id=?"
        return self.db.fetch_one(query, (person_id,))
    
    def search_persons(self, search_term):
        """البحث عن الزبائن"""
        query = "SELECT * FROM persons WHERE name LIKE ? OR phone LIKE ? OR address LIKE ?"
        search_pattern = f"%{search_term}%"
        return self.db.fetch_all(query, (search_pattern, search_pattern, search_pattern))

class Debt:
    """نموذج الديون"""
    
    def __init__(self, db_manager):
        self.db = db_manager
    
    def add_debt(self, person_id, amount, description=""):
        """إضافة دين جديد"""
        query = "INSERT INTO debts (person_id, amount, description) VALUES (?, ?, ?)"
        return self.db.execute_query(query, (person_id, amount, description))
    
    def update_debt(self, debt_id, amount, description, is_paid):
        """تعديل الدين"""
        query = "UPDATE debts SET amount=?, description=?, is_paid=? WHERE id=?"
        return self.db.execute_query(query, (amount, description, is_paid, debt_id))
    
    def delete_debt(self, debt_id):
        """حذف دين"""
        query = "DELETE FROM debts WHERE id=?"
        return self.db.execute_query(query, (debt_id,))
    
    def get_debts_by_person(self, person_id):
        """جلب ديون زبون معين"""
        query = "SELECT * FROM debts WHERE person_id=? ORDER BY debt_date DESC"
        return self.db.fetch_all(query, (person_id,))
    
    def get_all_debts(self):
        """جلب جميع الديون مع بيانات الزبائن"""
        query = """
            SELECT d.*, p.name, p.phone 
            FROM debts d 
            JOIN persons p ON d.person_id = p.id 
            ORDER BY d.debt_date DESC
        """
        return self.db.fetch_all(query)

class Installment:
    """نموذج الأقساط"""
    
    def __init__(self, db_manager):
        self.db = db_manager
    
    def add_installment(self, person_id, total_amount, installment_amount, due_date, description=""):
        """إضافة قسط جديد"""
        query = """
            INSERT INTO installments (person_id, total_amount, installment_amount, due_date, description) 
            VALUES (?, ?, ?, ?, ?)
        """
        return self.db.execute_query(query, (person_id, total_amount, installment_amount, due_date, description))
    
    def update_installment(self, installment_id, total_amount, paid_amount, installment_amount, due_date, description, is_completed):
        """تعديل القسط"""
        query = """
            UPDATE installments 
            SET total_amount=?, paid_amount=?, installment_amount=?, due_date=?, description=?, is_completed=? 
            WHERE id=?
        """
        return self.db.execute_query(query, (total_amount, paid_amount, installment_amount, due_date, description, is_completed, installment_id))
    
    def delete_installment(self, installment_id):
        """حذف قسط"""
        query = "DELETE FROM installments WHERE id=?"
        return self.db.execute_query(query, (installment_id,))
    
    def get_installments_by_person(self, person_id):
        """جلب أقساط زبون معين"""
        query = "SELECT * FROM installments WHERE person_id=? ORDER BY due_date DESC"
        return self.db.fetch_all(query, (person_id,))
    
    def get_all_installments(self):
        """جلب جميع الأقساط مع بيانات الزبائن"""
        query = """
            SELECT i.*, p.name, p.phone 
            FROM installments i 
            JOIN persons p ON i.person_id = p.id 
            ORDER BY i.due_date DESC
        """
        return self.db.fetch_all(query)

class InternetSubscription:
    """نموذج اشتراكات الإنترنت"""
    
    def __init__(self, db_manager):
        self.db = db_manager
    
    def add_subscription(self, person_id, plan_name, monthly_cost, start_date, end_date, description=""):
        """إضافة اشتراك إنترنت جديد"""
        query = """
            INSERT INTO internet_subscriptions (person_id, plan_name, monthly_cost, start_date, end_date, description) 
            VALUES (?, ?, ?, ?, ?, ?)
        """
        return self.db.execute_query(query, (person_id, plan_name, monthly_cost, start_date, end_date, description))
    
    def update_subscription(self, subscription_id, plan_name, monthly_cost, start_date, end_date, is_active, description):
        """تعديل اشتراك الإنترنت"""
        query = """
            UPDATE internet_subscriptions 
            SET plan_name=?, monthly_cost=?, start_date=?, end_date=?, is_active=?, description=? 
            WHERE id=?
        """
        return self.db.execute_query(query, (plan_name, monthly_cost, start_date, end_date, is_active, description, subscription_id))
    
    def delete_subscription(self, subscription_id):
        """حذف اشتراك إنترنت"""
        query = "DELETE FROM internet_subscriptions WHERE id=?"
        return self.db.execute_query(query, (subscription_id,))
    
    def get_subscriptions_by_person(self, person_id):
        """جلب اشتراكات زبون معين"""
        query = "SELECT * FROM internet_subscriptions WHERE person_id=? ORDER BY start_date DESC"
        return self.db.fetch_all(query, (person_id,))
    
    def get_all_subscriptions(self):
        """جلب جميع الاشتراكات مع بيانات الزبائن"""
        query = """
            SELECT s.*, p.name, p.phone 
            FROM internet_subscriptions s 
            JOIN persons p ON s.person_id = p.id 
            ORDER BY s.start_date DESC
        """
        return self.db.fetch_all(query)
