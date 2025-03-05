from django.db import models
from django.contrib.auth.models import User


# Message model to store sender, receiver, message content and timestamp.
class Message(models.Model):
    sender = models.ForeignKey(
        User,
        related_name='sent_messages',
        on_delete=models.CASCADE
        )
    receiver = models.ForeignKey(
        User,
        related_name='received_messages',
        on_delete=models.CASCADE
    )
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    # Shows who sent the message, who received it, and a short preview.
    def __str__(self):
        return (
            f"{self.sender.username} → {self.receiver.username}: "
            f"{self.message[:30]}"
        )
