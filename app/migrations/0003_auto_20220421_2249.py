# Generated by Django 3.2.13 on 2022-04-21 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20220421_2225'),
    ]

    operations = [
        migrations.AddField(
            model_name='passmodel',
            name='pass_img',
            field=models.ImageField(blank=True, null=True, upload_to='pass/'),
        ),
        migrations.AddField(
            model_name='passmodel',
            name='qr',
            field=models.ImageField(blank=True, null=True, upload_to='qr'),
        ),
    ]
