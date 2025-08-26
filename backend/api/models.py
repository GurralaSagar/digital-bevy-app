from django.db import models

class Repository(models.Model):
    keyword = models.CharField(max_length=200, db_index=True)
    name = models.CharField(max_length=250)
    full_name = models.CharField(max_length=300, null=True, blank=True)
    url = models.URLField(unique=True)
    description = models.TextField(null=True, blank=True)
    language = models.CharField(max_length=100, null=True, blank=True)
    stars = models.IntegerField(default=0)
    owner = models.CharField(max_length=150, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=['keyword', 'stars'])]

    def __str__(self) -> str:
        return self.full_name or self.name
