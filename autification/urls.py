from django.urls import path
from autification import views
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name = 'login'),
    path('logout/', LogoutView.as_view(), name = 'logout'),
    path('profile/<int:pk>/', views.ProfileDetailView.as_view(), name='profile_detail'),
    path('register/', views.RegisterView.as_view(), name = 'register'),
    path('profile/create/', views.ProfileCreateView.as_view(), name='profile_create'),
    path('profile/update/<int:pk>', views.ProfileUpdateView.as_view(), name = 'profile_update'),
]