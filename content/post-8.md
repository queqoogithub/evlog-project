---
title: "High Cohesion, Low Coupling"
date: "2026-03-05"
tags: ["personal"]
---

<span style="color:violet">High Cohesion, Low Coupling</span> →
Design Pattern ที่เน้นให้โค้ดมีความสัมพันธ์กันภายในโมดูลสูง (High Cohesion) และมีความเชื่อมโยงระหว่างโมดูลต่ำ (Low Coupling)

![](https://png.pngtree.com/png-clipart/20230928/original/pngtree-cute-spaghetti-cartoon-illustration-png-image_13005549.png)

### ❌ ตัวอย่าง: low cohesion

```python

# shop_utils.py
def add_product_to_cart(cart, product):
    cart.append(product)

def calculate_total(cart):
    return sum(item['price'] for item in cart)

def process_payment(payment_details):
    print("Processing payment...")

def generate_invoice(cart, customer):
    print("Generating invoice...")
```

**ปัญหา:**

* function พวกนี้ถูกโยนไว้ใน module เดียวกัน (```shop_utils.py```) แต่จริงๆแล้ว แต่ละ function มันอยู่คนละ concern
* ถ้าเอาไว้ใน module เดียวกัน → low cohesion → เพราะ module มันบอกไม่ได้ว่า "ตัวเองทำอะไร" มันเลยกลายเป็นถังขยะรวม

### ✅ ตัวอย่าง: high cohesion

```python

# cart.py
class Cart:
    def __init__(self):
        self.items = []

    def add_product(self, product):
        self.items.append(product)

    def calculate_total(self):
        return sum(item['price'] for item in self.items)
```

```Cart``` → concern เดียว → เกี่ยวกับตะกร้า

**function ข้างในทุกตัว → ทำงานกับ state ของ self.items → เกิด high cohesion**

```python
# payment.py
class PaymentProcessor:
    def process_payment(self, amount, payment_method):
        print(f"Processing {payment_method} payment of ${amount}")

# invoice.py
class InvoiceGenerator:
    def generate_invoice(self, cart, customer):
        print(f"Generating invoice for {customer}")
```

```PaymentProcessor``` → concern เดียว → เกี่ยวกับการจ่ายเงิน

**function ข้างในทุกตัว → ทำงานกับ state ของตัวเอง → เกิด high cohesion**

&nbsp;

### ทำไมแยกเป็น class แล้วช่วยได้ ?

* หลักๆ คือเรื่อง <b>single responsibility</b>
* ทำให้โค้ดอ่านเข้าใจง่าย → maintain ก็ง่ายขึ้น
* ลดโอกาสเกิด bugs (เพราะแต่ละ class จะทำแค่หน้าที่ของตัวเอง ไม่ยุ่งกับ class อื่น)
* เพิ่มประสิทธิภาพการพัฒนา (dev ตัดสินใจง่ายขึ้นว่าต้องพัฒนา หรือ แก้ส่วนไหน)