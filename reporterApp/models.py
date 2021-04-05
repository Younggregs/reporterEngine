# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
import pytz


class Account(models.Model):
    name = models.CharField(max_length = 350)
    email = models.EmailField()
    password = models.CharField(max_length = 350)
    isSuperUser = models.BooleanField(default = False)
    date = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return str(self.name)
    
    class Meta:
        ordering = ['-date']


class Location(models.Model):
    name = models.CharField(max_length = 350)
    date = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return str(self.name)
    
    class Meta:
        ordering = ['-date']


class Category(models.Model):
    name = models.CharField(max_length = 350)
    date = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return str(self.name)
    
    class Meta:
        ordering = ['-date']


class Impact(models.Model):
    name = models.CharField(max_length = 350)
    date = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return str(self.name)
    
    class Meta:
        ordering = ['-date']



class Report(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    impact = models.ForeignKey(Impact, on_delete=models.CASCADE)
    reportType = models.BooleanField()
    description = models.TextField()
    deed = models.TextField()
    report_date = models.DateField(default = timezone.now)
    date = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return str(self.deed)
    
    class Meta:
        ordering = ['-date']