# Generated by Django 3.2.18 on 2023-03-10 05:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('customauth', '0004_delete_task'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='标签名字',
        ),
        migrations.AddField(
            model_name='tag',
            name='name',
            field=models.CharField(default="", help_text='标签名字', max_length=64),
            preserve_default=False,
        ),
    ]