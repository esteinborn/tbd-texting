# Generated by Django 2.0.3 on 2018-04-28 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twilio_mgr', '0024_auto_20180420_1701'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='subject',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
    ]