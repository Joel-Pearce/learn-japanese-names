import pandas as pd
from django.core.management.base import BaseCommand
from flashcards.models import Flashcard


class Command(BaseCommand):
    help = "Populate Flashcard model from CSV file"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str, help="Path to the CSV file")

    def handle(self, *args, **options):
        csv_file = options["csv_file"]

        # Use pandas to read the CSV file
        try:
            df = pd.read_csv(csv_file)
        except pd.errors.EmptyDataError:
            self.stdout.write(
                self.style.SUCCESS("CSV file is empty. No records to import.")
            )
            return

        # Iterate through each row in the DataFrame and create Flashcard objects
        for index, row in df.iterrows():
            Flashcard.objects.create(
                kanji=row["kanji"],
                hiragana=row["hiragana"],
                surname=row["surname"],
                story=row["story"],
                image=row["image"],
            )

        self.stdout.write(
            self.style.SUCCESS(f"Successfully imported data from {csv_file}")
        )
