import random

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .forms import FlashcardForm, CategoryForm, CategoryFindForm
from .models import Flashcard, Category


def create_flashcard(request):
    if request.method == 'GET':
        form = FlashcardForm()
        return render(request, 'flashcards/create_flashcard.html', {'title': 'Create', 'form': form})
    form = FlashcardForm(request.POST)
    if form.is_valid():
        form.save()
    return redirect(reverse('categories_list'))


def update_flashcard(request, flashcard_id):
    current_flashcard = get_object_or_404(Flashcard, id=flashcard_id)
    if request.method == 'GET':
        form = FlashcardForm(instance=current_flashcard)
        return render(request, 'flashcards/update_flashcard.html', {'title': 'Update', 'form': form})
    form = FlashcardForm(request.POST, instance=current_flashcard)
    if form.is_valid():
        form.save()
    return redirect(reverse('categories_list'))


def flashcards_list(request):
    cards = Flashcard.objects.all()
    form = CategoryFindForm()
    if request.method == 'POST':
        form = CategoryFindForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data['model_choice']
            cards = Flashcard.objects.filter(category=category)
    return render(request, 'flashcards/flashcards_list.html', {
        'title': 'Flashcards',
        'cards': cards,
        'form': form,
    })


def delete_flashcard(request, flashcard_id):
    card_deleted = Flashcard.objects.get(id=flashcard_id)
    card_deleted.delete()
    return redirect(reverse('flashcards_list'))


def create_category(request):
    if request.method == 'GET':
        form = CategoryForm()
        return render(request, 'flashcards/create_category.html', {'title': 'Create', 'form': form})
    form = CategoryForm(request.POST)
    if form.is_valid():
        form.save()
    return redirect(reverse('categories_list'))


def update_category(request, category_id):
    current_category = get_object_or_404(Category, id=category_id)
    if request.method == 'GET':
        form = CategoryForm(instance=current_category)
        return render(request, 'flashcards/update_category.html', {'title': 'Update', 'form': form})
    form = CategoryForm(request.POST, instance=current_category)
    if form.is_valid():
        form.save()
    return redirect(reverse('categories_list'))


def categories_list(request):
    categories = Category.objects.all()

    if 'flashcards' in request.session:
        del request.session['flashcards']

    return render(request, 'flashcards/categories_list.html', {
        'title': 'Categories',
        'categories': categories,
    })


def delete_category(request, category_id):
    category_deleted = Category.objects.get(id=category_id)
    category_deleted.delete()
    categories = Category.objects.all()
    return render(request, 'flashcards/categories_list.html', {
        'title': 'Categories',
        'categories': categories,
    })


def learning_flashcards(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if 'flashcards' not in request.session:
        flashcards = list(Flashcard.objects.filter(category=category).values_list('id', 'first_side', 'second_side'))
        if not flashcards:
            return redirect(reverse('create_flashcard'))
        request.session['flashcards'] = flashcards
    else:
        flashcards = request.session['flashcards']

    last_card_id = request.session.get('last_card_id')

    if request.method == 'POST' and 'learn' in request.POST and last_card_id:
        flashcards = [card for card in flashcards if card[0] != last_card_id]
        request.session['flashcards'] = flashcards
        if not flashcards:
            return redirect(reverse('categories_list'))
    elif 'wrong' in request.POST:
        pass
    elif 'complete' in request.POST:
        request.session.clear()
        return redirect(reverse('categories_list'))

    card = random.choice(flashcards)
    while card[0] == last_card_id:
        card = random.choice(flashcards)
    request.session['last_card_id'] = card[0]

    last = len(flashcards) == 1

    if request.GET.get('reverse'):
        card1, card2 = card[2], card[1]
    else:
        card1, card2 = card[1], card[2]

    return render(request, 'flashcards/learning_flashcards.html', {
        'title': 'Learning',
        'card1': card1,
        'card2': card2,
        'category_id': category_id,
        'last': last,
    })
