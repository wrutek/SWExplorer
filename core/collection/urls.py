from django.urls import path

from . import views

app_name = 'collection'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('fetch/', views.FetchView.as_view(), name='fetch'),
    path('details/<int:dataset_id>/', views.DetailsView.as_view(), name='details'),
    path('value-count/<int:dataset_id>/', views.ValueCountView.as_view(), name='value_count'),
]