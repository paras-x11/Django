from django.db import models
from django.contrib.auth.models import User

class Snippet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    code = models.TextField()
    language = models.CharField(max_length=100, default='python')
    linenos = models.BooleanField(default=False)
    style = models.CharField(max_length=50, default='friendly')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    snippet = models.ForeignKey(Snippet, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment: {self.text}, on {self.snippet.title}"