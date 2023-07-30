from datetime import datetime, timedelta
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Flashcard(models.Model):
    kanji = models.CharField(max_length=10)
    hiragana = models.CharField(max_length=25)

    def __str__(self):
        return self.kanji


class Deck(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    flashcards = models.ManyToManyField(Flashcard, through="Review")

    def __str__(self):
        return f"Deck for {self.user.username}"


class Review(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, default=None)
    flashcard = models.ForeignKey(Flashcard, on_delete=models.CASCADE)
    last_review_date = models.DateTimeField(default=datetime.now)
    next_review_date = models.DateTimeField(default=datetime.now)
    ready_for_review = models.BooleanField(default=False)

    def __str__(self):
        return f"Review for {self.flashcard.kanji}"

    def update_review_date(self, is_correct):
        if is_correct:
            self.last_review_date = datetime.now()
            self.next_review_date = self.last_review_date + timedelta(days=1)
        else:
            self.next_review_date = datetime.now()
        self.ready_for_review = False
        self.save()

    def is_ready_for_review(self):
        if self.next_review_date <= datetime.now():
            self.ready_for_review = True
