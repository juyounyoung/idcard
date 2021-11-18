from django.db import models

# Create your models here.
class Board(models.Model):
    # TODO ::: 임의로 모델 만든거라 DB설계대로 다시 만들어야함
    author = models.CharField(max_length=10, null=False)
    title = models.CharField(max_length=100, null=False)
    content = models.TextField(null=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)