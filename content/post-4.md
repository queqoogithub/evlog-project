---
title: "มาลองใช้ Ollama กัน 🦙"
date: "2025-07-30"
tags: ["intro", "personal"]
---

![](https://content.pstmn.io/d776e89b-2248-4c3f-a942-2eef03064755/b2xsYW1hLmpwZw==)
<br>

<div class="callout callout-info">
✅ <strong>Info:</strong> ollama คือ tool ที่ช่วยให้เรารัน llm บนเครื่องของเราได้ (เหมือนมี chatgpt ส่วนตัว)
</div>

<br>

### ขั้นตอนการติดตั้งและใช้งาน Ollama
* ติดตั้ง [ollama download](https://ollama.com/download/windows)
* เปิด ollama (คลิกไปที่ icon มันเลย)
* เปิด terminal ขึ้นมา จากนั้นลองเช็ค version ด้วย ```ollama version```
* ติดตั้ง [ollama models](https://ollama.com/search) ด้วย ```ollama run model_xxx```
* จาก step ก่อนหน้า ollama มันจะติดตั้งและเรียกใช้งาน model ที่เราสนใจ
* [ 🍎 ทางเลือก 1 ] ตอนเปิด (ใช้งานครั้งถัดไป) ก็ ```ollama list``` จากนั้นเลือก model แล้วก็รัน ```ollama run model_xxx``` 
* [ 🍏 ทางเลือก 2 ] หรือถ้าต้องการเปิดผ่านหน้า user interface ก็คลิกไปที่แอป ollama ได้เลย (⚠️ ทั้งนี้ ใครที่โหลดแอปมานานแล้ว อาจจะต้องอัปเดทก่อนนะ เพราะฟีเจอร์ user interface เพิ่งมาเมื่อ 30 July นี่เอง)
<br>

![](https://llama-2.ai/wp-content/uploads/2023/12/Ollama-Multimodel-Models.jpeg)
<br>

<video autoplay muted loop controls width="100%" class="rounded-lg my-4">
  <source src="https://files.ollama.com/ollama_chat.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>
<br>

### ขั้นตอนการ เพิ่ม/อัพเดท/ลบ โมเดล
* ขั้นตอนนี้ต้องเปิด terminal ขึ้นมา จากนั้น
* [ 🍎 เพิ่ม/อัพเดท ] ```ollama pull model_xxxx``` สามารถเลือกโมเดลได้ที่ [explore models](https://ollama.com/search)
* [ 🍏 ลบ ] ```ollama rm model_xxx```

<br>

### โมเดลแปลภาษา Thai 🇹🇭 English 🇺🇸 แนะนำ
จากที่ผมลองใช้งานมาถือว่ายอดเยี่ยมเลย model นั้นก็คือ [typhoon-translate](https://ollama.com/scb10x/typhoon-translate-4b) เป็น model ที่ทาง scb10x พัฒนาขึ้นมาให้เราใช้แบบฟรีๆ ด้วยขนาดแค่ 4b parameters (~ 2.5 gb) ลองไปโหลดมาใช้แปลภาษากันได้
![](https://cdn-thumbnails.huggingface.co/social-thumbnails/models/scb10x/typhoon-translate-4b.png)
<br>

Refs: [ollama official](https://ollama.com)
