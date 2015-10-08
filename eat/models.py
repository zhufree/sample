from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
# Create your models here.


class Restaurant(models.Model):
    name = models.CharField(max_length=20)
    count = models.BigIntegerField(default=0)
    user = models.ForeignKey(User, related_name='like_restaurant')

    def __unicode__(self):
        return u'%s' % self.name

admin.site.register(Restaurant)
