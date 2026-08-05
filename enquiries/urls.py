from django.urls import path
from . import views

urlpatterns = [
    path('', views.enquiry_list, name='enquiry_list'),
    path('reply/<int:id>/', views.reply_enquiry, name='reply_enquiry'),
]