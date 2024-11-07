from django.urls import path
from social import views
from django.conf.urls.static import static
from Social_system import settings

urlpatterns = [
    path('communities/', views.ComunitiesListView.as_view(), name='communities'),
    path('community/<int:pk>/', views.CommunityDetailView.as_view(), name = 'community'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name = 'post_detail'),
    path('discusion/<int:pk>/', views.DiscusionDetailView.as_view(), name = 'discusion'),
    path('<int:community_pk>/post/create/', views.PostCreateView.as_view(), name='post_create'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)