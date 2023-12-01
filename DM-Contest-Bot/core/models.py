from django.db import models

class Entity(models.Model):

    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
    