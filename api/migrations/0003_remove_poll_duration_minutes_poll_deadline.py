# Generated by Django 4.2.3 on 2023-07-11 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_userprofile_delete_member'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='poll',
            name='duration_minutes',
        ),
        migrations.AddField(
            model_name='poll',
            name='deadline',
            field=models.DateTimeField(default='2023-07-12 22:47:03.971633'),
            preserve_default=False,
        ),
    ]
