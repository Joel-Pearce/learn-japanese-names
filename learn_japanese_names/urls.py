from django.urls import path
from django.contrib.auth import views as auth_views
from flashcards import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("signup/", views.signup, name="signup"),
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("learn/", views.learn_dashboard, name="learn"),
    path("review/", views.review_dashboard, name="review"),
    path("dashboard/", views.general_dashboard, name="dashboard"),
    path("story/", views.story, name="story"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
