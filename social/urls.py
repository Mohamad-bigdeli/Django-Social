from django.urls import path
from . import views

app_name="social"

urlpatterns = [
    path('home/', views.HomeView.as_view(), name="home"),
    path('post/<slug:tag_slug>/', views.HomeView.as_view(), name="post_list_by_tag"),
    path('post/detail/<pk>', views.PostDetailView.as_view(), name="post_detail"),
    path('search/', views.post_search, name="post_search"),
    path('post/detail/<pk>/comment/', views.comment_post, name="comment"),
    path('profile/', views.ProfileView.as_view(), name="profile"),
    path('create_post/', views.CreatePostView.as_view(), name="create_post"),
    path('post/detail/<pk>/delete_post/', views.delete_post, name="delete_post"),
]