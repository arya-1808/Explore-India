from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path('edit/<int:id>/', views.edit_destination, name='edit_destination'),
    path('delete/<int:id>/', views.delete_destination, name='delete_destination'),
]
