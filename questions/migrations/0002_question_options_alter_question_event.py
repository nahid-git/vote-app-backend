# Generated by Django 4.1 on 2024-01-24 19:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('options', '0002_remove_option_question'),
        ('events', '0003_alter_vote_unique_together'),
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='options',
            field=models.ManyToManyField(related_name='options', to='options.option'),
        ),
        migrations.AlterField(
            model_name='question',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='events.event'),
        ),
    ]
