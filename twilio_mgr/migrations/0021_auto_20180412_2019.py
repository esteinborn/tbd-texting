# Generated by Django 2.0.3 on 2018-04-12 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twilio_mgr', '0020_emailreminder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='keyword',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='message',
            field=models.CharField(max_length=400),
        ),
    ]