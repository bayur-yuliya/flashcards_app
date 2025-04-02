from django.urls import path

from . import views

urlpatterns = [
    path('flashcard/create/', views.create_flashcard, name='create_flashcard'),
    path('flashcard/<int:flashcard_id>/update/', views.update_flashcard, name='update_flashcard'),
    path('category/create/', views.create_category, name='create_category'),
    path('category/<int:category_id>/update/', views.update_category, name='update_category'),
    path('category/<int:category_id>/flashcard/', views.learning_flashcards, name='learning_flashcards'),
    path('flashcard/', views.flashcards_list, name='flashcards_list'),
    path('delete_category/<int:category_id>', views.delete_category, name='delete_category'),
    path('delete_flashcard/<int:flashcard_id>', views.delete_flashcard, name='delete_flashcard'),
    path('', views.categories_list, name='categories_list'),
]
