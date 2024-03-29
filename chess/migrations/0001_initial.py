# Generated by Django 2.1.3 on 2018-12-31 18:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('f_sid', models.IntegerField()),
                ('f_oid', models.IntegerField()),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('rnum', models.AutoField(primary_key=True, serialize=False)),
                ('state', models.CharField(choices=[('0', 'empty'), ('1', 'wait'), ('2', 'full')], default='wait', max_length=16)),
                ('blue', models.ForeignKey(max_length=16, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='blue', to=settings.AUTH_USER_MODEL)),
                ('red', models.ForeignKey(max_length=16, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='red', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=16)),
                ('rname', models.CharField(max_length=16)),
                ('idcard', models.CharField(max_length=18)),
                ('tele', models.CharField(max_length=11)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Victory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.IntegerField(default=0)),
                ('victory', models.IntegerField(default=0)),
                ('draw', models.IntegerField(default=0)),
                ('defeat', models.IntegerField(default=0)),
                ('score', models.IntegerField(default=1000)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
