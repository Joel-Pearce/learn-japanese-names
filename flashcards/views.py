from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login

from flashcards.models import Deck, Flashcard, Review
from flashcards.forms import FlashcardForm


def home(request):
    return render(request, 'flashcards/home.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'flashcards/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'flashcards/login.html', {'form': form})


def review_dashboard(request):
    user_deck = Deck.objects.filter(user=request.user).first()
    flashcard = Review.objects.filter(deck=user_deck).order_by('id').first()
    return render(request, 'flashcards/review_dashboard.html', {'flashcard': flashcard, 'form': FlashcardForm()})


def learn_dashboard(request):
    user_deck = Deck.objects.filter(user=request.user).first()
    try:
        flashcard = Flashcard.objects.exclude(deck=user_deck.id).order_by('id').first()
    except:
        flashcard = Flashcard.objects.get(id=1)
    return render(request, 'flashcards/learn_dashboard.html', {'flashcard': flashcard, 'form': FlashcardForm()})