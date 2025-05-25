from django.db import models

class Status(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"

class Type(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип"
        verbose_name_plural = "Типы"

class Category(models.Model):
    name = models.CharField(max_length=50)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        if self.type:
            return f"{self.name} ({self.type.name})"
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class SubCategory(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.category.name})"

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"

class CashflowRecord(models.Model):
    created_at = models.DateField(auto_now_add=True)
    manual_date = models.DateField(null=True, blank=True)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)
    type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.manual_date or self.created_at} — {self.amount}₽"

    class Meta:
        verbose_name = "Запись ДДС"
        verbose_name_plural = "Записи ДДС"

from django.db import models

class Record(models.Model):
    manual_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey('Status', on_delete=models.CASCADE)
    type = models.ForeignKey('Type', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    subcategory = models.ForeignKey('Subcategory', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"{self.manual_date or self.created_at} - {self.amount} ₽"
