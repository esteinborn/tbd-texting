# Generated by Django 2.0.3 on 2018-04-02 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twilio_mgr', '0009_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='message',
            field=models.CharField(max_length=1000, unique=True),
        ),
    ]
