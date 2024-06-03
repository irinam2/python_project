from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('service/<int:service_id>/', views.service_details, name='service_details'),
    path('add_to_favorite/<int:service_id>/', views.add_to_favorite, name='add_to_favorite'),
    path('remove_from_favorite/<int:service_id>/', views.remove_from_favorite, name='remove_from_favorite'),
]