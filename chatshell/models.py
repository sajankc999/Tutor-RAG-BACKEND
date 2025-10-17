#for saving responses from user

from django.db import models

class ChatHistory(models.Model):
    user_prompt= models.TextField()
    generated_response = models.TextField()
    generated_time = models.DateTimeField(auto_now_add=True)
