from django.http import HttpResponse


def index(request):
    return HttpResponse('Greetings')


def create_flashcard(request):
    return HttpResponse('Creating Flashcards')


def update_flashcard(request):
    return HttpResponse('Changing a FlashCard')


def create_category(request):
    return HttpResponse('Creating category')


def update_category(request):
    return HttpResponse('Changing a category')


def categories_list(request):
    return HttpResponse('Categories list')


def flashcards_list(request):
    return HttpResponse('Flashcards list')


def learning_flashcards(request):
    return HttpResponse('Learning flashcards')

