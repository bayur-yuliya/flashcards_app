from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .forms import FlashcardForm, CategoryForm
from .models import Flashcard, Category


def index(request):
    return render(request, 'flashcards/index.html')


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
    form = CategoryForm(request.POST, instance=current_flashcard)
    if form.is_valid():
        form.save()
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
    return render(request, 'flashcards/categories_list.html', {
        'title': 'Categories',
        'categories': categories,
    })


def flashcards_list(request):
    cards = Flashcard.objects.all()
    return render(request, 'flashcards/flashcards_list.html', {
        'title': 'Flashcards',
        'cards': cards,
    })


def learning_flashcards(request):
    return render(request, 'flashcards/learning_flashcards.html', {'title': 'Learning',})

