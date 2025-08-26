from django.contrib import admin
from .models import Repository

@admin.register(Repository)
class RepositoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'stars', 'language', 'keyword', 'created_at')
    search_fields = ('name', 'full_name', 'keyword', 'owner')
    list_filter = ('language',)
