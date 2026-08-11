from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    # User
    path(
        '',
        views.user_reviews,
        name='user_reviews'
    ),

    path(
        'add/',
        views.add_review,
        name='add_review'
    ),

    # Admin
    path(
        'admin-reviews/',
        views.admin_reviews,
        name='admin_reviews'
    ),

    # Delete
    path(
        'delete/<int:review_id>/',
        views.delete_review,
        name='delete_review'
    ),
]