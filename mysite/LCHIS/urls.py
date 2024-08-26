from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("admin/dashboard", views.admin_dashboard, name="admin_dashboard"),
    path("admin/child", views.child_list, name="child_list"),
    path("admin/child_detail/child_id=<int:child_id>/child_form_count=<int:child_form_count>", views.child_detail, name="child_detail"),
    path("admin/child_detail/", views.child_detail, name="child_detail"),

]