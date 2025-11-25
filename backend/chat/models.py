from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Room(models.Model):
    """
    Room Model
    """
    id = models.AutoField(primary_key=True)  # auto-incrementing ID
    name = models.CharField(max_length=255, blank=True)  # name of the room
    last_message_at = models.DateTimeField(default=timezone.now)  # last message timestamp
    is_private = models.BooleanField(default=False)  # if the room is private

    def __str__(self):
        if self.name:
            return self.name
        return f"Room {self.id}"


class Message(models.Model):
    """
    Message Model
    """
    id = models.AutoField(primary_key=True)  # auto-incrementing ID
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')  # room

    # sender and receiver define
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )

    content = models.TextField()  # message content
    timestamp = models.DateTimeField(default=timezone.now)  # message timestamp

    #  ordering
    class Meta:
        ordering = ['timestamp']
