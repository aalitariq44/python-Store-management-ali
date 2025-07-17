# نظام إدارة المتجر

# نظام إدارة المتجر - Store Management System

نظام شامل لإدارة المتاجر والمؤسسات التجارية باللغة العربية، تم تطويره باستخدام Python و PyQt5 مع قاعدة بيانات SQLite.

## المميزات الرئيسية

### 📊 إدارة الزبائن
- إضافة وتعديل وحذف بيانات الزبائن
- البحث المتقدم في قائمة الزبائن
- عرض تفصيلي لكل زبون مع جميع عملياته
- واجهة منفصلة لتفاصيل كل زبون

### 💰 إدارة الديون
- تسجيل ديون الزبائن مع التفاصيل
- تتبع حالة الديون (مدفوع / غير مدفوع)
- إحصائيات شاملة للديون
- تواريخ الاستحقاق والتنبيهات

### 📅 إدارة الأقساط
- إنشاء أقساط بدوريات مختلفة (شهري، أسبوعي، سنوي)
- تتبع المدفوعات وحساب المتبقي
- إضافة دفعات للأقساط
- نسبة الإنجاز ومؤشرات الحالة

### 🌐 إدارة اشتراكات الإنترنت
- تسجيل اشتراكات الإنترنت بسرعات مختلفة
- تفعيل وإيقاف الاشتراكات
- تتبع تواريخ انتهاء الصلاحية
- التحديث التلقائي لحالة الاشتراكات

## التقنيات المستخدمة

### البرمجة
- **Python 3.7+**: اللغة الأساسية
- **PyQt5**: واجهة المستخدم الرسومية
- **SQLite**: قاعدة البيانات المحلية
- **dataclasses**: لتنظيم النماذج

### التصميم
- **معمارية MVC**: فصل العرض عن المنطق
- **CSS**: تنسيق الواجهات
- **RTL Support**: دعم اللغة العربية
- **Responsive Design**: تصميم متجاوب

## هيكل المشروع

```
python Store management ali/
├── database/
│   ├── __init__.py
│   ├── connection.py       # إدارة الاتصال بقاعدة البيانات
│   ├── models.py          # نماذج البيانات
│   └── queries/           # استعلامات قاعدة البيانات
│       ├── __init__.py
│       ├── person_queries.py
│       ├── debt_queries.py
│       ├── installment_queries.py
│       └── internet_queries.py
├── controllers/           # طبقة المنطق
│   ├── __init__.py
│   ├── person_controller.py
│   ├── debt_controller.py
│   ├── installment_controller.py
│   └── internet_controller.py
├── views/                 # واجهات المستخدم
│   ├── __init__.py
│   ├── main_window.py     # النافذة الرئيسية
│   ├── persons_view.py    # إدارة الزبائن
│   ├── person_details_view.py  # تفاصيل الزبون
│   ├── debts_view.py      # إدارة الديون
│   ├── installments_view.py    # إدارة الأقساط
│   ├── internet_view.py   # إدارة الإنترنت
│   └── dialogs/          # النوافذ المنبثقة
│       ├── __init__.py
│       ├── add_person_dialog.py
│       ├── add_debt_dialog.py
│       ├── add_installment_dialog.py
│       └── add_internet_dialog.py
├── utils/                # المساعدات والأدوات
│   ├── __init__.py
│   ├── helpers.py        # دوال مساعدة
│   └── validators.py     # التحقق من البيانات
├── main.py              # نقطة البداية
├── styles.qss           # ملف التنسيق
└── README.md           # هذا الملف
```

## المتطلبات

### متطلبات النظام
- **نظام التشغيل**: Windows 10+ / macOS 10.14+ / Linux Ubuntu 18.04+
- **Python**: 3.7 أو أحدث
- **ذاكرة**: 512MB RAM كحد أدنى
- **مساحة القرص**: 100MB مساحة فارغة

### المكتبات المطلوبة
```bash
PyQt5>=5.15.0
sqlite3 (مدمجة مع Python)
```

## التثبيت والتشغيل

### 1. استنساخ المشروع
```bash
git clone https://github.com/yourname/store-management-system.git
cd store-management-system
```

### 2. إنشاء البيئة الافتراضية
```bash
python -m venv venv
```

### 3. تفعيل البيئة الافتراضية
**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. تثبيت المتطلبات
```bash
pip install PyQt5
```

### 5. تشغيل التطبيق
```bash
python main.py
```

## دليل الاستخدام

### البدء السريع

