# Generated by Django 4.2.1 on 2023-06-03 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fest', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='festmodel',
            name='about',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='festmodel',
            name='removed',
            field=models.BooleanField(default=False),
        ),
    ]
