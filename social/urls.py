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
    path('communities/filter/',views.SearchCommunitiesView.as_view(), name='communities_filter'),
    path('<int:pk>/like_post/', views.LikePostView.as_view(), name='like_post'),
    path('<int:pk>/like_comment/', views.LikeCommentView.as_view(), name='like_comment'),
    path('<int:community_pk>/subscribe', views.SubscribeView.as_view(), name = 'subscribe'),
    path('<int:community_pk>/discusion/create/', views.DiscucsionCreateView.as_view(), name = 'discusion_create'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)