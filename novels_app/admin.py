from django.contrib import admin
from .models import Category, Novel, Episode
from django.contrib.auth.models import Group, User


class EpisodeInline(admin.TabularInline):
    model = Episode
    fields = ('episode_number', 'title', 'file', 'uploaded_at')
    readonly_fields = ('uploaded_at',)
    extra = 0
    ordering = ('episode_number',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Novel)
class NovelAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_at')
    search_fields = ('title', 'author')
    list_filter = ('category',)
    inlines = [EpisodeInline]
    save_on_top = True

@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('novel', 'episode_number', 'title', 'uploaded_at')
    search_fields = ('title', 'novel__title')
    list_filter = ('novel__category',)


