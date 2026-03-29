from django.db import models
from django.contrib.auth.models import User


class Conversation(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="conversations",
        null=True,
        blank=True
    )

    title = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or "New Chat"


class ChatMessage(models.Model):

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages"
    )

    role = models.CharField(max_length=10)
    message = models.TextField()

    edited = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)