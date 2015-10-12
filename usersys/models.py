from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin


# Create your models here.
class StudentAcc(models.Model):
    sid = models.BigIntegerField(unique=True, blank=False, null=False)
    pwd = models.BigIntegerField(blank=False, null=False)
    user = models.ForeignKey(User, related_name='has_student_account')

    def __unicode__(self):
        return u'%s' % self.sid

admin.site.register(StudentAcc)