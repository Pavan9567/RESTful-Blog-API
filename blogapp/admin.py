from django.contrib import admin
from .models import *

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ["title"]

class CommentAdmin(admin.ModelAdmin):
    list_display = ["content"]

admin.site.register(Post,PostAdmin)
admin.site.register(Comment,CommentAdmin)
