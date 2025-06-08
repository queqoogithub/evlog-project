import os
import markdown
import frontmatter
from datetime import datetime
from collections import defaultdict
from jinja2 import Environment, FileSystemLoader

CONTENT_DIR = "content"
OUTPUT_DIR = "output"
TEMPLATES_DIR = "templates"

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
        
        html_body = markdown.markdown(post.content)
        slug = os.path.splitext(filename)[0]

        # แปลงวันที่จาก string -> datetime
        date_str = post.get("date", "2000-01-01")
        date = datetime.strptime(date_str, "%Y-%m-%d")

        post_data = {
            "title": post.get("title", "Untitled"),
            "tags": post.get("tags", []),
            "date": date,
            "content": html_body,
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
    rendered = post_template.render(post=post)
    with open(os.path.join(OUTPUT_DIR, f"{post['slug']}.html"), "w") as f:
        f.write(rendered)

# 3. สร้าง tag pages
tag_dir = os.path.join(OUTPUT_DIR, "tags")
os.makedirs(tag_dir, exist_ok=True)

for tag, tagged_posts in tags_dict.items():
    rendered = tag_template.render(tag=tag, posts=tagged_posts)
    with open(os.path.join(tag_dir, f"{tag}.html"), "w") as f:
        f.write(rendered)

print("✅ Static site generated!")

# 4. สร้าง index.html + page2.html + ...
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
homepage_template = env.get_template("homepage.html")
latest_posts = posts[:3]  # เอาโพสต์ใหม่สุด 3 อัน

homepage_rendered = homepage_template.render(posts=latest_posts)

with open(os.path.join(OUTPUT_DIR, "homepage.html"), "w") as f:
    f.write(homepage_rendered)
