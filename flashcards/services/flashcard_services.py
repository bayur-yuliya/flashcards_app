import random

from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse

from ..models import Flashcard, Category


def get_cards(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if "flashcards" not in request.session:
        flashcards = list(
            Flashcard.objects.filter(category=category).values_list(
                "id", "first_side", "second_side"
            )
        )
        if not flashcards:
            return redirect(reverse("create_flashcard"))
        request.session["flashcards"] = flashcards
    else:
        flashcards = request.session["flashcards"]
    if not flashcards:
        return redirect(reverse("categories_list"))
    return flashcards


def get_random_card(last_card_id, flashcards):
    if len(flashcards) == 0:
        return None
    card = random.choice(flashcards)
    if len(flashcards) > 1 and card[0] == last_card_id:
        while card[0] == last_card_id:
            card = random.choice(flashcards)
    return card


def get_counter(category, flashcards):
    count_cards_in_category = Flashcard.objects.filter(category=category).count()
    current_learn_cards = len(flashcards)
    current_learn_cards = count_cards_in_category - current_learn_cards + 1
    return current_learn_cards, count_cards_in_category


def catches_the_answer_on_the_card(request, flashcards, last_card_id):
    if "learn" in request.POST and last_card_id:
        flashcards = [card for card in flashcards if card[0] != last_card_id]
        request.session["flashcards"] = flashcards
        if not flashcards:
            request.session.clear()
            return redirect(reverse("categories_list"))
    elif "wrong" in request.POST:
        pass
    elif "complete" in request.POST:
        request.session.clear()
        return redirect(reverse("categories_list"))
