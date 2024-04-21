from django.contrib import admin
from django.db import models

from .models import Portfolio, Category, Post, Profile
from mdeditor.widgets import MDEditorWidget


class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'filter')
    search_fields = ['title']


admin.site.register(Category)
admin.site.register(Portfolio, PortfolioAdmin)


class PostModelAdmin (admin.ModelAdmin):
    prepopulated_fields = {"slug": ["title"]}
    formfield_overrides = {
        models.TextField: {'widget': MDEditorWidget}
    }


admin.site.register(Post, PostModelAdmin)
admin.site.register(Profile)