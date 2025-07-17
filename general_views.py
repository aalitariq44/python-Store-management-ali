# الواجهات العامة - General Views
# نوافذ عرض جميع البيانات في النظام (الديون، الأقساط، اشتراكات الإنترنت)

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from dialogs import DebtDialog, InstallmentDialog, SubscriptionDialog
from models import Debt, Installment, InternetSubscription, Person

class AllDebtsWindow(QMainWindow):
    """نافذة عرض جميع الديون في النظام"""
    
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.debt_model = Debt(db_manager)
        self.person_model = Person(db_manager)
        
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        """تهيئة واجهة المستخدم"""
        self.setWindowTitle("جميع الديون")
        self.setGeometry(100, 100, 1200, 700)
        
        # تطبيق تصميم عصري
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2E2E2E;
            }
            QWidget {
                background-color: #3C3C3C;
                color: #F0F0F0;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
            }
            QLabel {
                font-size: 14px;
            }
            QLineEdit {
                background-color: #505050;
                border: 1px solid #707070;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton {
                background-color: #5A9B5A;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #6BBF6B;
            }
            QPushButton:pressed {
                background-color: #4A8B4A;
            }
            QTableWidget {
                background-color: #505050;
                border: 1px solid #707070;
                gridline-color: #707070;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #5A9B5A;
                color: white;
                padding: 8px;
                border: 1px solid #707070;
                font-size: 16px;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QTableWidget::item:selected {
                background-color: #5A9B5A;
                color: white;
            }
            QTableWidget::alternating-row-color {
                background-color: #5A5A5A;
            }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # شريط البحث والأدوات
        toolbar_layout = QHBoxLayout()
        
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("البحث باسم الزبون, الوصف, أو الهاتف...")
        self.search_button = QPushButton("بحث")
        self.refresh_button = QPushButton("تحديث")
        self.add_button = QPushButton("إضافة دين جديد")
        self.edit_button = QPushButton("تعديل المحدد")
        self.delete_button = QPushButton("حذف المحدد")
        
        toolbar_layout.addWidget(QLabel("البحث:"))
        toolbar_layout.addWidget(self.search_edit)
        toolbar_layout.addWidget(self.search_button)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.add_button)
        toolbar_layout.addWidget(self.edit_button)
        toolbar_layout.addWidget(self.delete_button)
        toolbar_layout.addWidget(self.refresh_button)
        
        layout.addLayout(toolbar_layout)
        
        # جدول البيانات
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "المعرف", "اسم الزبون", "الهاتف", "المبلغ", "الوصف", "التاريخ", "حالة السداد"
        ])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        
        layout.addWidget(self.table)
        
        # ربط الأحداث
        self.search_button.clicked.connect(self.search_data)
        self.search_edit.returnPressed.connect(self.search_data)
        self.refresh_button.clicked.connect(self.load_data)
        self.add_button.clicked.connect(self.add_debt)
        self.edit_button.clicked.connect(self.edit_debt)
        self.delete_button.clicked.connect(self.delete_debt)
        
        central_widget.setLayout(layout)
    
    def load_data(self):
        """تحميل جميع الديون"""
        debts = self.debt_model.get_all_debts()
        self.populate_table(debts)
    
    def search_data(self):
        """البحث في الديون"""
        search_term = self.search_edit.text().strip()
        if search_term:
            # البحث في اسم الزبون والوصف
            query = """
                SELECT d.*, p.name, p.phone 
                FROM debts d 
                JOIN persons p ON d.person_id = p.id 
                WHERE p.name LIKE ? OR d.description LIKE ? OR p.phone LIKE ?
                ORDER BY d.debt_date DESC
            """
            search_pattern = f"%{search_term}%"
            debts = self.db_manager.fetch_all(query, (search_pattern, search_pattern, search_pattern))
            self.populate_table(debts)
        else:
            self.load_data()
    
    def populate_table(self, debts):
        """ملء الجدول بالبيانات"""
        self.table.setRowCount(len(debts))
        
        for row, debt in enumerate(debts):
            self.table.setItem(row, 0, QTableWidgetItem(str(debt[0])))
            self.table.setItem(row, 1, QTableWidgetItem(debt[6]))  # name
            self.table.setItem(row, 2, QTableWidgetItem(debt[7] or ""))  # phone
            self.table.setItem(row, 3, QTableWidgetItem(f"{debt[2]:.2f} ريال"))
            self.table.setItem(row, 4, QTableWidgetItem(debt[3] or ""))
            self.table.setItem(row, 5, QTableWidgetItem(debt[4]))
            self.table.setItem(row, 6, QTableWidgetItem("مدفوع" if debt[5] else "غير مدفوع"))
    
    def add_debt(self):
        """إضافة دين جديد"""
        # اختيار الزبون أولاً
        persons = self.person_model.get_all_persons()
        if not persons:
            QMessageBox.warning(self, "تحذير", "لا يوجد زبائن في النظام. يرجى إضافة زبون أولاً.")
            return
        
        person_names = [f"{p[1]} - {p[2] or 'بدون هاتف'}" for p in persons]
        person_name, ok = QInputDialog.getItem(self, "اختيار الزبون", "اختر الزبون:", person_names, 0, False)
        
        if ok and person_name:
            person_index = person_names.index(person_name)
            person_id = persons[person_index][0]
            
            dialog = DebtDialog(self)
            if dialog.exec_() == QDialog.Accepted:
                data = dialog.get_data()
                self.debt_model.add_debt(person_id, data['amount'], data['description'])
                self.load_data()
                QMessageBox.information(self, "نجح", "تم إضافة الدين بنجاح")
    
    def edit_debt(self):
        """تعديل دين موجود"""
        current_row = self.table.currentRow()
        if current_row >= 0:
            debt_id = int(self.table.item(current_row, 0).text())
            debts = self.debt_model.get_all_debts()
            debt_data = next((d for d in debts if d[0] == debt_id), None)
            
            if debt_data:
                dialog = DebtDialog(self, debt_data)
                if dialog.exec_() == QDialog.Accepted:
                    data = dialog.get_data()
                    self.debt_model.update_debt(debt_id, data['amount'], data['description'], data['is_paid'])
                    self.load_data()
                    QMessageBox.information(self, "نجح", "تم تعديل الدين بنجاح")
        else:
            QMessageBox.warning(self, "تحذير", "يرجى اختيار دين للتعديل")
    
    def delete_debt(self):
        """حذف دين"""
        current_row = self.table.currentRow()
        if current_row >= 0:
            debt_id = int(self.table.item(current_row, 0).text())
            reply = QMessageBox.question(self, "تأكيد الحذف", "هل أنت متأكد من حذف هذا الدين؟")
            if reply == QMessageBox.Yes:
                self.debt_model.delete_debt(debt_id)
                self.load_data()
                QMessageBox.information(self, "نجح", "تم حذف الدين بنجاح")
        else:
            QMessageBox.warning(self, "تحذير", "يرجى اختيار دين للحذف")