1. **تشغيل التطبيق**: قم بتشغيل `main.py`
2. **إضافة زبون جديد**: انقر على "إدارة الزبائن" ثم "إضافة زبون"
3. **تسجيل دين**: من تفاصيل الزبون، انتقل لتبويب "الديون" وانقر "إضافة دين"
4. **إنشاء قسط**: من تبويب "الأقساط" انقر "إضافة قسط" وحدد التفاصيل
5. **اشتراك إنترنت**: من تبويب "الإنترنت" انقر "إضافة اشتراك"

## قاعدة البيانات

### الجداول الرئيسية

#### جدول الزبائن (persons)
```sql
CREATE TABLE persons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT,
    email TEXT,
    address TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### جدول الديون (debts)
```sql
CREATE TABLE debts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    description TEXT,
    is_paid BOOLEAN DEFAULT FALSE,
    due_date DATE,
    paid_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (person_id) REFERENCES persons (id) ON DELETE CASCADE
);
```

#### جدول الأقساط (installments)
```sql
CREATE TABLE installments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER NOT NULL,
    total_amount REAL NOT NULL,
    paid_amount REAL DEFAULT 0,
    installment_amount REAL NOT NULL,
    frequency TEXT NOT NULL CHECK (frequency IN ('monthly', 'weekly', 'yearly')),
    description TEXT,
    start_date DATE,
    end_date DATE,
    is_completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (person_id) REFERENCES persons (id) ON DELETE CASCADE
);
```

#### جدول اشتراكات الإنترنت (internet_subscriptions)
```sql
CREATE TABLE internet_subscriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER NOT NULL,
    speed INTEGER NOT NULL,
    monthly_cost REAL NOT NULL,
    description TEXT,
    start_date DATE,
    end_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (person_id) REFERENCES persons (id) ON DELETE CASCADE
);
```

## الدعم والتواصل

- **الإبلاغ عن الأخطاء**: استخدم Issues في GitHub
- **طلب الميزات**: افتح Feature Request جديد
- **التواصل المباشر**: للدعم التقني

## الترخيص

هذا المشروع مرخص تحت MIT License - راجع ملف LICENSE للتفاصيل.

---

**تم التطوير بـ ❤️ للمجتمع العربي**

## المميزات الرئيسية

### 1️⃣ إدارة الزبائن
- إضافة وتعديل وحذف الزبائن
- البحث في قاعدة بيانات الزبائن
- عرض تفاصيل كل زبون مع إحصائياته

### 2️⃣ إدارة الديون
- تسجيل الديون للزبائن
- تتبع حالة الدفع
- تواريخ الاستحقاق
- عرض الديون المتأخرة

### 3️⃣ إدارة الأقساط
- نظام أقساط مرن (شهري، أسبوعي، سنوي)
- تتبع المدفوعات
- حساب النسب المئوية للإنجاز
- إدارة المبالغ المتبقية

### 4️⃣ اشتراكات الإنترنت
- إدارة باقات الإنترنت
- تتبع الاشتراكات النشطة
- حساب الإيرادات الشهرية
- تواريخ انتهاء الاشتراكات

## الهيكل التقني

### قاعدة البيانات (SQLite)
- **persons**: جدول الزبائن
- **debts**: جدول الديون
- **installments**: جدول الأقساط  
- **internet_subscriptions**: جدول اشتراكات الإنترنت

### هيكل المشروع

```
/project_root
├── main.py                     # نقطة تشغيل التطبيق
├── database/
│   ├── database_connection.py # إدارة الاتصال مع SQLite
│   ├── models.py              # النماذج (Person, Debt, Installment, InternetSubscription)
│   └── queries.py             # استعلامات SQL للعمليات CRUD
├── controllers/
│   ├── person_controller.py   # منطق إدارة الزبائن
│   ├── debt_controller.py     # منطق إدارة الديون
│   ├── installment_controller.py # منطق إدارة الأقساط
│   └── internet_controller.py # منطق إدارة اشتراكات الإنترنت
├── views/
│   ├── main_window.py         # النافذة الرئيسية
│   ├── persons_view.py        # واجهة إدارة الزبائن
│   ├── debts_view.py          # واجهة عرض الديون العامة
│   ├── installments_view.py   # واجهة عرض الأقساط العامة
│   ├── internet_view.py       # واجهة عرض الاشتراكات العامة
│   ├── person_details_view.py # نافذة تفاصيل الزبون
│   └── dialogs/
│       ├── add_person_dialog.py
│       ├── add_debt_dialog.py
│       ├── add_installment_dialog.py
│       └── add_internet_dialog.py
├── utils/
│   ├── helpers.py             # دوال مساعدة عامة
│   └── validators.py          # التحقق من صحة البيانات
└── resources/
    ├── icons/                 # أيقونات الواجهة
    └── styles.qss             # تنسيقات CSS للواجهة
