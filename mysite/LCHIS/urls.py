from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    
    path("user/dashboard/", views.user_dashboard, name="user_dashboard"),
    
    path("admin/login", views.admin_login_view, name="admin_login"),
    path("admin/dashboard", views.admin_dashboard, name="admin_dashboard"),
    
    path("admin/child", views.child_list, name="child_list"),
    path("admin/child/search", views.child_list, name="child_search"),
    path("admin/child_detail/", views.child_detail, name="child_detail"),
    path("admin/child_detail/pk=<int:pk>/", views.child_detail, name="child_detail"),
    path("admin/child_detail/pk=<int:pk>/delete_image=<str:delete_image>", views.child_detail, name="child_detail"),
    
    path("admin/gallery", views.gallery_list, name="gallery_list"),
    path("admin/gallery/search", views.gallery_list, name="gallery_search"),
    path("admin/gallery_detail/pk=<int:pk>/", views.gallery_detail, name="gallery_detail"),
    path("admin/gallery_detail/", views.gallery_detail, name="gallery_detail"),
    
    path("admin/vitamin", views.vitamin_list, name="vitamin_list"),
    path("admin/vitamin/search", views.vitamin_list, name="vitamin_search"),
    path("admin/vitamin_detail/pk=<int:pk>/", views.vitamin_detail, name="vitamin_detail"),
    path("admin/vitamin_detail", views.vitamin_detail, name="vitamin_detail"),
    
    path("admin/about_us", views.about_us_list, name="about_us_list"),
    path("admin/about_us/search", views.about_us_list, name="about_us_search"),
    path("admin/about_us_detail/pk=<int:pk>/", views.about_us_detail, name="about_us_detail"),
    path("admin/about_us_detail", views.about_us_detail, name="about_us_detail"),
    
    path("admin/contact_us", views.contact_us_list, name="contact_us_list"),
    path("admin/contact_us/search", views.contact_us_list, name="contact_us_search"),
    path("admin/contact_us_detail/pk=<int:pk>/", views.contact_us_detail, name="contact_us_detail"),
    path("admin/contact_us_detail", views.contact_us_detail, name="contact_us_detail"),
    
    # User paths
    path("registration/", views.user_registration, name="registration"),
    path("home/", views.home, name="home"),
    path("gallery/", views.gallery, name="gallery"),
    path("vitamins/", views.vitamins, name="vitamins"),
    path("about_us/", views.about_us, name="about_us"),
    path("contact_us/", views.contact_us, name="contact_us"),
    path("child_info/", views.child_info, name="child_info"),
    

]