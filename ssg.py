import os
import shutil
import re
import markdown
import frontmatter
from math import ceil
from datetime import datetime
from collections import defaultdict
from jinja2 import Environment, FileSystemLoader

CONTENT_DIR = "content"
OUTPUT_DIR = "output"
TEMPLATES_DIR = "templates"
BASE_URL = "https://evlog-project.vercel.app" # 💡 URL สำหรับ GoLive (Vercel)

env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
post_template = env.get_template("post.html")
tag_template = env.get_template("tag.html")

posts = []
tags_dict = defaultdict(list)

# 1. อ่านทุก markdown ใน content/
for filename in os.listdir(CONTENT_DIR):
    if filename.endswith(".md"):
        filepath = os.path.join(CONTENT_DIR, filename)
        post = frontmatter.load(filepath)
        
        html_body = markdown.markdown(post.content, extensions=['fenced_code', 'tables', 'codehilite'])
        slug = os.path.splitext(filename)[0]

        # แปลงวันที่จาก string -> datetime
        date_str = post.get("date", "2000-01-01")
        date = datetime.strptime(date_str, "%Y-%m-%d")

        # สกัดรูปภาพแรก (ถ้ามี)
        image_match = re.search(r'!\[.*?\]\((.*?)\)', post.content)
        first_image = image_match.group(1) if image_match else "https://images.unsplash.com/photo-1557683316-973673baf926?q=80&w=2029&auto=format&fit=crop"

        post_data = {
            "title": post.get("title", "Untitled"),
            "tags": post.get("tags", []),
            "date": date,
            "content": html_body,
            "image": first_image,
            "slug": slug
        }
        posts.append(post_data)

        for tag in post_data["tags"]:
            tags_dict[tag].append(post_data)

# 🔽 เรียงจากใหม่ไปเก่า
posts.sort(key=lambda p: p["date"], reverse=True)

# 2. สร้าง output/slug.html
os.makedirs(OUTPUT_DIR, exist_ok=True)
for post in posts:
    rendered = post_template.render(post=post, BASE_URL=BASE_URL)
    with open(os.path.join(OUTPUT_DIR, f"{post['slug']}.html"), "w") as f:
        f.write(rendered)

# 3. สร้าง tag pages
tag_dir = os.path.join(OUTPUT_DIR, "tags")
os.makedirs(tag_dir, exist_ok=True)

for tag, tagged_posts in tags_dict.items():
    rendered = tag_template.render(tag=tag, posts=tagged_posts, BASE_URL=BASE_URL)
    with open(os.path.join(tag_dir, f"{tag}.html"), "w") as f:
        f.write(rendered)

print("✅ Static site generated!")

# 4. สร้าง pagination -> index.html + page2.html + ...
index_template = env.get_template("index.html")
POSTS_PER_PAGE = 5

total_pages = (len(posts) + POSTS_PER_PAGE - 1) // POSTS_PER_PAGE

for page_num in range(1, total_pages + 1):
    start = (page_num - 1) * POSTS_PER_PAGE
    end = start + POSTS_PER_PAGE
    page_posts = posts[start:end]

    rendered = index_template.render(
        posts=page_posts,
        current_page=page_num,
        total_pages=total_pages
    )

    if page_num == 1:
        output_path = os.path.join(OUTPUT_DIR, "index.html")
    else:
        output_path = os.path.join(OUTPUT_DIR, f"page{page_num}.html")

    with open(output_path, "w") as f:
        f.write(rendered)

# 5. สร้าง homepage.html (แสดงโพสต์ล่าสุด 3 อัน)
# POSTS_PER_PAGE = 5
# 1. โหลด template
homepage_template = env.get_template("homepage.html")
# 2. จำนวนหน้า
total_pages = ceil(len(posts) / POSTS_PER_PAGE)

for page in range(total_pages):
    start = page * POSTS_PER_PAGE
    end = start + POSTS_PER_PAGE
    page_posts = posts[start:end]

    # ชื่อไฟล์: หน้าแรกคือ index.html, หน้าอื่นคือ page2.html, page3.html ...
    if page == 0:
        filename = "index.html"
    else:
        filename = f"page{page + 1}.html"

    output = homepage_template.render(
        posts=page_posts,
        current_page=page + 1,
        total_pages=total_pages,
        BASE_URL=BASE_URL
    )
    with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
        f.write(output)

# 6. สร้างหน้า about.html
about_template = env.get_template("about.html")
about_output = about_template.render(BASE_URL=BASE_URL)
with open(os.path.join(OUTPUT_DIR, "about.html"), "w", encoding="utf-8") as f:
    f.write(about_output)

# X. คัดลอก static folder ไปยัง output
static_dir = "static"
if os.path.exists(static_dir):
    shutil.copytree(static_dir, os.path.join(OUTPUT_DIR, "static"), dirs_exist_ok=True)