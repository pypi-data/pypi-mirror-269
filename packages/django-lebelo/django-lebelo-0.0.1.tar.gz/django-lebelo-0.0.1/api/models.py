from django.db import models


class Permission(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class DeveloperAccount(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    api_key = models.CharField(max_length=40, unique=True)
    is_active = models.BooleanField(default=True)
    permissions = models.ManyToManyField(Permission)

    def __str__(self):
        return self.name
