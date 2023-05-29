# Generated by Django 3.2.12 on 2023-05-28 17:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Flashcard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kanji', models.CharField(max_length=10)),
                ('hiragana', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_review_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('next_review_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('flashcard', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flashcards.flashcard')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
