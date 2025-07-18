# -*- coding: utf-8 -*-
"""
استعلامات SQL للعمليات CRUD
يحتوي على جميع الاستعلامات المطلوبة للتطبيق
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, date
from .database_connection import DatabaseConnection
from .models import Person, Debt, Installment, InternetSubscription, Payment


class PersonQueries:
    """
    استعلامات خاصة بالزبائن
    """
    
    def __init__(self, db: DatabaseConnection):
        self.db = db
    
    def create_person(self, person: Person) -> Optional[int]:
        """
        إضافة زبون جديد
        """
        query = """
            INSERT INTO persons (name, phone, address, notes)
            VALUES (?, ?, ?, ?)
        """
        return self.db.execute_insert(query, (person.name, person.phone, person.address, person.notes))
    
    def get_all_persons(self) -> List[Person]:
        """
        الحصول على جميع الزبائن
        """
        query = "SELECT * FROM persons ORDER BY name"
        rows = self.db.execute_query(query)
        
        if rows:
            return [Person(
                id=row['id'],
                name=row['name'],
                phone=row['phone'],
                address=row['address'],
                notes=row['notes'],
                created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None
            ) for row in rows]
        return []
    
    def get_person_by_id(self, person_id: int) -> Optional[Person]:
        """
        الحصول على زبون بالمعرف
        """
        query = "SELECT * FROM persons WHERE id = ?"
        rows = self.db.execute_query(query, (person_id,))
        
        if rows:
            row = rows[0]
            return Person(
                id=row['id'],
                name=row['name'],
                phone=row['phone'],
                address=row['address'],
                notes=row['notes'],
                created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None
            )
        return None
    
    def update_person(self, person: Person) -> bool:
        """
        تحديث بيانات زبون
        """
        query = """
            UPDATE persons 
            SET name = ?, phone = ?, address = ?, notes = ?
            WHERE id = ?
        """
        result = self.db.execute_query(query, (person.name, person.phone, person.address, person.notes, person.id))
        return result is not None
    
    def delete_person(self, person_id: int) -> bool:
        """
        حذف زبون
        """
        query = "DELETE FROM persons WHERE id = ?"
        result = self.db.execute_query(query, (person_id,))
        return result is not None
    
    def search_persons(self, search_term: str) -> List[Person]:
        """
        البحث في الزبائن
        """
        query = """
            SELECT * FROM persons 
            WHERE name LIKE ? OR phone LIKE ? OR address LIKE ? OR notes LIKE ?
            ORDER BY name
        """
        search_pattern = f"%{search_term}%"
        rows = self.db.execute_query(query, (search_pattern, search_pattern, search_pattern, search_pattern))
        
        if rows:
            return [Person(
                id=row['id'],
                name=row['name'],
                phone=row['phone'],
                address=row['address'],
                notes=row['notes'],
                created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None
            ) for row in rows]
        return []


class DebtQueries:
    """
    استعلامات خاصة بالديون
    """
    
    def __init__(self, db: DatabaseConnection):
        self.db = db
    
    def create_debt(self, debt: Debt) -> Optional[int]:
        """
        إضافة دين جديد
        """
        query = """
            INSERT INTO debts (person_id, amount, description, due_date, is_paid)
            VALUES (?, ?, ?, ?, ?)
        """
        return self.db.execute_insert(query, (
            debt.person_id, debt.amount, debt.description, 
            debt.due_date.isoformat() if debt.due_date else None, debt.is_paid
        ))
    
    def get_all_debts(self) -> List[Debt]:
        """
        الحصول على جميع الديون مع أسماء الزبائن
        """
        query = """
            SELECT d.*, p.name as person_name
            FROM debts d
            JOIN persons p ON d.person_id = p.id
            ORDER BY d.created_at DESC
        """
        rows = self.db.execute_query(query)
        
        if rows:
            return [Debt(
                id=row['id'],
                person_id=row['person_id'],
                amount=row['amount'],
                description=row['description'],
                due_date=date.fromisoformat(row['due_date']) if row['due_date'] else None,
                is_paid=bool(row['is_paid']),
                created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None,
                person_name=row['person_name']
            ) for row in rows]
        return []
    
    def get_debts_by_person(self, person_id: int) -> List[Debt]:
        """
        الحصول على ديون زبون معين
        """
        query = """
            SELECT d.*, p.name as person_name
            FROM debts d
            JOIN persons p ON d.person_id = p.id
            WHERE d.person_id = ?
            ORDER BY d.created_at DESC
        """
        rows = self.db.execute_query(query, (person_id,))
        
        if rows:
            return [Debt(
                id=row['id'],
                person_id=row['person_id'],
                amount=row['amount'],
                description=row['description'],
                due_date=date.fromisoformat(row['due_date']) if row['due_date'] else None,
                is_paid=bool(row['is_paid']),
                created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None,
                person_name=row['person_name']
            ) for row in rows]
        return []
    
    def update_debt(self, debt: Debt) -> bool:
        """
        تحديث دين
        """
        query = """
            UPDATE debts 
            SET amount = ?, description = ?, due_date = ?, is_paid = ?
            WHERE id = ?
        """
        result = self.db.execute_query(query, (
            debt.amount, debt.description, 
            debt.due_date.isoformat() if debt.due_date else None, 
            debt.is_paid, debt.id
        ))
        return result is not None
    
    def delete_debt(self, debt_id: int) -> bool:
        """
        حذف دين
        """
        query = "DELETE FROM debts WHERE id = ?"
        result = self.db.execute_query(query, (debt_id,))
        return result is not None


class InstallmentQueries:
    """
    استعلامات خاصة بالأقساط
    """
    
    def __init__(self, db: DatabaseConnection):
        self.db = db
    
    def create_installment(self, installment: Installment) -> Optional[int]:
        """
        إضافة قسط جديد
        """
        query = """
            INSERT INTO installments (person_id, total_amount, paid_amount, installment_amount, 
                                    frequency, description, start_date, end_date, is_completed)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        return self.db.execute_insert(query, (
            installment.person_id, installment.total_amount, installment.paid_amount,
            installment.installment_amount, installment.frequency, installment.description,
            installment.start_date.isoformat() if installment.start_date else None,
            installment.end_date.isoformat() if installment.end_date else None,
            installment.is_completed
        ))
    
    def get_all_installments(self) -> List[Installment]:
        """
        الحصول على جميع الأقساط مع أسماء الزبائن
        """
        query = """
            SELECT i.*, p.name as person_name
            FROM installments i
            JOIN persons p ON i.person_id = p.id
            ORDER BY i.created_at DESC
        """
        rows = self.db.execute_query(query)
        
        if rows:
            return [Installment(
                id=row['id'],
                person_id=row['person_id'],
                total_amount=row['total_amount'],
                paid_amount=row['paid_amount'],
                installment_amount=row['installment_amount'],
                frequency=row['frequency'],
                description=row['description'],
                start_date=date.fromisoformat(row['start_date']) if row['start_date'] else None,
                end_date=date.fromisoformat(row['end_date']) if row['end_date'] else None,
                is_completed=bool(row['is_completed']),
                created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None,
                person_name=row['person_name']
            ) for row in rows]
        return []
    
    def get_installments_by_person(self, person_id: int) -> List[Installment]:
        """
        الحصول على أقساط زبون معين
        """
        query = """
            SELECT i.*, p.name as person_name
            FROM installments i
            JOIN persons p ON i.person_id = p.id
            WHERE i.person_id = ?
            ORDER BY i.created_at DESC
        """
        rows = self.db.execute_query(query, (person_id,))
        
        if rows:
            return [Installment(
                id=row['id'],
                person_id=row['person_id'],
                total_amount=row['total_amount'],
                paid_amount=row['paid_amount'],
                installment_amount=row['installment_amount'],
                frequency=row['frequency'],
                description=row['description'],
                start_date=date.fromisoformat(row['start_date']) if row['start_date'] else None,
                end_date=date.fromisoformat(row['end_date']) if row['end_date'] else None,
                is_completed=bool(row['is_completed']),
                created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None,
                person_name=row['person_name']
            ) for row in rows]
        return []

    def get_installment_by_id(self, installment_id: int) -> Optional[Installment]:
        """
        الحصول على قسط بالمعرف
        """
        query = """
            SELECT i.*, p.name as person_name
            FROM installments i
            JOIN persons p ON i.person_id = p.id
            WHERE i.id = ?
        """
        rows = self.db.execute_query(query, (installment_id,))
        
        if rows:
            row = rows[0]
            return Installment(
                id=row['id'],
                person_id=row['person_id'],
                total_amount=row['total_amount'],
                paid_amount=row['paid_amount'],
                installment_amount=row['installment_amount'],
                frequency=row['frequency'],
                description=row['description'],
                start_date=date.fromisoformat(row['start_date']) if row['start_date'] else None,
                end_date=date.fromisoformat(row['end_date']) if row['end_date'] else None,
                is_completed=bool(row['is_completed']),
                created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None,
                person_name=row['person_name']
            )
        return None
    
    def update_installment(self, installment: Installment) -> bool:
        """
        تحديث قسط
        """
        query = """
            UPDATE installments 
            SET total_amount = ?, paid_amount = ?, installment_amount = ?, 
                frequency = ?, description = ?, start_date = ?, end_date = ?, is_completed = ?
            WHERE id = ?
        """
        result = self.db.execute_query(query, (
            installment.total_amount, installment.paid_amount, installment.installment_amount,
            installment.frequency, installment.description,
            installment.start_date.isoformat() if installment.start_date else None,
            installment.end_date.isoformat() if installment.end_date else None,
            installment.is_completed, installment.id
        ))
        return result is not None

    def update_installment_amounts(self, installment_id: int):
        """
        تحديث المبالغ المدفوعة والمتبقية للقسط
        """
        # حساب مجموع الدفعات
        payments_sum = self.db.execute_query("SELECT SUM(amount) as total FROM payments WHERE installment_id = ?", (installment_id,))[0]['total'] or 0
        
        # الحصول على المبلغ الإجمالي للقسط
        installment_total = self.db.execute_query("SELECT total_amount FROM installments WHERE id = ?", (installment_id,))[0]['total_amount']
        
        # تحديث القسط
        is_completed = payments_sum >= installment_total
        query = "UPDATE installments SET paid_amount = ?, is_completed = ? WHERE id = ?"
        self.db.execute_query(query, (payments_sum, is_completed, installment_id))
    
    def delete_installment(self, installment_id: int) -> bool:
        """
        حذف قسط
        """
        query = "DELETE FROM installments WHERE id = ?"
        result = self.db.execute_query(query, (installment_id,))
        return result is not None


