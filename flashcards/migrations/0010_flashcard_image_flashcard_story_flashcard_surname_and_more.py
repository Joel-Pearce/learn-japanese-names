# Generated by Django 4.2.3 on 2023-12-27 15:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("flashcards", "0009_alter_review_last_review_date_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="flashcard",
            name="image",
            field=models.ImageField(null=True, upload_to=""),
        ),
        migrations.AddField(
            model_name="flashcard",
            name="story",
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name="flashcard",
            name="surname",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="review",
            name="last_review_date",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 12, 27, 15, 49, 23, 913406, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.AlterField(
            model_name="review",
            name="next_review_date",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 12, 27, 15, 49, 23, 913419, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
