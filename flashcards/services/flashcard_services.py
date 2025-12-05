import logging
import random

from django.db import DatabaseError
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse

from ..models import Flashcard, Category

logger = logging.getLogger(__name__)


def get_cards(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if "flashcards" not in request.session:
        try:
            flashcards = list(
                Flashcard.objects.filter(category=category).values_list(
                    "id", "first_side", "second_side"
                )
            )
            if not flashcards:
                return None, redirect(reverse("create_flashcard"))
            if not isinstance(flashcards, list):
                logger.warning("Corrupted data in the session, we clear it")
                request.session.pop("flashcards", None)
                request.session.pop("category_id", None)
                return get_cards(request, category_id)
            request.session["flashcards"] = flashcards
        except DatabaseError as e:
            logger.error(f"Database error when receiving cards: {e}")
            return None, redirect(reverse("categories_list"))
    else:
        flashcards = request.session["flashcards"]
    if not flashcards:
        return None, redirect(reverse("categories_list"))
    return flashcards, None


def get_available_cards(flashcards, last_card_id):
    if not flashcards:
        return []
    return [card for card in flashcards if card[0] != last_card_id]


def get_random_card(last_card_id, flashcards):
    if len(flashcards) == 0:
        return None
    if len(flashcards) == 1:
        return flashcards[0]
    try:
        available_cards = get_available_cards(flashcards, last_card_id)
        if available_cards:
            return random.choice(available_cards)
        else:
            return random.choice(flashcards)
    except IndexError as e:
        logger.error(f"Card selection error: {e}")
        return None


def get_counter(category, flashcards):
    count_cards_in_category = Flashcard.objects.filter(category=category).count()
    current_learn_cards = len(flashcards)
    if current_learn_cards > count_cards_in_category:
        current_learn_cards = count_cards_in_category
    current_learn_cards = count_cards_in_category - current_learn_cards + 1
    return current_learn_cards, count_cards_in_category


def catches_the_answer_on_the_card(request, flashcards, last_card_id):
    if request.method != "POST":
        raise ValueError("The function expects a POST request.")

    if "learn" in request.POST and last_card_id:
        flashcards = get_available_cards(flashcards, last_card_id)
        request.session["flashcards"] = flashcards
        if not flashcards:
            request.session.pop("flashcards", None)
            return None, redirect(reverse("categories_list"))
        return flashcards, None
    elif "wrong" in request.POST:
        return flashcards, None
    elif "complete" in request.POST:
        request.session.pop("flashcards", None)
        return None, redirect(reverse("categories_list"))
    else:
        # Unknown action
        logger.warning(f"Unknown action in POST: {dict(request.POST)}")
        return flashcards, None
