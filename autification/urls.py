from django.urls import path
from autification import views
from django.conf.urls.static import static

urlpatterns = [
    path('login', views.CustomLoginView.as_view(), name = 'login'),
    path('logout', views.CustomLogoutView.as_view(), name = 'logout'),
]