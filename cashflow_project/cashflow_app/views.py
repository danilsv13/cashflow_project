from django.shortcuts import render
from .models import CashflowRecord

# Упрощенное отображение всех записей ДДС (не используется фильтр)
def record_list(request):
    records = CashflowRecord.objects.all().select_related('status', 'type', 'category', 'subcategory')
    return render(request, 'record_list.html', {'records': records})

from django.shortcuts import render, redirect
from .forms import CashflowRecordForm

# Обработка формы создания новой записи
def record_create(request):
    if request.method == 'POST':
        form = CashflowRecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('record_list')
    else:
        form = CashflowRecordForm()
    return render(request, 'record_form.html', {'form': form})

from .models import Status, Type, Category, SubCategory
from .forms import StatusForm, TypeForm, CategoryForm, SubCategoryForm

# Обработчик создания новых элементов справочников
def manage_reference_data(request):
    status_form = StatusForm(request.POST or None, prefix='status')
    type_form = TypeForm(request.POST or None, prefix='type')
    category_form = CategoryForm(request.POST or None, prefix='category')
    subcategory_form = SubCategoryForm(request.POST or None, prefix='subcategory')

    if request.method == 'POST':
        if 'submit_status' in request.POST and status_form.is_valid():
            status_form.save()
            return redirect('manage_reference')
        elif 'submit_type' in request.POST and type_form.is_valid():
            type_form.save()
            return redirect('manage_reference')
        elif 'submit_category' in request.POST and category_form.is_valid():
            category_form.save()
            return redirect('manage_reference')
        elif 'submit_subcategory' in request.POST and subcategory_form.is_valid():
            subcategory_form.save()
            return redirect('manage_reference')


    context = {
        'status_form': status_form,
        'type_form': type_form,
        'category_form': category_form,
        'subcategory_form': subcategory_form,
        'statuses': Status.objects.all(),
        'types': Type.objects.all(),
        'categories': Category.objects.all(),
        'subcategories': SubCategory.objects.all(),
    }
    return render(request, 'manage_reference_data.html', context)



MODEL_FORM_MAP = {
    'status': (Status, StatusForm, 'Редактировать статус'),
    'type': (Type, TypeForm, 'Редактировать тип'),
    'category': (Category, CategoryForm, 'Редактировать категорию'),
    'subcategory': (SubCategory, SubCategoryForm, 'Редактировать подкатегорию'),
}

from django.shortcuts import render, redirect, get_object_or_404


# Обработчик удаления и редактирования справочника
def edit_reference(request, ref_type, pk):
    if ref_type not in MODEL_FORM_MAP:
        raise Http404("Неверный тип справочника")

    model, form_class, title = MODEL_FORM_MAP[ref_type]
    instance = get_object_or_404(model, pk=pk)

    if request.method == 'POST':
        form = form_class(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('manage_reference')
    else:
        form = form_class(instance=instance)

    return render(request, 'edit_reference_item.html', {'form': form, 'title': title})

def delete_reference(request, ref_type, pk):
    if ref_type not in MODEL_FORM_MAP:
        raise Http404("Неверный тип справочника")

    model, _, _ = MODEL_FORM_MAP[ref_type]
    instance = get_object_or_404(model, pk=pk)
    instance.delete()
    return redirect('manage_reference')




from .forms import RecordFilterForm
from .models import CashflowRecord

# Главная страница с отображением записей и фильтрацией
def home_view(request):

    if request.method == 'POST' and 'delete_record_id' in request.POST:
        record_id = request.POST.get('delete_record_id')
        record = get_object_or_404(CashflowRecord, id=record_id)
        record.delete()
        return redirect('record_list')  # Перенаправление на главную
    
    records = CashflowRecord.objects.all()
    filter_form = RecordFilterForm(request.GET or None)

    if filter_form.is_valid():
        cd = filter_form.cleaned_data
        if cd['date_from']:
            records = records.filter(manual_date__gte=cd['date_from'])
        if cd['date_to']:
            records = records.filter(manual_date__lte=cd['date_to'])
        if cd['status']:
            records = records.filter(status=cd['status'])
        if cd['type']:
            records = records.filter(type=cd['type'])
        if cd['category']:
            records = records.filter(category=cd['category'])
        if cd['subcategory']:
            records = records.filter(subcategory=cd['subcategory'])

    return render(request, 'record_list.html', {
        'records': records,
        'filter_form': filter_form,
    })


from django.http import JsonResponse
from .models import Category, SubCategory

# Ajax-запросы для создания взаимосвязей между полями
def get_categories_by_type(request):
    type_id = request.GET.get('type_id')
    categories = Category.objects.filter(type_id=type_id).values('id', 'name')
    return JsonResponse({'categories': list(categories)})

def get_subcategories_by_category(request):
    category_id = request.GET.get('category_id')
    subcategories = SubCategory.objects.filter(category_id=category_id).values('id', 'name')
    return JsonResponse({'subcategories': list(subcategories)})

from django.shortcuts import render, get_object_or_404, redirect
from .models import CashflowRecord

from .forms import CashflowRecordForm


# Редактор записей на главной странице
def record_edit(request, pk):
    record = get_object_or_404(CashflowRecord, pk=pk)
    if request.method == 'POST':
        form = CashflowRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('record_list')
    else:
        form = CashflowRecordForm(instance=record)
    return render(request, 'record_edit.html', {'form': form})
