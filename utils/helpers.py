# -*- coding: utf-8 -*-
"""
دوال مساعدة عامة
يحتوي على دوال للتنسيق والرسائل والعمليات المساعدة
"""

import sys
from datetime import datetime, date
from typing import Optional
from PyQt5.QtWidgets import QMessageBox, QWidget
from PyQt5.QtCore import QDate


class MessageHelper:
    """
    مساعد الرسائل
    """
    
    @staticmethod
    def show_info(parent: QWidget, title: str, message: str):
        """
        عرض رسالة معلومات
        
        Args:
            parent: النافذة الأب
            title: عنوان الرسالة
            message: نص الرسالة
        """
        msg_box = QMessageBox(parent)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()
    
    @staticmethod
    def show_warning(parent: QWidget, title: str, message: str):
        """
        عرض رسالة تحذير
        
        Args:
            parent: النافذة الأب
            title: عنوان الرسالة
            message: نص الرسالة
        """
        msg_box = QMessageBox(parent)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()
    
    @staticmethod
    def show_error(parent: QWidget, title: str, message: str):
        """
        عرض رسالة خطأ
        
        Args:
            parent: النافذة الأب
            title: عنوان الرسالة
            message: نص الرسالة
        """
        msg_box = QMessageBox(parent)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()
    
    @staticmethod
    def show_question(parent: QWidget, title: str, message: str) -> bool:
        """
        عرض رسالة سؤال
        
        Args:
            parent: النافذة الأب
            title: عنوان الرسالة
            message: نص الرسالة
            
        Returns:
            True إذا ضغط المستخدم Yes
        """
        reply = QMessageBox.question(
            parent, title, message,
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        return reply == QMessageBox.Yes


class DateHelper:
    """
    مساعد التواريخ
    """
    
    @staticmethod
    def format_date(date_obj: Optional[date]) -> str:
        """
        تنسيق التاريخ للعرض
        
        Args:
            date_obj: كائن التاريخ
            
        Returns:
            التاريخ منسق أو فارغ
        """
        if date_obj:
            return date_obj.strftime("%Y-%m-%d")
        return ""
    
    @staticmethod
    def format_datetime(datetime_obj: Optional[datetime]) -> str:
        """
        تنسيق التاريخ والوقت للعرض
        
        Args:
            datetime_obj: كائن التاريخ والوقت
            
        Returns:
            التاريخ والوقت منسق أو فارغ
        """
        if datetime_obj:
            return datetime_obj.strftime("%Y-%m-%d %H:%M")
        return ""
    
    @staticmethod
    def date_to_qdate(date_obj: Optional[date]) -> Optional[QDate]:
        """
        تحويل التاريخ Python إلى QDate
        
        Args:
            date_obj: كائن التاريخ Python
            
        Returns:
            QDate أو None
        """
        if date_obj:
            return QDate(date_obj.year, date_obj.month, date_obj.day)
        return None
    
    @staticmethod
    def qdate_to_date(qdate: QDate) -> Optional[date]:
        """
        تحويل QDate إلى تاريخ Python
        
        Args:
            qdate: QDate
            
        Returns:
            date أو None
        """
        if qdate and qdate.isValid():
            return date(qdate.year(), qdate.month(), qdate.day())
        return None


class NumberHelper:
    """
    مساعد الأرقام
    """
    
    @staticmethod
    def format_currency(amount: float) -> str:
        """
        تنسيق المبلغ كعملة
        
        Args:
            amount: المبلغ
            
        Returns:
            المبلغ منسق
        """
        return f"{amount:,.2f}"
    
    @staticmethod
    def format_percentage(percentage: float) -> str:
        """
        تنسيق النسبة المئوية
        
        Args:
            percentage: النسبة
            
        Returns:
            النسبة منسقة
        """
        return f"{percentage:.1f}%"
    
    @staticmethod
    def safe_float(value: str) -> float:
        """
        تحويل النص إلى رقم عشري بأمان
        
        Args:
            value: النص
            
        Returns:
            الرقم العشري أو 0.0
        """
        try:
            return float(value.replace(',', ''))
        except (ValueError, AttributeError):
            return 0.0
    
    @staticmethod
    def safe_int(value: str) -> int:
        """
        تحويل النص إلى رقم صحيح بأمان
        
        Args:
            value: النص
            
        Returns:
            الرقم الصحيح أو 0
        """
        try:
            return int(float(value.replace(',', '')))
        except (ValueError, AttributeError):
            return 0


class TableHelper:
    """
    مساعد الجداول
    """
    
    @staticmethod
    def setup_table_headers(table_widget, headers: list):
        """
        إعداد رؤوس الجدول
        
        Args:
            table_widget: الجدول
            headers: قائمة برؤوس الأعمدة
        """
        table_widget.setColumnCount(len(headers))
        table_widget.setHorizontalHeaderLabels(headers)
        
        # ضبط عرض الأعمدة
        header = table_widget.horizontalHeader()
        for i in range(len(headers)):
            header.setSectionResizeMode(i, header.Stretch)
    
    @staticmethod
    def clear_table(table_widget):
        """
        مسح محتويات الجدول
        
        Args:
            table_widget: الجدول
        """
        table_widget.setRowCount(0)
    
    @staticmethod
    def get_selected_row_data(table_widget) -> Optional[dict]:
        """
        الحصول على بيانات الصف المحدد
        
        Args:
            table_widget: الجدول
            
        Returns:
            قاموس ببيانات الصف أو None
        """
        current_row = table_widget.currentRow()
        if current_row >= 0:
            row_data = {}
            for col in range(table_widget.columnCount()):
                item = table_widget.item(current_row, col)
                if item:
                    row_data[col] = item.text()
                else:
                    row_data[col] = ""
            return row_data
        return None


class StyleHelper:
    """
    مساعد التنسيقات
    """
    
    @staticmethod
    def get_status_style(is_active: bool) -> str:
        """
        الحصول على نمط الحالة
        
        Args:
            is_active: حالة النشاط
            
        Returns:
            نمط CSS
        """
        if is_active:
            return "color: green; font-weight: bold;"
        else:
            return "color: red; font-weight: bold;"
    
    @staticmethod
    def get_amount_style(amount: float) -> str:
        """
        الحصول على نمط المبلغ
        
        Args:
            amount: المبلغ
            
        Returns:
            نمط CSS
        """
        if amount > 0:
            return "color: green; font-weight: bold;"
        elif amount < 0:
            return "color: red; font-weight: bold;"
        else:
            return "color: gray;"


class AppHelper:
    """
    مساعد التطبيق
    """
    
    @staticmethod
    def center_window(window, width: int = 800, height: int = 600):
        """
        توسيط النافذة على الشاشة
        
        Args:
            window: النافذة
            width: العرض
            height: الارتفاع
        """
        from PyQt5.QtWidgets import QDesktopWidget
        
        window.resize(width, height)
        
        # الحصول على معلومات الشاشة
        desktop = QDesktopWidget()
        screen_geometry = desktop.screenGeometry()
        
        # حساب المركز
        x = (screen_geometry.width() - width) // 2
        y = (screen_geometry.height() - height) // 2
        
        window.move(x, y)
    
    @staticmethod
    def set_window_icon(window, icon_path: str):
        """
        تعيين أيقونة النافذة
        
        Args:
            window: النافذة
            icon_path: مسار الأيقونة
        """
        from PyQt5.QtGui import QIcon
        
        try:
            window.setWindowIcon(QIcon(icon_path))
        except Exception:
            pass  # تجاهل الخطأ إذا لم توجد الأيقونة
