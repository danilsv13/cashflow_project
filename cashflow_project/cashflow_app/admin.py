from django.contrib import admin
from .models import Status, Type, Category, SubCategory, CashflowRecord


# Регистрация моделей в админке с отображением полей id и name
@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type')
    list_filter = ('type',)
    search_fields = ('name',)

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)

# Отображение записей ДДС в админке с фильтрацией и поиском по комментарию
@admin.register(CashflowRecord)
class CashflowRecordAdmin(admin.ModelAdmin):
    list_display = ('manual_date', 'status', 'type', 'category', 'subcategory', 'amount', 'comment')
    list_filter = ('status', 'type', 'category', 'subcategory', 'manual_date')
    search_fields = ('comment',)
