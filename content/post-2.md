---
title: "Test Coverage 🧪"
date: "2025-07-02"
tags: ["personal"]
---

## ประเด็นสำคัญเกี่ยวกับ Test Coverage ( TC )

<br>
<div class="callout callout-warning">
⚠️ <strong>Warning:</strong> แม้ว่า TC จะช่วยตรวจสอบโค้ดส่วนที่ยังไม่ได้เทส (Finding Untested Code) แต่ก็มีข้อควรระวังที่เราควรพิจารณา
</div>
<br>

![](https://cdn.prod.website-files.com/62294553e9aeea20d15d7bc2/66fe582bc6931aa7f5f7e60d_649c8f07635380642bbfa001_Quality%2520Assurance%2520Testing%2520Meme.webp)
<br>

### ตัวเลข TC ไม่ใช่ตัวชี้วัดคุณภาพการเทส (Quality Target): 

* การกำหนดเป้าหมาย TC ที่สูงๆ เช่น "ต้องอย่างน้อย 80% ก่อนนำโค้ดขึ้น Production" อาจทำให้เดฟเขียนเทสเพื่อให้ได้ตัวเลขตามเป้าหมาย โดยไม่ได้คำนึงถึงคุณภาพ (Quality) ของการเทสจริงๆ 
* การมี TC สูงๆ เช่น 100% อาจชี้ให้เห็นว่ามีการเขียนเทสเพียงเพื่อเพิ่มตัวเลข ไม่ได้ดูว่าส่วนใดของโค้ดมีความสำคัญและควรเน้นการทดสอบเป็นพิเศษ (เช่น การเทส Trivial Code)

<br>

Trivial Code

```python

    def process_status_code(status_code):
        """
        Processes a given HTTP status code.
        """
        if status_code >= 200 and status_code < 300:
            return "SUCCESS"
        elif status_code >= 400 and status_code < 500:
            return "CLIENT_ERROR"
        elif status_code >= 500 and status_code < 600:
            return "SERVER_ERROR"
        else:
            return "UNKNOWN"
```

❌ Trivial Test ⇒ การเขียนเทสเพื่อให้ครอบคลุมทุก ```if | elif | else``` statement นั้นง่ายมากๆ ⇒ แต่ไม่ได้สะท้อน behavior อะไรเลย

```python

    class TestStatusCodeProcessor(unittest.TestCase):
        def test_success_status(self):
            self.assertEqual(process_status_code(200), "SUCCESS")
            self.assertEqual(process_status_code(299), "SUCCESS")

        def test_client_error_status(self):
            self.assertEqual(process_status_code(400), "CLIENT_ERROR")
            self.assertEqual(process_status_code(404), "CLIENT_ERROR")

        def test_server_error_status(self):
            self.assertEqual(process_status_code(500), "SERVER_ERROR")
            self.assertEqual(process_status_code(503), "SERVER_ERROR")

        def test_unknown_status(self):
            self.assertEqual(process_status_code(100), "UNKNOWN")
            self.assertEqual(process_status_code(300), "UNKNOWN")
            self.assertEqual(process_status_code(600), "UNKNOWN")
```

&nbsp;

### คุณภาพสำคัญกว่าปริมาณ: 

* ควรเน้นที่ Behavior หรือ จุดที่ Complexity สูง ไม่ใช่แค่การเขียนเทสเพื่อให้ครอบคลุมโค้ดมากที่สุด และหากการเปลี่ยนแปลงโค้ดเพียงเล็กน้อย แล้วต้องแก้ไขเทสจำนวนมาก อาจแสดงว่าเทสมีความซ้ำซ้อนกันอยู่ (Brittle Test)
* แนวทาง Test-Driven Development (TDD) เป็นแนวทางที่ดี แต่ก็ไม่เพียงพอที่จะรับประกันได้ว่าเทสนั้นมีคุณภาพดีเสมอไป เช่น ในกรณีที่เดฟตีความ "ความต้องการ (Requirement) ผิดพลาด" โค้ดที่ผ่านเทส นั้นก็อาจจะยังไม่ตอบโจทย์ Users อยู่ดี

<br>

ตัวอย่าง: ฟังก์ชั่นคำนวณส่วนลด

```python

    def calculate_discount(price: float, customer_type: str) -> float:
        if customer_type == "VIP":
            return price * 0.8
        elif customer_type == "Regular":
            return price * 0.9
        else:
            return price
```

❌ TC สูงแต่ซ้ำซ้อนใน Logic ที่ไม่ใช่ Core Business (เช่น integer price, zero price, negative price, none customer) ⇒  ซึ่งจะทำให้ทีมต้อง Maintain เทสที่ไม่มี Value จำนวนมาก !!!

```python

    class TestCalculateDiscountVerbose(unittest.TestCase):
        def test_vip_customer(self):
            self.assertEqual(calculate_discount(100.0, "VIP"), 80.0)

        def test_regular_customer(self):
            self.assertEqual(calculate_discount(100.0, "Regular"), 90.0)

        def test_unknown_customer(self):
            self.assertEqual(calculate_discount(100.0, "Other"), 100.0)

        def test_zero_price(self):
            self.assertEqual(calculate_discount(0.0, "VIP"), 0.0)

        def test_negative_price(self):
            self.assertEqual(calculate_discount(-100.0, "Regular"), -90.0)

        def test_none_customer(self):
            with self.assertRaises(TypeError):
                calculate_discount(100.0)

        def test_integer_price(self):
            self.assertEqual(calculate_discount(200, "VIP"), 160.0)
```

✅ TC น้อยกว่า แต่เน้นคุณภาพ ⇒ เน้นที่ Core Logic ในการคำนวณ Discount ตาม ```customer_type```

```python

    class TestCalculateDiscount(unittest.TestCase):
        def test_customer_type_discount(self):
            test_cases = [
                ("VIP", 100.0, 80.0),
                ("Regular", 100.0, 90.0),
                ("Other", 100.0, 100.0),
            ]
            for customer_type, price, expected in test_cases:
                with self.subTest(customer_type=customer_type):
                    self.assertEqual(calculate_discount(price, customer_type), expected)
```

&nbsp;

### แล้วเมื่อไหร่ที่เรียกได้ว่าเทสเพียงพอ ?
* เมื่อถึงจุดที่แทบจะไม่มี Bugs บน Production
* เมื่อถึงจุดที่การ Refactoring เป็นเรื่องง่าย

<br>

Refs: [Martin Fowler - Test Coverage](https://martinfowler.com/bliki/TestCoverage.html)