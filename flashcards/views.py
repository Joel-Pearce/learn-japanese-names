from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from flashcards.models import Deck, Flashcard, Review
from flashcards.forms import FlashcardForm

import random


def home(request):
    return render(request, "flashcards/home.html")


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "flashcards/signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "flashcards/login.html", {"form": form})


@login_required
def review_dashboard(request):
    # first, check if the user has a deck
    if Deck.objects.filter(user=request.user) is None:
        return render(
            request,
            "flashcards/review_dashboard.html",
            {"flashcard": None, "form": FlashcardForm()},
        )
    else:
        user_deck = Deck.objects.filter(user=request.user).first()

    # next, check if there is anything to review in the deck
    if (
        Review.objects.filter(deck=user_deck, ready_for_review=True)
        .order_by("next_review_date")
        .first()
        is None
    ):
        return render(
            request,
            "flashcards/review_dashboard.html",
            {"flashcard": None, "form": FlashcardForm()},
        )
    else:
        flashcard = (
            Review.objects.filter(deck=user_deck, ready_for_review=True)
            .order_by("next_review_date")
            .first()
        )

    if request.method == "POST":
        hiragana = request.POST["user_response"]
        if hiragana == flashcard.flashcard.hiragana:
            flashcard.update_review_date(is_correct=True)
            return redirect("review")
        else:
            message = "I'm afraid that is incorrect. Please try again."
            flashcard.update_review_date(is_correct=False)
            flashcard.is_ready_for_review()
            return render(
                request,
                "flashcards/review_dashboard.html",
                {"flashcard": flashcard, "form": FlashcardForm(), "message": message},
            )

    return render(
        request,
        "flashcards/review_dashboard.html",
        {"flashcard": flashcard, "form": FlashcardForm()},
    )


@login_required
def learn_dashboard(request):
    if not Deck.objects.filter(user=request.user):
        user_deck = Deck(user=request.user)
        user_deck.save()
    else:
        user_deck = Deck.objects.filter(user=request.user).first()

    try:
        flashcard = Flashcard.objects.exclude(deck=user_deck.id).order_by("id").first()
    except:
        flashcard = Flashcard.objects.get(id=1)

    if request.method == "POST":
        hiragana = request.POST["user_response"]
        if hiragana == flashcard.hiragana:
            # Flashcard answered correctly, add it to the user's deck for review
            review = Review(deck=user_deck, flashcard=flashcard)
            review.save()
            return redirect("learn")
        else:
            message = "I'm afraid that is incorrect. Please try again."
            return render(
                request,
                "flashcards/learn_dashboard.html",
                {"flashcard": flashcard, "form": FlashcardForm(), "message": message},
            )

    return render(
        request,
        "flashcards/learn_dashboard.html",
        {"flashcard": flashcard, "form": FlashcardForm()},
    )
