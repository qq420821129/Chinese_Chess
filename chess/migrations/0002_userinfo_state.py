# Generated by Django 2.1.4 on 2019-01-03 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chess', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='state',
            field=models.CharField(choices=[('0', 'wait'), ('1', 'outline'), ('2', 'waitready'), ('3', 'ready'), ('4', 'playing')], default='outline', max_length=10),
        ),
    ]