class AllInstallmentsWindow(QMainWindow):
    """نافذة عرض جميع الأقساط في النظام"""
    
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.installment_model = Installment(db_manager)
        self.person_model = Person(db_manager)
        
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        """تهيئة واجهة المستخدم"""
        self.setWindowTitle("جميع الأقساط")
        self.setGeometry(100, 100, 1400, 700)

        # تطبيق تصميم عصري
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2E2E2E;
            }
            QWidget {
                background-color: #3C3C3C;
                color: #F0F0F0;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
            }
            QLabel {
                font-size: 14px;
            }
            QLineEdit {
                background-color: #505050;
                border: 1px solid #707070;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton {
                background-color: #5A9B5A;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #6BBF6B;
            }
            QPushButton:pressed {
                background-color: #4A8B4A;
            }
            QTableWidget {
                background-color: #505050;
                border: 1px solid #707070;
                gridline-color: #707070;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #5A9B5A;
                color: white;
                padding: 8px;
                border: 1px solid #707070;
                font-size: 16px;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QTableWidget::item:selected {
                background-color: #5A9B5A;
                color: white;
            }
            QTableWidget::alternating-row-color {
                background-color: #5A5A5A;
            }
        """)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # شريط البحث والأدوات
        toolbar_layout = QHBoxLayout()
        
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("البحث باسم الزبون, الوصف, أو الهاتف...")
        self.search_button = QPushButton("بحث")
        self.refresh_button = QPushButton("تحديث")
        self.add_button = QPushButton("إضافة قسط جديد")
        self.edit_button = QPushButton("تعديل المحدد")
        self.delete_button = QPushButton("حذف المحدد")
        
        toolbar_layout.addWidget(QLabel("البحث:"))
        toolbar_layout.addWidget(self.search_edit)
        toolbar_layout.addWidget(self.search_button)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.add_button)
        toolbar_layout.addWidget(self.edit_button)
        toolbar_layout.addWidget(self.delete_button)
        toolbar_layout.addWidget(self.refresh_button)
        
        layout.addLayout(toolbar_layout)
        
        # جدول البيانات
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "المعرف", "اسم الزبون", "الهاتف", "المبلغ الإجمالي", "المدفوع", "مبلغ القسط", "تاريخ الاستحقاق", "الوصف", "مكتمل"
        ])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        
        layout.addWidget(self.table)
        
        # ربط الأحداث
        self.search_button.clicked.connect(self.search_data)
        self.search_edit.returnPressed.connect(self.search_data)
        self.refresh_button.clicked.connect(self.load_data)
        self.add_button.clicked.connect(self.add_installment)
        self.edit_button.clicked.connect(self.edit_installment)
        self.delete_button.clicked.connect(self.delete_installment)
        
        central_widget.setLayout(layout)
    
    def load_data(self):
        """تحميل جميع الأقساط"""
        installments = self.installment_model.get_all_installments()
        self.populate_table(installments)
    
    def search_data(self):
        """البحث في الأقساط"""
        search_term = self.search_edit.text().strip()
        if search_term:
            query = """
                SELECT i.*, p.name, p.phone 
                FROM installments i 
                JOIN persons p ON i.person_id = p.id 
                WHERE p.name LIKE ? OR i.description LIKE ? OR p.phone LIKE ?
                ORDER BY i.due_date DESC
            """
            search_pattern = f"%{search_term}%"
            installments = self.db_manager.fetch_all(query, (search_pattern, search_pattern, search_pattern))
            self.populate_table(installments)
        else:
            self.load_data()
    
    def populate_table(self, installments):
        """ملء الجدول بالبيانات"""
        self.table.setRowCount(len(installments))
        
        for row, installment in enumerate(installments):
            self.table.setItem(row, 0, QTableWidgetItem(str(installment[0])))
            self.table.setItem(row, 1, QTableWidgetItem(installment[8]))  # name
            self.table.setItem(row, 2, QTableWidgetItem(installment[9] or ""))  # phone
            self.table.setItem(row, 3, QTableWidgetItem(f"{installment[2]:.2f} ريال"))
            self.table.setItem(row, 4, QTableWidgetItem(f"{installment[3]:.2f} ريال"))
            self.table.setItem(row, 5, QTableWidgetItem(f"{installment[4]:.2f} ريال"))
            self.table.setItem(row, 6, QTableWidgetItem(installment[5] or ""))
            self.table.setItem(row, 7, QTableWidgetItem(installment[6] or ""))
            self.table.setItem(row, 8, QTableWidgetItem("مكتمل" if installment[7] else "غير مكتمل"))
    
    def add_installment(self):
        """إضافة قسط جديد"""
        persons = self.person_model.get_all_persons()
        if not persons:
            QMessageBox.warning(self, "تحذير", "لا يوجد زبائن في النظام. يرجى إضافة زبون أولاً.")
            return
        
        person_names = [f"{p[1]} - {p[2] or 'بدون هاتف'}" for p in persons]
        person_name, ok = QInputDialog.getItem(self, "اختيار الزبون", "اختر الزبون:", person_names, 0, False)
        
        if ok and person_name:
            person_index = person_names.index(person_name)
            person_id = persons[person_index][0]
            
            dialog = InstallmentDialog(self)
            if dialog.exec_() == QDialog.Accepted:
                data = dialog.get_data()
                self.installment_model.add_installment(
                    person_id,
                    data['total_amount'],
                    data['installment_amount'],
                    data['due_date'],
                    data['description']
                )
                self.load_data()
                QMessageBox.information(self, "نجح", "تم إضافة القسط بنجاح")
    
    def edit_installment(self):
        """تعديل قسط موجود"""
        current_row = self.table.currentRow()
        if current_row >= 0:
            installment_id = int(self.table.item(current_row, 0).text())
            installments = self.installment_model.get_all_installments()
            installment_data = next((i for i in installments if i[0] == installment_id), None)
            
            if installment_data:
                dialog = InstallmentDialog(self, installment_data)
                if dialog.exec_() == QDialog.Accepted:
                    data = dialog.get_data()
                    self.installment_model.update_installment(
                        installment_id,
                        data['total_amount'],
                        data['paid_amount'],
                        data['installment_amount'],
                        data['due_date'],
                        data['description'],
                        data['is_completed']
                    )
                    self.load_data()
                    QMessageBox.information(self, "نجح", "تم تعديل القسط بنجاح")
        else:
            QMessageBox.warning(self, "تحذير", "يرجى اختيار قسط للتعديل")
    
    def delete_installment(self):
        """حذف قسط"""
        current_row = self.table.currentRow()
        if current_row >= 0:
            installment_id = int(self.table.item(current_row, 0).text())
            reply = QMessageBox.question(self, "تأكيد الحذف", "هل أنت متأكد من حذف هذا القسط؟")
            if reply == QMessageBox.Yes:
                self.installment_model.delete_installment(installment_id)
                self.load_data()
                QMessageBox.information(self, "نجح", "تم حذف القسط بنجاح")
        else:
            QMessageBox.warning(self, "تحذير", "يرجى اختيار قسط للحذف")

class AllSubscriptionsWindow(QMainWindow):
    """نافذة عرض جميع اشتراكات الإنترنت في النظام"""
    
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.subscription_model = InternetSubscription(db_manager)
        self.person_model = Person(db_manager)
        
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        """تهيئة واجهة المستخدم"""
        self.setWindowTitle("جميع اشتراكات الإنترنت")
        self.setGeometry(100, 100, 1400, 700)
        
        # تطبيق تصميم عصري
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2E2E2E;
            }
            QWidget {
                background-color: #3C3C3C;
                color: #F0F0F0;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
            }
            QLabel {
                font-size: 14px;
            }
            QLineEdit {
                background-color: #505050;
                border: 1px solid #707070;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton {
                background-color: #5A9B5A;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #6BBF6B;
            }
            QPushButton:pressed {
                background-color: #4A8B4A;
            }
            QTableWidget {
                background-color: #505050;
                border: 1px solid #707070;
                gridline-color: #707070;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #5A9B5A;
                color: white;
                padding: 8px;
                border: 1px solid #707070;
                font-size: 16px;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QTableWidget::item:selected {
                background-color: #5A9B5A;
                color: white;
            }
            QTableWidget::alternating-row-color {
                background-color: #5A5A5A;
            }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # شريط البحث والأدوات
        toolbar_layout = QHBoxLayout()
        
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("البحث باسم الزبون, الخطة, أو الهاتف...")
        self.search_button = QPushButton("بحث")
        self.refresh_button = QPushButton("تحديث")
        self.add_button = QPushButton("إضافة اشتراك جديد")
        self.edit_button = QPushButton("تعديل المحدد")
        self.delete_button = QPushButton("حذف المحدد")
        
        toolbar_layout.addWidget(QLabel("البحث:"))
        toolbar_layout.addWidget(self.search_edit)
        toolbar_layout.addWidget(self.search_button)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.add_button)
        toolbar_layout.addWidget(self.edit_button)
        toolbar_layout.addWidget(self.delete_button)
        toolbar_layout.addWidget(self.refresh_button)
        
        layout.addLayout(toolbar_layout)
        
        # جدول البيانات
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "المعرف", "اسم الزبون", "الهاتف", "اسم الخطة", "التكلفة الشهرية", "تاريخ البداية", "تاريخ النهاية", "نشط", "الوصف"
        ])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        
        layout.addWidget(self.table)
        
        # ربط الأحداث
        self.search_button.clicked.connect(self.search_data)
        self.search_edit.returnPressed.connect(self.search_data)
        self.refresh_button.clicked.connect(self.load_data)
        self.add_button.clicked.connect(self.add_subscription)
        self.edit_button.clicked.connect(self.edit_subscription)
        self.delete_button.clicked.connect(self.delete_subscription)
        
        central_widget.setLayout(layout)
    
    def load_data(self):
        """تحميل جميع الاشتراكات"""
        subscriptions = self.subscription_model.get_all_subscriptions()
        self.populate_table(subscriptions)
    
    def search_data(self):
        """البحث في الاشتراكات"""
        search_term = self.search_edit.text().strip()
        if search_term:
            query = """
                SELECT s.*, p.name, p.phone 
                FROM internet_subscriptions s 
                JOIN persons p ON s.person_id = p.id 
                WHERE p.name LIKE ? OR s.plan_name LIKE ? OR s.description LIKE ? OR p.phone LIKE ?
                ORDER BY s.start_date DESC
            """
            search_pattern = f"%{search_term}%"
            subscriptions = self.db_manager.fetch_all(query, (search_pattern, search_pattern, search_pattern, search_pattern))
            self.populate_table(subscriptions)
        else:
            self.load_data()
    
    def populate_table(self, subscriptions):
        """ملء الجدول بالبيانات"""
        self.table.setRowCount(len(subscriptions))
        
        for row, subscription in enumerate(subscriptions):
            self.table.setItem(row, 0, QTableWidgetItem(str(subscription[0])))
            self.table.setItem(row, 1, QTableWidgetItem(subscription[8]))  # name
            self.table.setItem(row, 2, QTableWidgetItem(subscription[9] or ""))  # phone
            self.table.setItem(row, 3, QTableWidgetItem(subscription[2]))
            self.table.setItem(row, 4, QTableWidgetItem(f"{subscription[3]:.2f} ريال"))
            self.table.setItem(row, 5, QTableWidgetItem(subscription[4] or ""))
            self.table.setItem(row, 6, QTableWidgetItem(subscription[5] or ""))
            self.table.setItem(row, 7, QTableWidgetItem("نشط" if subscription[6] else "غير نشط"))
            self.table.setItem(row, 8, QTableWidgetItem(subscription[7] or ""))
    
    def add_subscription(self):
        """إضافة اشتراك جديد"""
        persons = self.person_model.get_all_persons()
        if not persons:
            QMessageBox.warning(self, "تحذير", "لا يوجد زبائن في النظام. يرجى إضافة زبون أولاً.")
            return
        
        person_names = [f"{p[1]} - {p[2] or 'بدون هاتف'}" for p in persons]
        person_name, ok = QInputDialog.getItem(self, "اختيار الزبون", "اختر الزبون:", person_names, 0, False)
        
        if ok and person_name:
            person_index = person_names.index(person_name)
            person_id = persons[person_index][0]
            
            dialog = SubscriptionDialog(self)
            if dialog.exec_() == QDialog.Accepted:
                data = dialog.get_data()
                self.subscription_model.add_subscription(
                    person_id,
                    data['plan_name'],
                    data['monthly_cost'],
                    data['start_date'],
                    data['end_date'],
                    data['description']
                )
                self.load_data()
                QMessageBox.information(self, "نجح", "تم إضافة الاشتراك بنجاح")
    
    def edit_subscription(self):
        """تعديل اشتراك موجود"""
        current_row = self.table.currentRow()
        if current_row >= 0:
            subscription_id = int(self.table.item(current_row, 0).text())
            subscriptions = self.subscription_model.get_all_subscriptions()
            subscription_data = next((s for s in subscriptions if s[0] == subscription_id), None)
            
            if subscription_data:
                dialog = SubscriptionDialog(self, subscription_data)
                if dialog.exec_() == QDialog.Accepted:
                    data = dialog.get_data()
                    self.subscription_model.update_subscription(
                        subscription_id,
                        data['plan_name'],
                        data['monthly_cost'],
                        data['start_date'],
                        data['end_date'],
                        data['is_active'],
                        data['description']
                    )
                    self.load_data()
                    QMessageBox.information(self, "نجح", "تم تعديل الاشتراك بنجاح")
        else:
            QMessageBox.warning(self, "تحذير", "يرجى اختيار اشتراك للتعديل")
    
    def delete_subscription(self):
        """حذف اشتراك"""
        current_row = self.table.currentRow()
        if current_row >= 0:
            subscription_id = int(self.table.item(current_row, 0).text())
            reply = QMessageBox.question(self, "تأكيد الحذف", "هل أنت متأكد من حذف هذا الاشتراك؟")
            if reply == QMessageBox.Yes:
                self.subscription_model.delete_subscription(subscription_id)
                self.load_data()
                QMessageBox.information(self, "نجح", "تم حذف الاشتراك بنجاح")
        else:
            QMessageBox.warning(self, "تحذير", "يرجى اختيار اشتراك للحذف")
