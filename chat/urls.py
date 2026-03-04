from django.urls import path
from . import views

urlpatterns = [

    path("", views.home),

    path("create/", views.create_conversation),

    path("ask/", views.ask_ai),

    path("messages/<int:convo_id>/", views.load_messages),

]