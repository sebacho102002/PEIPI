from django.urls import path, re_path
from django.views.generic import TemplateView
from . import views  
from .views import exportar_datos_view

urlpatterns = [
    path('', views.home_page, name='home'),
    path('detail/<int:pk>/', views.entry_detail, name='entry_detail'),
    path('entries/', views.entry_list, name='entry_list'),
    path('entry/new/', views.entry_new, name='entry_new'),
    path('entry/<int:pk>/edit/', views.entry_edit, name='entry_edit'),
    path('entry/<int:pk>/delete/', views.entry_delete, name='entry_delete'),
    path('extracted-data/', views.extracted_data_list, name='extracted_data_list'),
    path('exportar/', exportar_datos_view, name='exportar_datos'),
    path('exportar/ejecutar_scraping/', views.ejecutar_scraping, name='ejecutar_scraping'),

    # URL correcta para robots.txt
    re_path(r'^robots\.txt$', TemplateView.as_view(template_name="robots.txt", content_type="text/plain"), name='robots'),
    
    # Sección de ingeniería de sistemas
    path('ingenieria-sistemas/entries/', views.entry_list, name='ingenieria_sistemas_entries'),
    path('ingenieria-sistemas/entry/<int:pk>/', views.entry_detail, name='entry_detail'),
]
