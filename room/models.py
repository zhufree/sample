# -*-coding:utf-8-*-
from django.db import models

# Create your models here.
class Booking(models.Model):
    year=models.CharField(max_length=10,verbose_name="年")
    month= models.CharField(max_length=10, verbose_name="月")
    day = models.CharField(max_length=10, verbose_name="日")
    hour = models.CharField(max_length=10, verbose_name="时")
    minute = models.CharField(max_length=10, verbose_name="分")
    area = models.CharField(max_length=10, verbose_name="预约区")
    room = models.CharField(max_length=10, verbose_name="房间号")
    def __unicode__(self):
	 return u'%s,%s,%s,%s' %(self.area,self.room,self.hour,self.minute)
