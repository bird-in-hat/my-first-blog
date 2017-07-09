from django.db import models

# Create your models here.
from django.utils.timezone import now


class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateTimeField(default=now())
    publish_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.publish_date = now()
        self.save()

    def __str__(self):
        return self.title
