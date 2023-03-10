# Generated by Django 3.2.18 on 2023-03-02 10:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('hr', '0004_alter_employee_contact'),
    ]

    operations = [
        migrations.CreateModel(
            name='Compensation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='employee',
            name='compensations',
            field=models.ManyToManyField(to='hr.Compensation'),
        ),
    ]
