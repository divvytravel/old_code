# -*- coding: utf-8 -*-

import datetime
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(u"Вид в url", unique=True)

    def __unicode__(self):
        return self.name


class Post(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=250)
    text = models.TextField()
    tags = models.ManyToManyField('trip.Tags', related_name='posts', blank=True, verbose_name=u'Теги')
    slug = models.SlugField(u"Вид в url", unique=True)
    created = models.DateTimeField(default=datetime.datetime.now())

    def __unicode__(self):
        return self.title
