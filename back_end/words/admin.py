from django.contrib import admin

from .models import Word, Category


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ('id', 'eng_word', 'ukr_word', 'category')
    list_display_links = ('id', 'eng_word')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')

