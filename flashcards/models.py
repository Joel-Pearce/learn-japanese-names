from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

import math


class Flashcard(models.Model):
    kanji = models.CharField(max_length=10)
    hiragana = models.CharField(max_length=100)
    surname = models.BooleanField(default=False)
    story = models.TextField()
    image = models.CharField(max_length=20)

    def __str__(self):
        return self.kanji


class Deck(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    flashcards = models.ManyToManyField(Flashcard, through="Review")

    def __unicode__(self):
        return self.user


class Review(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, default=None)
    flashcard = models.ForeignKey(Flashcard, on_delete=models.CASCADE)
    last_review_date = models.DateTimeField(default=timezone.now())
    next_review_date = models.DateTimeField(default=timezone.now())
    ready_for_review = models.BooleanField(default=False)
    exponential_time = models.FloatField(default=1)
    exponential_increment = models.FloatField(default=0)
    was_wrong = models.BooleanField(default=False)

    def __unicode__(self):
        return self.flashcard

    def is_ready_for_review(self):
        """Checks whether a flashcard is ready for review.

        If it is, then the 'reader_to_review' variable is set to True, meaning it will appear
        in a user's review dashboard."""
        if self.next_review_date <= timezone.now():
            self.ready_for_review = True
            self.save()
        else:
            self.ready_for_review = False
            self.save()

    def update_review_date(self, is_correct):
        """Updates the next date at which a flashcard is to be reviewed.

        If the user gets the review wrong once, then the flashcard will appear again the next day,
        and the increment by which it will appear is shortened."""
        if is_correct:
            self.last_review_date = timezone.now()
            self.next_review_date = timezone.now() + timedelta(
                days=self.exponential_time
            )
            if not self.was_wrong:
                self.exponential_increment += 1
                self.exponential_time += self.exponential_increment
            else:
                self.next_review_date = timezone.now() + timedelta(1)
                self.exponential_time = math.ceil(self.exponential_time / 2)
                self.exponential_increment = 0
                self.was_wrong = False

        else:
            self.was_wrong = True
        self.is_ready_for_review()
        self.save()
