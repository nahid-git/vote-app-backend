# Generated by Django 4.1 on 2024-01-26 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_emailconfirmationmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='student_id',
            field=models.CharField(max_length=16),
        ),
    ]
