from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    # Authentication Urls
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name="logout"),
    path("password/", views.PasswordsChangeView.as_view()),
    # Post Detail Url
    path('post/<int:pk>', views.PostDetailView.as_view(), name='post-detail'),
    # Posts by Author
    path('blogger/<int:pk>',
         views.PostListbyAuthorView.as_view(),
         name='posts-by-author'),
    # Post Comment View
    path('post/<int:pk>/comment/',
         views.PostCommentCreate.as_view(),
         name='post_comment'),
    # About View
    path('about/', views.about),
    # Contact View
    path('contact/', views.contact),
]