class InternetSubscriptionQueries:
    """
    استعلامات خاصة باشتراكات الإنترنت
    """
    
    def __init__(self, db: DatabaseConnection):
        self.db = db
    
    def create_subscription(self, subscription: InternetSubscription) -> Optional[int]:
        """
        إضافة اشتراك جديد
        """
        query = """
            INSERT INTO internet_subscriptions (person_id, plan_name, monthly_fee, 
                                               start_date, end_date, is_active)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        return self.db.execute_insert(query, (
            subscription.person_id, subscription.plan_name, subscription.monthly_fee,
            subscription.start_date.isoformat() if subscription.start_date else None,
            subscription.end_date.isoformat() if subscription.end_date else None,
            subscription.is_active
        ))
    
    def get_all_subscriptions(self) -> List[InternetSubscription]:
        """
        الحصول على جميع الاشتراكات مع أسماء الزبائن
        """
        query = """
            SELECT s.id, s.person_id, s.plan_name, s.monthly_fee, s.start_date, s.end_date, s.is_active, s.created_at, s.updated_at, p.name as person_name
            FROM internet_subscriptions s
            JOIN persons p ON s.person_id = p.id
            ORDER BY s.created_at DESC
        """
        rows = self.db.execute_query(query)
        
        if rows:
            return [InternetSubscription(
                id=row['id'],
                person_id=row['person_id'],
                plan_name=row['plan_name'],
                monthly_fee=row['monthly_fee'],
                start_date=date.fromisoformat(row['start_date']) if row['start_date'] else None,
                end_date=date.fromisoformat(row['end_date']) if row['end_date'] else None,
                is_active=bool(row['is_active']),
                created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None,
                updated_at=datetime.fromisoformat(row['updated_at']) if row['updated_at'] else None,
                person_name=row['person_name']
            ) for row in rows]
        return []
    
    def get_subscriptions_by_person(self, person_id: int) -> List[InternetSubscription]:
        """
        الحصول على اشتراكات زبون معين
        """
        query = """
            SELECT s.id, s.person_id, s.plan_name, s.monthly_fee, s.start_date, s.end_date, s.is_active, s.created_at, s.updated_at, p.name as person_name
            FROM internet_subscriptions s
            JOIN persons p ON s.person_id = p.id
            WHERE s.person_id = ?
            ORDER BY s.created_at DESC
        """
        rows = self.db.execute_query(query, (person_id,))
        
        if rows:
            return [InternetSubscription(
                id=row['id'],
                person_id=row['person_id'],
                plan_name=row['plan_name'],
                monthly_fee=row['monthly_fee'],
                start_date=date.fromisoformat(row['start_date']) if row['start_date'] else None,
                end_date=date.fromisoformat(row['end_date']) if row['end_date'] else None,
                is_active=bool(row['is_active']),
                created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None,
                updated_at=datetime.fromisoformat(row['updated_at']) if row['updated_at'] else None,
                person_name=row['person_name']
            ) for row in rows]
        return []
    
    def update_subscription(self, subscription: InternetSubscription) -> bool:
        """
        تحديث اشتراك
        """
        query = """
            UPDATE internet_subscriptions 
            SET plan_name = ?, monthly_fee = ?, 
                start_date = ?, end_date = ?, is_active = ?
            WHERE id = ?
        """
        result = self.db.execute_query(query, (
            subscription.plan_name, subscription.monthly_fee,
            subscription.start_date.isoformat() if subscription.start_date else None,
            subscription.end_date.isoformat() if subscription.end_date else None,
            subscription.is_active, subscription.id
        ))
        return result is not None
    
    def delete_subscription(self, subscription_id: int) -> bool:
        """
        حذف اشتراك
        """
        query = "DELETE FROM internet_subscriptions WHERE id = ?"
        result = self.db.execute_query(query, (subscription_id,))
        return result is not None


class PaymentQueries:
    """
    استعلامات خاصة بالدفعات
    """

    def __init__(self, db: DatabaseConnection):
        self.db = db

    def create_payment(self, payment: Payment) -> Optional[int]:
        """
        إضافة دفعة جديدة
        """
        query = """
            INSERT INTO payments (installment_id, amount, payment_date)
            VALUES (?, ?, ?)
        """
        payment_id = self.db.execute_insert(query, (
            payment.installment_id, payment.amount,
            payment.payment_date.isoformat() if payment.payment_date else None
        ))
        if payment_id:
            InstallmentQueries(self.db).update_installment_amounts(payment.installment_id)
        return payment_id

    def get_payments_by_installment(self, installment_id: int) -> List[Payment]:
        """
        الحصول على دفعات قسط معين
        """
        query = """
            SELECT * FROM payments
            WHERE installment_id = ?
            ORDER BY payment_date DESC
        """
        rows = self.db.execute_query(query, (installment_id,))

        if rows:
            return [Payment(
                id=row['id'],
                installment_id=row['installment_id'],
                amount=row['amount'],
                payment_date=date.fromisoformat(row['payment_date']) if row['payment_date'] else None,
                created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None
            ) for row in rows]
        return []

    def get_payment_by_id(self, payment_id: int) -> Optional[Payment]:
        """
        الحصول على دفعة بالمعرف
        """
        query = "SELECT * FROM payments WHERE id = ?"
        rows = self.db.execute_query(query, (payment_id,))
        if rows:
            row = rows[0]
            return Payment(
                id=row['id'],
                installment_id=row['installment_id'],
                amount=row['amount'],
                payment_date=date.fromisoformat(row['payment_date']) if row['payment_date'] else None,
                created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None
            )
        return None

    def delete_payment(self, payment_id: int) -> bool:
        """
        حذف دفعة
        """
        payment = self.get_payment_by_id(payment_id)
        if not payment:
            return False

        query = "DELETE FROM payments WHERE id = ?"
        result = self.db.execute_query(query, (payment_id,))
        if result is not None:
            InstallmentQueries(self.db).update_installment_amounts(payment.installment_id)
            return True
        return False
