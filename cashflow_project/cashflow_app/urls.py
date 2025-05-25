from django.urls import path
from . import views
from .views import home_view


# Добавление ссылок
urlpatterns = [
   
    path('add/', views.record_create, name='record_create'),
    path('references/', views.manage_reference_data, name='manage_reference'),
    path('references/<str:ref_type>/edit/<int:pk>/', views.edit_reference, name='edit_reference'),
    path('references/<str:ref_type>/delete/<int:pk>/', views.delete_reference, name='delete_reference'),
    path('', views.home_view, name='record_list'),
    path('record/<int:pk>/edit/', views.record_edit, name='record_edit'),
    
    # ajax для создания взаимосвязи между категориями, подкатегориями 
    path('ajax/get-categories/', views.get_categories_by_type, name='get_categories_by_type'),
    path('ajax/get-subcategories/', views.get_subcategories_by_category, name='get_subcategories_by_category'),

]


