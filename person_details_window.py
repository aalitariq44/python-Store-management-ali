# نافذة تفاصيل الزبون - Customer Details Window
# تعرض جميع بيانات الزبون مع تبويبات للديون والأقساط والاشتراكات

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from dialogs import DebtDialog, InstallmentDialog, SubscriptionDialog
from models import Debt, Installment, InternetSubscription

class PersonDetailsWindow(QDialog):
    """نافذة تفاصيل الزبون مع تبويبات لجميع البيانات المرتبطة"""
    
    def __init__(self, person_data, db_manager, parent=None):
        super().__init__(parent)
        self.person_data = person_data
        self.db_manager = db_manager
        self.debt_model = Debt(db_manager)
        self.installment_model = Installment(db_manager)
        self.subscription_model = InternetSubscription(db_manager)
        
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        """تهيئة واجهة المستخدم"""
        self.setWindowTitle(f"تفاصيل الزبون: {self.person_data[1]}")
        self.setGeometry(100, 100, 1100, 700)

        # تطبيق تصميم عصري
        self.setStyleSheet("""
            QDialog {
                background-color: #2E2E2E;
            }
            QWidget {
                background-color: #3C3C3C;
                color: #F0F0F0;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
            }
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                border: 1px solid #5A9B5A;
                border-radius: 5px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 10px;
            }
            QLabel {
                font-size: 14px;
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
            QTabWidget::pane {
                border: 1px solid #5A9B5A;
                border-radius: 5px;
            }
            QTabBar::tab {
                background-color: #505050;
                color: #F0F0F0;
                padding: 10px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                font-size: 14px;
            }
            QTabBar::tab:selected {
                background-color: #5A9B5A;
                color: white;
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
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # معلومات الزبون
        info_group = QGroupBox("معلومات الزبون")
        info_layout = QGridLayout()
        info_layout.setSpacing(10)
        
        info_layout.addWidget(QLabel("<b>الاسم:</b>"), 0, 0)
        info_layout.addWidget(QLabel(self.person_data[1]), 0, 1)
        
        info_layout.addWidget(QLabel("<b>الهاتف:</b>"), 1, 0)
        info_layout.addWidget(QLabel(self.person_data[2] or "غير محدد"), 1, 1)
        
        info_layout.addWidget(QLabel("<b>العنوان:</b>"), 2, 0)
        info_layout.addWidget(QLabel(self.person_data[3] or "غير محدد"), 2, 1)
        
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        # التبويبات
        self.tab_widget = QTabWidget()
        self.tab_widget.setFont(QFont("Segoe UI", 12))
        
        # تبويب الديون
        self.debts_tab = self.create_debts_tab()
        self.tab_widget.addTab(self.debts_tab, "الديون")
        
        # تبويب الأقساط
        self.installments_tab = self.create_installments_tab()
        self.tab_widget.addTab(self.installments_tab, "الأقساط")
        
        # تبويب اشتراكات الإنترنت
        self.subscriptions_tab = self.create_subscriptions_tab()
        self.tab_widget.addTab(self.subscriptions_tab, "اشتراكات الإنترنت")
        
        layout.addWidget(self.tab_widget)
        
        # زر الإغلاق
        close_button = QPushButton("إغلاق")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)
        
        self.setLayout(layout)
    
    def create_debts_tab(self):
        """إنشاء تبويب الديون"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # أزرار الإدارة
        button_layout = QHBoxLayout()
        self.add_debt_btn = QPushButton("إضافة دين")
        self.edit_debt_btn = QPushButton("تعديل")
        self.delete_debt_btn = QPushButton("حذف")
        
        button_layout.addWidget(self.add_debt_btn)
        button_layout.addWidget(self.edit_debt_btn)
        button_layout.addWidget(self.delete_debt_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        # جدول الديون
        self.debts_table = QTableWidget()
        self.debts_table.setColumnCount(5)
        self.debts_table.setHorizontalHeaderLabels(["المعرف", "المبلغ", "الوصف", "التاريخ", "حالة السداد"])
        self.debts_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.debts_table.setAlternatingRowColors(True)
        self.debts_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.debts_table.verticalHeader().setVisible(False)
        
        layout.addWidget(self.debts_table)
        
        # ربط الأزرار
        self.add_debt_btn.clicked.connect(self.add_debt)
        self.edit_debt_btn.clicked.connect(self.edit_debt)
        self.delete_debt_btn.clicked.connect(self.delete_debt)
        
        widget.setLayout(layout)
        return widget
    
    def create_installments_tab(self):
        """إنشاء تبويب الأقساط"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # أزرار الإدارة
        button_layout = QHBoxLayout()
        self.add_installment_btn = QPushButton("إضافة قسط")
        self.edit_installment_btn = QPushButton("تعديل")
        self.delete_installment_btn = QPushButton("حذف")
        
        button_layout.addWidget(self.add_installment_btn)
        button_layout.addWidget(self.edit_installment_btn)
        button_layout.addWidget(self.delete_installment_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        # جدول الأقساط
        self.installments_table = QTableWidget()
        self.installments_table.setColumnCount(7)
        self.installments_table.setHorizontalHeaderLabels(["المعرف", "المبلغ الإجمالي", "المدفوع", "مبلغ القسط", "تاريخ الاستحقاق", "الوصف", "مكتمل"])
        self.installments_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.installments_table.setAlternatingRowColors(True)
        self.installments_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.installments_table.verticalHeader().setVisible(False)
        
        layout.addWidget(self.installments_table)
        
        # ربط الأزرار
        self.add_installment_btn.clicked.connect(self.add_installment)
        self.edit_installment_btn.clicked.connect(self.edit_installment)
        self.delete_installment_btn.clicked.connect(self.delete_installment)
        
        widget.setLayout(layout)
        return widget
    
    def create_subscriptions_tab(self):
        """إنشاء تبويب اشتراكات الإنترنت"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # أزرار الإدارة
        button_layout = QHBoxLayout()
        self.add_subscription_btn = QPushButton("إضافة اشتراك")
        self.edit_subscription_btn = QPushButton("تعديل")
        self.delete_subscription_btn = QPushButton("حذف")
        
        button_layout.addWidget(self.add_subscription_btn)
        button_layout.addWidget(self.edit_subscription_btn)
        button_layout.addWidget(self.delete_subscription_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        # جدول الاشتراكات
        self.subscriptions_table = QTableWidget()
        self.subscriptions_table.setColumnCount(7)
        self.subscriptions_table.setHorizontalHeaderLabels(["المعرف", "اسم الخطة", "التكلفة الشهرية", "تاريخ البداية", "تاريخ النهاية", "نشط", "الوصف"])
        self.subscriptions_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.subscriptions_table.setAlternatingRowColors(True)
        self.subscriptions_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.subscriptions_table.verticalHeader().setVisible(False)
        
        layout.addWidget(self.subscriptions_table)
        
        # ربط الأزرار
        self.add_subscription_btn.clicked.connect(self.add_subscription)
        self.edit_subscription_btn.clicked.connect(self.edit_subscription)
        self.delete_subscription_btn.clicked.connect(self.delete_subscription)
        
        widget.setLayout(layout)
        return widget
    
    def load_data(self):
        """تحميل جميع البيانات"""
        self.load_debts()
        self.load_installments()
        self.load_subscriptions()
    
    def load_debts(self):
        """تحميل بيانات الديون"""
        debts = self.debt_model.get_debts_by_person(self.person_data[0])
        self.debts_table.setRowCount(len(debts))
        
        for row, debt in enumerate(debts):
            self.debts_table.setItem(row, 0, QTableWidgetItem(str(debt[0])))
            self.debts_table.setItem(row, 1, QTableWidgetItem(f"{debt[2]:.2f} ريال"))
            self.debts_table.setItem(row, 2, QTableWidgetItem(debt[3] or ""))
            self.debts_table.setItem(row, 3, QTableWidgetItem(debt[4]))
            self.debts_table.setItem(row, 4, QTableWidgetItem("مدفوع" if debt[5] else "غير مدفوع"))
    
    def load_installments(self):
        """تحميل بيانات الأقساط"""
        installments = self.installment_model.get_installments_by_person(self.person_data[0])
        self.installments_table.setRowCount(len(installments))
        
        for row, installment in enumerate(installments):
            self.installments_table.setItem(row, 0, QTableWidgetItem(str(installment[0])))
            self.installments_table.setItem(row, 1, QTableWidgetItem(f"{installment[2]:.2f} ريال"))
            self.installments_table.setItem(row, 2, QTableWidgetItem(f"{installment[3]:.2f} ريال"))
            self.installments_table.setItem(row, 3, QTableWidgetItem(f"{installment[4]:.2f} ريال"))
            self.installments_table.setItem(row, 4, QTableWidgetItem(installment[5] or ""))
            self.installments_table.setItem(row, 5, QTableWidgetItem(installment[6] or ""))
            self.installments_table.setItem(row, 6, QTableWidgetItem("مكتمل" if installment[7] else "غير مكتمل"))
    
    def load_subscriptions(self):
        """تحميل بيانات الاشتراكات"""
        subscriptions = self.subscription_model.get_subscriptions_by_person(self.person_data[0])
        self.subscriptions_table.setRowCount(len(subscriptions))
        
        for row, subscription in enumerate(subscriptions):
            self.subscriptions_table.setItem(row, 0, QTableWidgetItem(str(subscription[0])))
            self.subscriptions_table.setItem(row, 1, QTableWidgetItem(subscription[2]))
            self.subscriptions_table.setItem(row, 2, QTableWidgetItem(f"{subscription[3]:.2f} ريال"))
            self.subscriptions_table.setItem(row, 3, QTableWidgetItem(subscription[4] or ""))
            self.subscriptions_table.setItem(row, 4, QTableWidgetItem(subscription[5] or ""))
            self.subscriptions_table.setItem(row, 5, QTableWidgetItem("نشط" if subscription[6] else "غير نشط"))
            self.subscriptions_table.setItem(row, 6, QTableWidgetItem(subscription[7] or ""))
    
    def add_debt(self):
        """إضافة دين جديد"""
        dialog = DebtDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            self.debt_model.add_debt(self.person_data[0], data['amount'], data['description'])
            self.load_debts()
            QMessageBox.information(self, "نجح", "تم إضافة الدين بنجاح")
    
    def edit_debt(self):
        """تعديل دين موجود"""
        current_row = self.debts_table.currentRow()
        if current_row >= 0:
            debt_id = int(self.debts_table.item(current_row, 0).text())
            debts = self.debt_model.get_debts_by_person(self.person_data[0])
            debt_data = next((d for d in debts if d[0] == debt_id), None)
            
            if debt_data:
                dialog = DebtDialog(self, debt_data)
                if dialog.exec_() == QDialog.Accepted:
                    data = dialog.get_data()
                    self.debt_model.update_debt(debt_id, data['amount'], data['description'], data['is_paid'])
                    self.load_debts()
                    QMessageBox.information(self, "نجح", "تم تعديل الدين بنجاح")
        else:
            QMessageBox.warning(self, "تحذير", "يرجى اختيار دين للتعديل")
    
    def delete_debt(self):
        """حذف دين"""
        current_row = self.debts_table.currentRow()
        if current_row >= 0:
            debt_id = int(self.debts_table.item(current_row, 0).text())
            reply = QMessageBox.question(self, "تأكيد الحذف", "هل أنت متأكد من حذف هذا الدين؟")
            if reply == QMessageBox.Yes:
                self.debt_model.delete_debt(debt_id)
                self.load_debts()
                QMessageBox.information(self, "نجح", "تم حذف الدين بنجاح")
        else:
            QMessageBox.warning(self, "تحذير", "يرجى اختيار دين للحذف")
    
    def add_installment(self):
        """إضافة قسط جديد"""
        dialog = InstallmentDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            self.installment_model.add_installment(
                self.person_data[0], 
                data['total_amount'], 
                data['installment_amount'], 
                data['due_date'], 
                data['description']
            )
            self.load_installments()
            QMessageBox.information(self, "نجح", "تم إضافة القسط بنجاح")
    
    def edit_installment(self):
        """تعديل قسط موجود"""
        current_row = self.installments_table.currentRow()
        if current_row >= 0:
            installment_id = int(self.installments_table.item(current_row, 0).text())
            installments = self.installment_model.get_installments_by_person(self.person_data[0])
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
                    self.load_installments()
                    QMessageBox.information(self, "نجح", "تم تعديل القسط بنجاح")
        else:
            QMessageBox.warning(self, "تحذير", "يرجى اختيار قسط للتعديل")
    
    def delete_installment(self):
        """حذف قسط"""
        current_row = self.installments_table.currentRow()
        if current_row >= 0:
            installment_id = int(self.installments_table.item(current_row, 0).text())
            reply = QMessageBox.question(self, "تأكيد الحذف", "هل أنت متأكد من حذف هذا القسط؟")
            if reply == QMessageBox.Yes:
                self.installment_model.delete_installment(installment_id)
                self.load_installments()
                QMessageBox.information(self, "نجح", "تم حذف القسط بنجاح")
        else:
            QMessageBox.warning(self, "تحذير", "يرجى اختيار قسط للحذف")
    
    def add_subscription(self):
        """إضافة اشتراك جديد"""
        dialog = SubscriptionDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            self.subscription_model.add_subscription(
                self.person_data[0],
                data['plan_name'],
                data['monthly_cost'],
                data['start_date'],
                data['end_date'],
                data['description']
            )
            self.load_subscriptions()
            QMessageBox.information(self, "نجح", "تم إضافة الاشتراك بنجاح")
    
    def edit_subscription(self):
        """تعديل اشتراك موجود"""
        current_row = self.subscriptions_table.currentRow()
        if current_row >= 0:
            subscription_id = int(self.subscriptions_table.item(current_row, 0).text())
            subscriptions = self.subscription_model.get_subscriptions_by_person(self.person_data[0])
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
                    self.load_subscriptions()
                    QMessageBox.information(self, "نجح", "تم تعديل الاشتراك بنجاح")
        else:
            QMessageBox.warning(self, "تحذير", "يرجى اختيار اشتراك للتعديل")
    
    def delete_subscription(self):
        """حذف اشتراك"""
        current_row = self.subscriptions_table.currentRow()
        if current_row >= 0:
            subscription_id = int(self.subscriptions_table.item(current_row, 0).text())
            reply = QMessageBox.question(self, "تأكيد الحذف", "هل أنت متأكد من حذف هذا الاشتراك؟")
            if reply == QMessageBox.Yes:
                self.subscription_model.delete_subscription(subscription_id)
                self.load_subscriptions()
                QMessageBox.information(self, "نجح", "تم حذف الاشتراك بنجاح")
        else:
            QMessageBox.warning(self, "تحذير", "يرجى اختيار اشتراك للحذف")
