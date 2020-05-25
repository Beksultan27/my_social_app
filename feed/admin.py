from django.contrib import admin

from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'created_at', 'owner', 'image']


admin.site.register(Post, PostAdmin)
