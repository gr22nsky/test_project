from django.db import models

class AI_Friend(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

class Conversation(models.Model):
    user_id = models.IntegerField()
    ai_friend = models.ForeignKey(AI_Friend, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation with {self.ai_friend.name} at {self.created_at}"
