from datetime import date

from django.db import models


class Compensation(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return "%s" % self.name


class Contact(models.Model):
    phone = models.CharField(max_length=50, unique=True)
    address = models.CharField(max_length=50)

    def __str__(self):
        return "%s" % self.phone


class Department(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return "%s" % self.name


class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    contact = models.OneToOneField(Contact, on_delete=models.CASCADE, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True)
    compensations = models.ManyToManyField(Compensation)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)


class Job(models.Model):
    title = models.CharField(max_length=255)
    employees = models.ManyToManyField(Employee, through='Assignment')

    def __str__(self):
        return "%s" % self.title


class Assignment(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    position = models.ForeignKey(Job, on_delete=models.CASCADE)
    begin_date = models.DateField()
    end_date = models.DateField(default=date(2055, 12, 31))
