from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from account import Account as _Account
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

    def auto_get_bars(self):
        """
        get bars and create sign_status
        :return:
        """
        _account = _Account(self.uid, self.pwd)
        _account.get_bars()
        print _account.like_tiebas
        for bar in _account.like_tiebas:
            cur_bar, dummy = Bar.objects.get_or_create(
                name = bar['name'],
                link = bar['link']
            )
            new_sign_status = SignStatus.objects.create(
                 account = self,
                 bar = cur_bar,
                 signed = False,
            )
            new_sign_status.save()
            cur_bar.bar_sign_status.add(new_sign_status)
            cur_bar.save()
            self.account_sign_status.add(new_sign_status)
            self.bars.add(cur_bar)
        self.save()



class SignStatus(models.Model):
    signed = models.BooleanField(default=False)
    bar = models.ForeignKey(Bar, related_name='bar_sign_status')
    account = models.ForeignKey(Account, related_name='account_sign_status')

    def __unicode__(self):
        return u'%s in %s' % (self.account.uid, self.bar.name)

admin.site.register(Bar)
admin.site.register(Account)
admin.site.register(SignStatus)
