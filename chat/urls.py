from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    path("", views.home),

    path("create/", views.create_conversation),
    path("ask/", views.ask_ai),
    path("messages/<int:convo_id>/", views.load_messages),
    path("delete/<int:convo_id>/", views.delete_conversation),
    path("edit/<int:msg_id>/", views.edit_message),

    path("accounts/login/", auth_views.LoginView.as_view(template_name="login.html")),
    path("accounts/logout/", auth_views.LogoutView.as_view()),

]