from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("admin/dashboard", views.admin_dashboard, name="admin_dashboard"),
    path("admin/child", views.child_list, name="child_list"),
    path("admin/child_detail/", views.child_detail, name="child_detail"),
    path("admin/child_detail/pk=<int:pk>/", views.child_detail, name="child_detail"),
    path("admin/child_detail/pk=<int:pk>/delete_image=<str:delete_image>", views.child_detail, name="child_detail"),
    path("admin/gallery", views.gallery_list, name="gallery_list"),
    path("admin/gallery_detail/pk=<int:pk>/", views.gallery_detail, name="gallery_detail"),
    path("admin/gallery_detail/", views.gallery_detail, name="gallery_detail"),
    path("user/dashboard/", views.user_dashboard, name="user_dashboard"),
]