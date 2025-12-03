from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST

from .forms import FlashcardForm, CategoryForm, CategoryFindForm, GroupOfFlashcardsForm
from .models import Flashcard, Category
from .services.flashcard_services import (
    get_cards,
    get_random_card,
    get_counter,
    catches_the_answer_on_the_card,
)


def create_flashcard(request):
    if request.method == "GET":
        form = FlashcardForm()
        return render(
            request,
            "flashcards/create_and_update_flashcard.html",
            {"title": "Create card", "form": form},
        )
    form = FlashcardForm(request.POST)
    if form.is_valid():
        form.save()
    return redirect(reverse("categories_list"))


def update_flashcard(request, flashcard_id):
    current_flashcard = get_object_or_404(Flashcard, id=flashcard_id)
    if request.method == "GET":
        form = FlashcardForm(instance=current_flashcard)
        return render(
            request,
            "flashcards/create_and_update_flashcard.html",
            {"title": "Update card", "form": form},
        )
    form = FlashcardForm(request.POST, instance=current_flashcard)
    if form.is_valid():
        form.save()
    return redirect(reverse("categories_list"))


def flashcards_list(request):
    cards = Flashcard.objects.all()
    form = CategoryFindForm()
    if request.method == "POST":
        form = CategoryFindForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data["model_choice"]
            cards = Flashcard.objects.filter(category=category)
    return render(
        request,
        "flashcards/flashcards_list.html",
        {
            "title": "Flashcards",
            "cards": cards,
            "form": form,
        },
    )


@require_POST
def delete_flashcard(request):
    flashcard_id = request.POST.get("card_id")
    card_deleted = Flashcard.objects.get(id=flashcard_id)
    card_deleted.delete()
    return redirect(reverse("flashcards_list"))


def create_category(request):
    if request.method == "GET":
        form = CategoryForm()
        return render(
            request,
            "flashcards/create_and_update_category.html",
            {"title": "Create category", "form": form},
        )
    form = CategoryForm(request.POST)
    if form.is_valid():
        form.save()
    return redirect(reverse("categories_list"))


def update_category(request, category_id):
    current_category = get_object_or_404(Category, id=category_id)
    if request.method == "GET":
        form = CategoryForm(instance=current_category)
        return render(
            request,
            "flashcards/create_and_update_category.html",
            {"title": "Update category", "form": form},
        )
    form = CategoryForm(request.POST, instance=current_category)
    if form.is_valid():
        form.save()
    return redirect(reverse("categories_list"))


def categories_list(request):
    categories = Category.objects.all()

    if "flashcards" in request.session:
        del request.session["flashcards"]

    return render(
        request,
        "flashcards/categories_list.html",
        {
            "title": "Categories",
            "categories": categories,
        },
    )


@require_POST
def delete_category(request):
    category_id = request.POST.get("category_id")
    category_deleted = Category.objects.get(id=category_id)
    category_deleted.delete()
    return redirect(reverse("categories_list"))


def learning_flashcards(request, category_id):
    flashcards, errors = get_cards(request, category_id)
    if errors:
        return errors
    last_card_id = request.session.get("last_card_id")

    current_learn_cards, count_cards_in_category = get_counter(category_id, flashcards)

    if request.method == "POST":
        flashcards, redirect_response = catches_the_answer_on_the_card(
            request, flashcards, last_card_id
        )
        if redirect_response:
            return redirect_response
        current_learn_cards, count_cards_in_category = get_counter(
            category_id, flashcards
        )

    card = get_random_card(last_card_id, flashcards)
    request.session["last_card_id"] = card[0]

    if request.GET.get("reverse"):
        card1, card2 = card[2], card[1]
    else:
        card1, card2 = card[1], card[2]

    is_last_card_in_session = len(flashcards) == 1

    return render(
        request,
        "flashcards/learning_flashcards.html",
        {
            "title": "Learning cards",
            "card1": card1,
            "card2": card2,
            "is_last_card_in_session": is_last_card_in_session,
            "current_learn_cards": current_learn_cards,
            "count_cards_in_category": count_cards_in_category,
        },
    )


def create_group_of_flashcards(request):
    if request.method == "POST":
        form = GroupOfFlashcardsForm(request.POST)
        if form.is_valid():
            form.save_cards()
            return redirect(reverse("categories_list"))
    form = GroupOfFlashcardsForm()
    return render(request, "flashcards/group_of_flashcards.html", {"form": form})


def get_cards_in_category(request, category_id):
    title = "Get all cards in category"
    category = Category.objects.get(id=category_id)
    cards = Flashcard.objects.filter(category=category)
    return render(
        request,
        "flashcards/get_cards_in_category.html",
        {"title": title, "category": category, "cards": cards},
    )
