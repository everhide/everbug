from django.db import models


class CustomEntity(models.Model):
    item = models.CharField(max_length=30)

    def __str__(self):
        return self.item

    class Meta:
        abstract = True
        managed = False


class Entity(CustomEntity):
    class Meta:
        db_table = 'def_entity'


class AltEntity(CustomEntity):
    class Meta:
        db_table = 'alt_entity'
