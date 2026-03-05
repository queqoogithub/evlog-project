---
title: "โค้ดเริ่มตุ่ย 💩"
date: "2025-07-03"
tags: ["personal"]
---

### Code Smells

<span style="color:brown">Code Smells ( โค้ดเริ่มตุ่ย 💩 )</span> คือ 
สัญญาณเตือนว่าโค้ดเริ่มมีปัญหาบางอย่าง (เช่น โค้ดเริ่มอ่านไม่รู้เรื่อง) ถึงแม้ว่าโค้ดจะยังทำงานได้ปกติ แต่การมี Code Smells จะทำให้โค้ดมีปัญหาในระยะยาว ... สะสมเป็น <b>Tech Debt</b>

![](https://media.licdn.com/dms/image/v2/D4D12AQGi6c9pRsiNYQ/article-cover_image-shrink_600_2000/article-cover_image-shrink_600_2000/0/1734422913181?e=2147483647&v=beta&t=cJFiW6zGmsy-WQz-gDtmhR0k2TrehA3CiThwyudt4GM)

&nbsp;

### ทำไม Code Smells ถึงสำคัญ ?
* ลดประสิทธิภาพการเดฟ - Code Smells ยากในการทำความเข้าใจ แก้ไขและทดสอบ
* เพิ่มโอกาสเกิด Bugs - โค้ดที่ซับซ้อนเกินไปทำให้เกิด Bugs ง่าย
* ลดคุณภาพโดยรวม - ส่งผลต่อความน่าเชื่อถือและประสิทธิภาพของระบบ

&nbsp;

❌ โค้ดซ้ำ

```python

    def calculate_rectangle_area(length, width):
        if length <= 0 or width <= 0:
            raise ValueError("Length and width must be positive")
        return length * width

    def calculate_triangle_area(base, height):
        if base <= 0 or height <= 0:
            raise ValueError("Base and height must be positive")
        return 0.5 * base * height

    def calculate_circle_area(radius):
        if radius <= 0:
            raise ValueError("Radius must be positive")
        return 3.14159 * radius * radius
```

✅ การแก้ไข: สร้าง Class หรือ Function เพื่อ Reuse มัน

```python

    def _validate_positive_values(*values):
        if any(value <= 0 for value in values):
            raise ValueError("All values must be positive")

    def calculate_rectangle_area(length, width):
        _validate_positive_values(length, width)
        return length * width

    def calculate_triangle_area(base, height):
        _validate_positive_values(base, height)
        return 0.5 * base * height

    def calculate_circle_area(radius):
        _validate_positive_values(radius)
        return 3.14159 * radius * radius
```

❌ Class หรือ Function ใหญ่ (ยาว) ไป

```python

    class User:
        def __init__(self, name, email):
            self.name = name
            self.email = email
            self.orders = []
        
        def validate_email(self):
            return re.match(r'^[^@]+@[^@]+\.[^@]+$', self.email)
        
        def send_email(self, message):
            pass
        
        def add_order(self, order):
            self.orders.append(order)
        
        def calculate_total_spent(self):
            return sum(order.total for order in self.orders)
        
        def generate_receipt(self, order):
            pass
        
        def save_to_database(self):
            pass
```

✅ การแก้ไข: แตก Class หรือ Function ออกตามหน้าที่ย่อยๆ

```python

    class User:
        def __init__(self, name, email):
            self.name = name
            self.email = email
            self.orders = []
        
        def add_order(self, order):
            self.orders.append(order)

    class EmailValidator:
        @staticmethod
        def is_valid(email):
            return re.match(r'^[^@]+@[^@]+\.[^@]+$', email) is not None

    class EmailService:
        @staticmethod
        def send_email(email, message):
            pass

    class OrderAnalyzer:
        @staticmethod
        def calculate_total_spent(orders):
            return sum(order.total for order in orders)

    class ReceiptGenerator:
        @staticmethod
        def generate_receipt(order):
            pass

    class UserRepository:
        @staticmethod
        def save_user(user):
            pass
```

❌ Parameter ยาวปายยยย...ยยย

```python

    def create_user_account(first_name, last_name, email, phone, address, 
                        city, state, zip_code, country, date_of_birth, 
                        preferred_language, marketing_consent):
        pass
```

✅ การแก้ไข: แตก Class ย่อยตามประเภท Parameters

```python

    from dataclasses import dataclass
    from typing import Optional

    @dataclass
    class UserProfile:
        first_name: str
        last_name: str
        email: str
        phone: Optional[str] = None
        date_of_birth: Optional[str] = None

    @dataclass
    class UserAddress:
        address: str
        city: str
        state: str
        zip_code: str
        country: str

    @dataclass
    class UserPreferences:
        preferred_language: str = 'en'
        marketing_consent: bool = False

    def create_user_account(profile: UserProfile, 
                        address: UserAddress, 
                        preferences: UserPreferences):
        pass
```

❌ Magic Number (ตัวเลขลึกลับ มีที่ไป ... แต่ไม่มีที่มา)

```python

    def calculate_discount(amount):
        if amount > 1000:
            return amount * 0.1
        elif amount > 500:
            return amount * 0.05
        return 0
```

✅ การแก้ไข: กำหนดมันเป็นค่าคงที่

```python

    # constants
    PREMIUM_THRESHOLD = 1000
    STANDARD_THRESHOLD = 500
    PREMIUM_DISCOUNT_RATE = 0.1
    STANDARD_DISCOUNT_RATE = 0.05

    def calculate_discount(amount):
        if amount > PREMIUM_THRESHOLD:
            return amount * PREMIUM_DISCOUNT_RATE
        elif amount > STANDARD_THRESHOLD:
            return amount * STANDARD_DISCOUNT_RATE
        return 0
```

&nbsp;

ถ้าโค้ดของเรามีลักษณะ (❌) ดังกล่าว นั่นแสดงว่าโค้ดของเราเริ่มส่งกลิ่น (ตุ่ย) แล้วหละ 💩💩💩

&nbsp;

### แนวทางเพื่อหลีกเลี่ยง Code Smells ?

* Design Principles - ปฏิบัติตามหหลักการที่ดี เช่น SOLID Principles
* Code Review - ให้เพื่อนร่วมทีมช่วยตรวจสอบ
* Refactoring - ปรับปรุงโค้ดอย่างสม่ำเสมอ
* Naming - ตั้งชื่อตัวแปรและฟังก์ชันให้สื่อความหมาย

&nbsp;

Refs: [Understanding Code Smells](https://www.linkedin.com/pulse/understanding-code-smells-what-why-matter-how-fix-them-savchenko-tevsf/)