from django.urls import path

from apps.platform.accounts import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.RoleLoginView.as_view(), name="login"),
    path("logout/", views.RoleLogoutView.as_view(), name="logout"),
]