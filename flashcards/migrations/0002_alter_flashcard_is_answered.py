# Generated by Django 5.1.5 on 2025-01-23 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flashcards', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flashcard',
            name='is_answered',
            field=models.BooleanField(default=False),
        ),
    ]