```

## المتطلبات

### البرمجيات المطلوبة
- Python 3.7+
- PyQt5
- SQLite3 (مدمج مع Python)

### التثبيت
```bash
pip install PyQt5
```

## تشغيل التطبيق

```bash
python main.py
```

## كيفية الاستخدام

### 1. البدء السريع
1. تشغيل التطبيق من الملف `main.py`
2. ستظهر النافذة الرئيسية مع أربعة أزرار رئيسية
3. اختر "إدارة الزبائن" للبدء بإضافة الزبائن

### 2. إدارة الزبائن
- **إضافة زبون**: اضغط "إضافة زبون" وأدخل البيانات المطلوبة
- **تعديل زبون**: اختر زبون من القائمة واضغط "تعديل"  
- **حذف زبون**: اختر زبون واضغط "حذف" (سيحذف جميع البيانات المرتبطة)
- **البحث**: استخدم حقل البحث للعثور على زبون محدد

### 3. عرض تفاصيل الزبون
- اضغط مرتين على أي زبون أو اختر "عرض التفاصيل"
- ستفتح نافذة بتبويبات تحتوي على:
  - بيانات الزبون الأساسية
  - الديون الخاصة به
  - الأقساط الخاصة به  
  - اشتراكات الإنترنت الخاصة به

### 4. إدارة الديون
- من النافذة الرئيسية اختر "عرض الديون"
- يمكنك عرض جميع الديون في النظام
- إضافة ديون جديدة
- تعديل أو حذف الديون الموجودة
- وضع علامة "مدفوع" على الديون

### 5. إدارة الأقساط
- اختر "عرض الأقساط" من النافذة الرئيسية
- إضافة أقساط جديدة مع تحديد:
  - المبلغ الإجمالي
  - مبلغ القسط
  - دورية الدفع (شهري/أسبوعي/سنوي)
- إضافة دفعات للأقساط الموجودة
- تتبع نسبة الإنجاز

### 6. اشتراكات الإنترنت
- اختر "اشتراكات الإنترنت" من النافذة الرئيسية
- إضافة اشتراكات جديدة مع تحديد:
  - اسم الباقة
  - السرعة
  - الرسوم الشهرية
  - تواريخ البداية والنهاية
- تفعيل وإلغاء تفعيل الاشتراكات

## المميزات التقنية

### 1. فصل الاهتمامات (Separation of Concerns)
- **Models**: تعريف هياكل البيانات
- **Controllers**: منطق العمل والقواعد
- **Views**: واجهات المستخدم
- **Utils**: الأدوات المساعدة

### 2. التحقق من البيانات
- فحص شامل للبيانات المُدخلة
- رسائل خطأ واضحة باللغة العربية
- منع إدخال البيانات غير الصحيحة

### 3. إدارة قاعدة البيانات
- استخدام SQLite للتخزين المحلي
- العلاقات المناسبة بين الجداول
- حذف تتالي للبيانات المرتبطة

### 4. واجهة المستخدم
- تصميم حديث ومتجاوب
- دعم كامل للغة العربية
- تنسيقات CSS مخصصة
- تجربة مستخدم سهلة ومباشرة

## الملاحظات المهمة

### الأمان
- البيانات محفوظة محلياً في ملف SQLite
- لا توجد اتصالات خارجية
- يُنصح بإجراء نسخ احتياطية دورية

### الأداء
- التطبيق محُسن للاستخدام المحلي
- سرعة في البحث والتصفية
- إدارة ذاكرة فعالة

### التوسعات المستقبلية
- إمكانية إضافة قاعدة بيانات خارجية
- تقارير مفصلة وإحصائيات
- تصدير البيانات لملفات Excel
- نظام صلاحيات للمستخدمين

## المطور

تم تطوير هذا النظام باستخدام:
- **Python 3.x**
- **PyQt5** للواجهات
- **SQLite** لقاعدة البيانات
- **نمط MVC** للهيكل البرمجي

## الترخيص

هذا المشروع مطور للاستخدام التعليمي والتجاري المحلي.

---

**ملاحظة**: تأكد من وجود Python و PyQt5 قبل تشغيل التطبيق.
