from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .forms import FlashcardForm, CategoryForm
from .models import Flashcard, Category


def index(request):
    return render(request, 'flashcards/index.html', {'title': 'Index'})


def create_flashcard(request):
    if request.method == 'GET':
        form = FlashcardForm()
        return render(request, 'flashcards/create_flashcard.html', {'title': 'Create', 'form': form})
    form = FlashcardForm(request.POST)
    if form.is_valid():
        form.save()
    return redirect(reverse('flashcards_list'))


def update_flashcard(request, flashcard_id):
    current_flashcard = get_object_or_404(Flashcard, id=flashcard_id)
    if request.method == 'GET':
        form = FlashcardForm(instance=current_flashcard)
        return render(request, 'flashcards/update_flashcard.html', {'title': 'Update', 'form': form})
    form = FlashcardForm(request.POST, instance=current_flashcard)
    if form.is_valid():
        form.save()
    return redirect(reverse('flashcards_list'))


def flashcards_list(request):
    cards = Flashcard.objects.all()
    return render(request, 'flashcards/flashcards_list.html', {
        'title': 'Flashcards',
        'cards': cards,
    })


def delete_flashcard(request, flashcard_id):
    card_deleted = Flashcard.objects.get(id=flashcard_id)
    card_deleted.delete()
    cards = Flashcard.objects.all()
    return render(request, 'flashcards/flashcards_list.html', {
        'title': 'Flashcards',
        'cards': cards,
    })


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
    card = Flashcard.objects.filter(category=Category.objects.get(id=category_id), is_answered=False)
    len_ = len(card)
    last = True if len_ == 1 else False
    first_side = True

    if request.GET.get('next_side1'):
        first_side = False

    if request.GET.get('next_side2'):
        first_side = True

    if request.GET.get('learn'):
        Flashcard.objects.filter(id=card[0].id).update(is_answered=True)

    if request.GET.get('complete'):
        Flashcard.objects.all().update(is_answered=False)
        return redirect(reverse('categories_list'))

    return render(request, 'flashcards/learning_flashcards.html', {
        'title': 'Learning',
        'card1': card[0].first_side,
        'card2': card[0].second_side,
        'category_id': category_id,
        'last': last,
        'first_side': first_side
    })


def finish(request):
    return render(request, 'flashcards/finish.html', {'title': 'Finish'})
