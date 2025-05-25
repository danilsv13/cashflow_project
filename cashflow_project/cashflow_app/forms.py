from django import forms
from .models import CashflowRecord, Status, Type, Category, SubCategory

# Форма для добавления/редактирования записей ДДС
class CashflowRecordForm(forms.ModelForm):
    class Meta:
        model = CashflowRecord
        fields = ['manual_date', 'status', 'type', 'category', 'subcategory', 'amount', 'comment']
        labels = {
            'manual_date': 'Дата',
            'status': 'Статус',
            'type': 'Тип',
            'category': 'Категория',
            'subcategory': 'Подкатегория',
            'amount': 'Сумма',
            'comment': 'Комментарий',
        }
        widgets = {
            'manual_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'subcategory': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].empty_label = 'Выберите статус'
        self.fields['type'].empty_label = 'Выберите тип'
        self.fields['category'].empty_label = 'Выберите категорию'
        self.fields['subcategory'].empty_label = 'Выберите подкатегорию'

# Формы для справочника: статус, типы, категории и тд.. 
class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']
        labels = {'name': 'Название статуса'}
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class TypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = ['name']
        labels = {'name': 'Название типа'}
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'type']
        labels = {
            'name': 'Название категории',
            'type': 'Тип',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
        }

class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ['name', 'category']
        labels = {
            'name': 'Название подкатегории',
            'category': 'Категория',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }


from django import forms
from .models import Status, Type, Category, SubCategory


# Форма фильтрации записей на главной странице
class RecordFilterForm(forms.Form):
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='С даты'
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='По дату'
    )
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        required=False,
        label='Статус',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    type = forms.ModelChoiceField(
        queryset=Type.objects.all(),
        required=False,
        label='Тип',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        label='Категория',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    subcategory = forms.ModelChoiceField(
        queryset=SubCategory.objects.all(),
        required=False,
        label='Подкатегория',
        widget=forms.Select(attrs={'class': 'form-select'})
    )


from django import forms
from .models import Record

class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['manual_date', 'status', 'type', 'category', 'subcategory', 'amount', 'comment']
