# -*- coding: utf-8 -*-
"""
واجهات نظام التسجيل
"""

from .login_dialog import LoginDialog
from .first_time_setup_dialog import FirstTimeSetupDialog
from .password_settings_dialog import PasswordSettingsDialog

__all__ = [
    'LoginDialog',
    'FirstTimeSetupDialog', 
    'PasswordSettingsDialog'
]
