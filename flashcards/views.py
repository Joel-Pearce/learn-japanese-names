from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from flashcards.models import Deck, Flashcard, Review
from flashcards.forms import (
    FlashcardForm,
    CustomAuthenticationForm,
    CustomUserCreationForm,
)
from flashcards.utils import (
    check_input,
    update_flashcards_in_deck,
    get_number_of_user_learn_cards,
    get_number_of_user_review_cards,
)

import random


def home(request):
    return render(request, "flashcards/home.html")


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = CustomUserCreationForm()
    return render(request, "flashcards/signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("dashboard")
    else:
        form = CustomAuthenticationForm()
    return render(request, "flashcards/login.html", {"form": form})


@login_required(login_url="/login")
def review_dashboard(request):
    form = FlashcardForm(request.POST or None)
    # first, check if the user has a deck
    if Deck.objects.filter(user=request.user) is None:
        return render(
            request,
            "flashcards/review_dashboard.html",
            {"flashcard": None, "form": FlashcardForm()},
        )
    else:
        user_deck = Deck.objects.filter(user=request.user).first()
        update_flashcards_in_deck(user_deck)

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
            {"flashcard": None, "form": form},
        )
    else:
        flashcard = (
            Review.objects.filter(deck=user_deck, ready_for_review=True)
            .order_by("next_review_date")
            .first()
        )

    if request.method == "POST":
        hiragana = request.POST["user_response"]
        if check_input(hiragana, flashcard.flashcard.hiragana):
            flashcard.update_review_date(is_correct=True)
            return redirect("review")
        else:
            message = "I'm afraid that is incorrect. Please try again."
            return render(
                request,
                "flashcards/review_dashboard.html",
                {"flashcard": flashcard, "form": form, "message": message},
            )

    return render(
        request,
        "flashcards/review_dashboard.html",
        {"flashcard": flashcard, "form": form},
    )


@login_required(login_url="/login")
def learn_dashboard(request):
    form = FlashcardForm(request.POST or None)
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
        if check_input(hiragana, flashcard.hiragana):
            # Flashcard answered correctly, add it to the user's deck for review
            review = Review(deck=user_deck, flashcard=flashcard)
            review.save()
            return redirect("learn")
        else:
            message = "I'm afraid that is incorrect. Please try again."
            return render(
                request,
                "flashcards/learn_dashboard.html",
                {"flashcard": flashcard, "form": form, "message": message},
            )

    return render(
        request,
        "flashcards/learn_dashboard.html",
        {"flashcard": flashcard, "form": form},
    )


@login_required(login_url="/signup")
def general_dashboard(request):
    if user_deck := Deck.objects.filter(user=request.user).first():
        update_flashcards_in_deck(user_deck)

    num_to_review = get_number_of_user_review_cards(request.user)
    num_to_learn = get_number_of_user_learn_cards(request.user)

    return render(
        request,
        "flashcards/general_dashboard.html",
        {
            "num_to_review": num_to_review,
            "num_to_learn": num_to_learn,
        },
    )
