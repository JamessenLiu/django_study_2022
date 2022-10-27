import time

from django.db import models


class BaseModel(models.Model):
    created_at = models.IntegerField()
    updated_at = models.IntegerField()
    format_created_at = models.DateTimeField(auto_now=True)
    format_updated_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        time_now = int(time.time())
        if self.pk:
            self.updated_at = time_now
        else:
            self.created_at = time_now
            self.updated_at = time_now

        super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True
