# Generated by Django 2.1 on 2018-12-08 01:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GRXX',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('account', models.CharField(max_length=16)),
                ('password', models.CharField(max_length=64)),
                ('nickname', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='HY',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('f_sid', models.IntegerField()),
                ('f_oid', models.IntegerField()),
                ('f_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chess.GRXX')),
            ],
        ),
        migrations.CreateModel(
            name='PM',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('r_ranking', models.IntegerField()),
                ('r_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chess.GRXX')),
            ],
        ),
        migrations.CreateModel(
            name='SMZ',
            fields=[
                ('c_name', models.CharField(max_length=16)),
                ('c_IDcard', models.IntegerField()),
                ('C_tele', models.IntegerField(primary_key=True, serialize=False)),
                ('c_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chess.GRXX')),
            ],
        ),
        migrations.CreateModel(
            name='ZJ',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('m_sum', models.IntegerField()),
                ('m_victory', models.IntegerField()),
                ('m_draw', models.IntegerField()),
                ('m_defeat', models.IntegerField()),
                ('m_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chess.GRXX')),
            ],
        ),
    ]
