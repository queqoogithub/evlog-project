from django.contrib import admin

# Register your models here.
from .models import Post, About

# TINY new # Overriding a form to use our TinyMCE widget 
from tinymce.widgets import TinyMCE
from django.db import models

#admin.site.register(Post)

# Custom User Model
class PostAdmin(admin.ModelAdmin):

    fieldsets = [
        ("Title / Author / Date", {'fields': ["title", "title_image", "author", "date"]}),
        ("Text", {"fields": ["text"]})
    ]

    formfield_overrides = { # TINY new
        models.TextField : {'widget': TinyMCE()},
    }

class AboutAdmin(admin.ModelAdmin): # new
    fieldsets = [
        ("About Title", {'fields': ["title"]}),
        ("About Text", {"fields": ["text"]})
    ]

    formfield_overrides = { # TINY new
        models.TextField : {'widget': TinyMCE()},
    }

admin.site.register(Post,PostAdmin)
admin.site.register(About,AboutAdmin) # new
