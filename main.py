# الواجهة الرئيسية - Main Window
# النافذة الأساسية للتطبيق التي تحتوي على إدارة الزبائن والوصول للواجهات الأخرى

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from database import DatabaseManager
from models import Person
from dialogs import PersonDialog
from person_details_window import PersonDetailsWindow
from general_views import AllDebtsWindow, AllInstallmentsWindow, AllSubscriptionsWindow

class MainWindow(QMainWindow):
    """النافذة الرئيسية للتطبيق"""
    
    def __init__(self):
        super().__init__()
        
        # تهيئة قاعدة البيانات والنماذج
        self.db_manager = DatabaseManager()
        self.person_model = Person(self.db_manager)
        
        self.init_ui()
        self.load_persons()
    
    def init_ui(self):
        """تهيئة واجهة المستخدم"""
        self.setWindowTitle("نظام إدارة المتجر")
        self.setGeometry(100, 100, 1400, 800)

        # تطبيق تصميم عصري
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2E2E2E;
            }
            QMenuBar {
                background-color: #3C3C3C;
                color: #F0F0F0;
                font-size: 14px;
            }
            QMenuBar::item:selected {
                background-color: #5A9B5A;
            }
            QMenu {
                background-color: #3C3C3C;
                color: #F0F0F0;
            }
            QMenu::item:selected {
                background-color: #5A9B5A;
            }
            QToolBar {
                background-color: #3C3C3C;
                border: none;
            }
            QToolButton {
                color: #F0F0F0;
                font-size: 14px;
                padding: 8px;
            }
            QToolButton:hover {
                background-color: #5A9B5A;
            }
            QStatusBar {
                background-color: #3C3C3C;
                color: #F0F0F0;
                font-size: 12px;
            }
        """)
        
        # إنشاء القائمة الرئيسية
        self.create_menu_bar()
        
        # إنشاء شريط الأدوات
        self.create_toolbar()
        
        # إنشاء الواجهة المركزية
        self.create_central_widget()
        
        # إنشاء شريط الحالة
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("مرحباً بك في نظام إدارة المتجر")
    
    def create_menu_bar(self):
        """إنشاء القائمة الرئيسية"""
        menubar = self.menuBar()
        
        # قائمة الزبائن
        customers_menu = menubar.addMenu("الزبائن")
        
        add_customer_action = QAction("إضافة زبون جديد", self)
        add_customer_action.triggered.connect(self.add_person)
        customers_menu.addAction(add_customer_action)
        
        customers_menu.addSeparator()
        
        refresh_action = QAction("تحديث القائمة", self)
        refresh_action.triggered.connect(self.load_persons)
        customers_menu.addAction(refresh_action)
        
        # قائمة العرض العام
        view_menu = menubar.addMenu("العرض العام")
        
        all_debts_action = QAction("جميع الديون", self)
        all_debts_action.triggered.connect(self.show_all_debts)
        view_menu.addAction(all_debts_action)
        
        all_installments_action = QAction("جميع الأقساط", self)
        all_installments_action.triggered.connect(self.show_all_installments)
        view_menu.addAction(all_installments_action)
        
        all_subscriptions_action = QAction("جميع اشتراكات الإنترنت", self)
        all_subscriptions_action.triggered.connect(self.show_all_subscriptions)
        view_menu.addAction(all_subscriptions_action)
        
        # قائمة المساعدة
        help_menu = menubar.addMenu("مساعدة")
        
        about_action = QAction("حول البرنامج", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def create_toolbar(self):
        """إنشاء شريط الأدوات"""
        toolbar = self.addToolBar("الأدوات الرئيسية")
        
        # أزرار شريط الأدوات
        add_person_btn = QAction("إضافة زبون", self)
        add_person_btn.triggered.connect(self.add_person)
        toolbar.addAction(add_person_btn)
        
        edit_person_btn = QAction("تعديل زبون", self)
        edit_person_btn.triggered.connect(self.edit_person)
        toolbar.addAction(edit_person_btn)
        
        delete_person_btn = QAction("حذف زبون", self)
        delete_person_btn.triggered.connect(self.delete_person)
        toolbar.addAction(delete_person_btn)
        
        toolbar.addSeparator()
        
        view_details_btn = QAction("عرض التفاصيل", self)
        view_details_btn.triggered.connect(self.view_person_details)
        toolbar.addAction(view_details_btn)
        
        toolbar.addSeparator()
        
        refresh_btn = QAction("تحديث", self)
        refresh_btn.triggered.connect(self.load_persons)
        toolbar.addAction(refresh_btn)
    
    def create_central_widget(self):
        """إنشاء الواجهة المركزية"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # تطبيق تصميم مخصص للواجهة المركزية
        central_widget.setStyleSheet("""
            QWidget {
                background-color: #3C3C3C;
                color: #F0F0F0;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 16px;
            }
            QLabel {
                font-size: 16px;
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
                font-size: 16px;
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
                font-size: 16px;
                color: #F0F0F0;
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
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # عنوان القسم
        title_label = QLabel("إدارة الزبائن")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title_label.setStyleSheet("color: #5A9B5A;")
        layout.addWidget(title_label)
        
        # شريط البحث
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("البحث:"))
        
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("ابحث بالاسم, الهاتف, أو العنوان...")
        self.search_edit.textChanged.connect(self.search_persons)
        search_layout.addWidget(self.search_edit)
        
        self.search_button = QPushButton("بحث")
        self.search_button.clicked.connect(self.search_persons)
        search_layout.addWidget(self.search_button)
        
        layout.addLayout(search_layout)
        
        # جدول الزبائن
        self.persons_table = QTableWidget()
        self.persons_table.setColumnCount(4)
        self.persons_table.setHorizontalHeaderLabels(["المعرف", "الاسم", "رقم الهاتف", "العنوان"])
        self.persons_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.persons_table.setAlternatingRowColors(True)
        self.persons_table.doubleClicked.connect(self.view_person_details)
        self.persons_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.persons_table.verticalHeader().setVisible(False)
        
        layout.addWidget(self.persons_table)
        
        # أزرار الإجراءات
        buttons_layout = QHBoxLayout()
        
        self.add_person_btn = QPushButton("إضافة زبون جديد")
        self.edit_person_btn = QPushButton("تعديل البيانات")
        self.delete_person_btn = QPushButton("حذف الزبون")
        self.view_details_btn = QPushButton("عرض التفاصيل")
        
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.add_person_btn)
        buttons_layout.addWidget(self.edit_person_btn)
        buttons_layout.addWidget(self.delete_person_btn)
        buttons_layout.addWidget(self.view_details_btn)
        
        layout.addLayout(buttons_layout)
        
        # ربط الأزرار بالوظائف
        self.add_person_btn.clicked.connect(self.add_person)
        self.edit_person_btn.clicked.connect(self.edit_person)
        self.delete_person_btn.clicked.connect(self.delete_person)
        self.view_details_btn.clicked.connect(self.view_person_details)
        
        central_widget.setLayout(layout)
    
    def load_persons(self):
        """تحميل جميع الزبائن"""
        persons = self.person_model.get_all_persons()
        self.populate_table(persons)
        self.status_bar.showMessage(f"تم تحميل {len(persons)} زبون")
    
    def populate_table(self, persons):
        """ملء الجدول بالزبائن"""
        self.persons_table.setRowCount(len(persons))
        
        for row, person in enumerate(persons):
            self.persons_table.setItem(row, 0, QTableWidgetItem(str(person[0])))
            self.persons_table.setItem(row, 1, QTableWidgetItem(person[1]))
            self.persons_table.setItem(row, 2, QTableWidgetItem(person[2] or ""))
            self.persons_table.setItem(row, 3, QTableWidgetItem(person[3] or ""))
    
    def search_persons(self):
        """البحث عن الزبائن"""
        search_term = self.search_edit.text().strip()
        if search_term:
            persons = self.person_model.search_persons(search_term)
            self.populate_table(persons)
            self.status_bar.showMessage(f"تم العثور على {len(persons)} زبون")
        else:
            self.load_persons()
    
    def add_person(self):
        """إضافة زبون جديد"""
        dialog = PersonDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()
            if data['name']:
                self.person_model.add_person(data['name'], data['phone'], data['address'])
                self.load_persons()
                QMessageBox.information(self, "نجح", "تم إضافة الزبون بنجاح")
            else:
                QMessageBox.warning(self, "تحذير", "يجب إدخال اسم الزبون")
    
    def edit_person(self):
        """تعديل بيانات الزبون"""
        current_row = self.persons_table.currentRow()
        if current_row >= 0:
            person_id = int(self.persons_table.item(current_row, 0).text())
            person_data = self.person_model.get_person_by_id(person_id)
            
            if person_data:
                dialog = PersonDialog(self, person_data)
                if dialog.exec_() == QDialog.Accepted:
                    data = dialog.get_data()
                    if data['name']:
                        self.person_model.update_person(person_id, data['name'], data['phone'], data['address'])
                        self.load_persons()
                        QMessageBox.information(self, "نجح", "تم تعديل بيانات الزبون بنجاح")
                    else:
                        QMessageBox.warning(self, "تحذير", "يجب إدخال اسم الزبون")
        else:
            QMessageBox.warning(self, "تحذير", "يرجى اختيار زبون للتعديل")
    
    def delete_person(self):
        """حذف الزبون"""
        current_row = self.persons_table.currentRow()
        if current_row >= 0:
            person_id = int(self.persons_table.item(current_row, 0).text())
            person_name = self.persons_table.item(current_row, 1).text()
            
            reply = QMessageBox.question(
                self, 
                "تأكيد الحذف", 
                f"هل أنت متأكد من حذف الزبون '{person_name}'؟\n\nسيؤدي هذا إلى حذف جميع البيانات المرتبطة به (الديون، الأقساط، الاشتراكات).",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.person_model.delete_person(person_id)
                self.load_persons()
                QMessageBox.information(self, "نجح", "تم حذف الزبون وجميع بياناته بنجاح")
        else:
            QMessageBox.warning(self, "تحذير", "يرجى اختيار زبون للحذف")
    
    def view_person_details(self):
        """عرض تفاصيل الزبون"""
        current_row = self.persons_table.currentRow()
        if current_row >= 0:
            person_id = int(self.persons_table.item(current_row, 0).text())
            person_data = self.person_model.get_person_by_id(person_id)
            
            if person_data:
                details_window = PersonDetailsWindow(person_data, self.db_manager, self)
                details_window.exec_()
        else:
            QMessageBox.warning(self, "تحذير", "يرجى اختيار زبون لعرض تفاصيله")
    
    def show_all_debts(self):
        """عرض جميع الديون"""
        self.debts_window = AllDebtsWindow(self.db_manager, self)
        self.debts_window.show()
    
    def show_all_installments(self):
        """عرض جميع الأقساط"""
        self.installments_window = AllInstallmentsWindow(self.db_manager, self)
        self.installments_window.show()
    
    def show_all_subscriptions(self):
        """عرض جميع اشتراكات الإنترنت"""
        self.subscriptions_window = AllSubscriptionsWindow(self.db_manager, self)
        self.subscriptions_window.show()
    
    def show_about(self):
        """عرض معلومات حول البرنامج"""
        QMessageBox.about(
            self,
            "حول البرنامج",
            """
            <h3>نظام إدارة المتجر</h3>
            <p>برنامج شامل لإدارة الزبائن والديون والأقساط واشتراكات الإنترنت</p>
            <p><b>الإصدار:</b> 1.0</p>
            <p><b>التقنيات المستخدمة:</b> Python, PyQt5, SQLite</p>
            <p><b>الميزات:</b></p>
            <ul>
                <li>إدارة الزبائن</li>
                <li>تتبع الديون</li>
                <li>إدارة الأقساط</li>
                <li>متابعة اشتراكات الإنترنت</li>
                <li>واجهة سهلة الاستخدام</li>
                <li>قاعدة بيانات محلية</li>
            </ul>
            """
        )

def main():
    """دالة تشغيل التطبيق الرئيسية"""
    app = QApplication(sys.argv)
    
    # تطبيق الستايل العربي
    app.setLayoutDirection(Qt.RightToLeft)
    
    # إنشاء وعرض النافذة الرئيسية
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
