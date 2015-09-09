from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
# Create your models here.


class Bar(models.Model):
    name = models.CharField(max_length=20, unique=True)
    link = models.URLField(unique=True)
    fid = models.BigIntegerField(null=True, unique=True)
    tbs = models.CharField(max_length=30, null=True)

    def __unicode__(self):
        return u'%s' % self.name


class Account(models.Model):
    uid = models.CharField(max_length=10)
    pwd = models.CharField(max_length=30)
    bars = models.ManyToManyField(Bar, related_name='bar_has_accounts', null=True)
    user = models.ForeignKey(User, related_name='user_has_accounts', null=True)

    def __unicode__(self):
        return u'%s' % self.uid

    #def login(self):


class Sign_status(models.Model):
    signed = models.BooleanField(default=False)
    bar = models.ForeignKey(Bar, related_name='bar_sign_status')
    account = models.ForeignKey(Account, related_name='account_sign_status')

    def __unicode__(self):
        return u'%s in %s' % (self.account.uid, self.bar.name)

admin.site.register(Bar)
admin.site.register(Account)
admin.site.register(Sign_status)
