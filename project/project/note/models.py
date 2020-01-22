from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Label(models.Model):
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='label_owner')
    label = models.CharField(max_length=25)

    def __str__(self):
        return str(self.label)


class Note(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user"
    )
    title = models.CharField(max_length=100)
    note = models.CharField(max_length=250)
    label = models.ManyToManyField(Label)
    date_posted = models.DateTimeField(auto_now_add=True)
    # is_archive = models.BooleanField(default=False)
    # is_trashed = models.BooleanField(default=False)
    # is_pinned = models.BooleanField(default=False)
    # make_copy = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)
