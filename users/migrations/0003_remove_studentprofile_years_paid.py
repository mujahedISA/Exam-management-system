# Generated by Django 5.2 on 2025-05-01 18:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_studentprofile_generated_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentprofile',
            name='years_paid',
        ),
    ]
