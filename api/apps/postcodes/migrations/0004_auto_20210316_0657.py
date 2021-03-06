# Generated by Django 3.1.7 on 2021-03-16 06:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('postcodes', '0003_auto_20210316_0651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='code',
            name='country',
            field=models.CharField(default=django.utils.timezone.now, max_length=80),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='code',
            name='postcode',
            field=models.CharField(default=django.utils.timezone.now, max_length=80),
            preserve_default=False,
        ),
    ]
