# Generated by Django 3.0.5 on 2020-04-07 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('text', models.TextField(max_length=400)),
                ('OTP', models.CharField(max_length=250)),
                ('to', models.CharField(max_length=12)),
                ('sms_time', models.DateTimeField()),
            ],
        ),
    ]
