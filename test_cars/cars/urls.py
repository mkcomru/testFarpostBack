# cars/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import car_list, car_detail, car_create, car_edit, car_delete, add_comment, CarListCreateAPIView, CarRetrieveUpdateDestroyAPIView, CommentListCreateAPIView

urlpatterns = [
    path('api/cars/', CarListCreateAPIView.as_view(), name='api-car-list-create'),
    path('api/cars/<int:pk>/', CarRetrieveUpdateDestroyAPIView.as_view(), name='api-car-detail'),
    path('api/comments/', CommentListCreateAPIView.as_view(), name='api-comment-list-create'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', car_list, name='car-list'),
    path('cars/<int:pk>/', car_detail, name='car-detail'),
    path('cars/create/', car_create, name='car-create'),
    path('cars/<int:pk>/edit/', car_edit, name='car-edit'),
    path('cars/<int:car_id>/add_comment/', add_comment, name='add-comment'),
    path('cars/<int:car_id>/delete/', car_delete, name='car-delete'),
]