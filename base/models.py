from django.db import models

from base.managers import DeletedObjects, ActiveObjects


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    objects = ActiveObjects()
    all_objects = models.Manager()
    deleted_objects = DeletedObjects()

    class Meta:
        abstract = True
