# Generated by Django 4.2.3 on 2024-01-07 16:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("flashcards", "0011_alter_flashcard_image_alter_flashcard_story_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="review",
            name="last_review_date",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 1, 7, 16, 55, 47, 490364, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.AlterField(
            model_name="review",
            name="next_review_date",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 1, 7, 16, 55, 47, 490376, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
