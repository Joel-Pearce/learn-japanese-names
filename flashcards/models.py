from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


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

    def __unicode__(self):
        return self.flashcard

    def is_ready_for_review(self):
        if self.next_review_date <= timezone.now():
            self.ready_for_review = True
            self.save()
        else:
            self.ready_for_review = False
            self.save()

    def update_review_date(self, is_correct):
        if is_correct:
            self.last_review_date = timezone.now()
            self.next_review_date = timezone.now() + timedelta(
                days=float(self.exponential_time)
            )
            self.exponential_time += 1
        self.is_ready_for_review()
        self.save()
