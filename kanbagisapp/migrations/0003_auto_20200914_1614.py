# Generated by Django 2.0.7 on 2020-09-14 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kanbagisapp', '0002_userprofile_confirmed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='informed',
            field=models.BooleanField(default=False, help_text='Bilgili kullanıcı'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='privacy',
            field=models.BooleanField(default=False, help_text='Gizlilik'),
        ),
    ]
