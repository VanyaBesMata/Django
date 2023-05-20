from django.db import models


class Employee(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')


class Position(models.Model):
    position = models.CharField(max_length=50, verbose_name='Должность')
    employee = models.IntegerField(verbose_name='id сотрудника')


class Department(models.Model):
    department = models.CharField(max_length=50, verbose_name='Отдел')
    position = models.CharField(max_length=50, verbose_name='Должность')
    last_name = models.CharField(max_length=50, unique=True, verbose_name='Фамилия')
