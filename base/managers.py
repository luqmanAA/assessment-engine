from django.db import models


class ActiveObjects(models.Manager):
    def get_queryset(self):
        return super(ActiveObjects, self).get_queryset().filter(is_deleted=False)


class DeletedObjects(models.Manager):
    def get_queryset(self):
        return super(DeletedObjects, self).get_queryset().filter(is_deleted=True)
