from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('flashcard/<int:flashcard_id>/create/', views.create_flashcard, name='create_flashcard'),
    path('flashcard/<int:flashcard_id>/update/', views.update_flashcard, name='update_flashcard'),
    path('category/<int:category_id>/create/', views.create_category, name='create_category'),
    path('category/<int:category_id>/update/', views.update_category, name='update_category'),
    path('category/<int:category_id>/flashcard/<int:flashcard_id>/', views.learning_flashcards, name='learning_flashcards'),
    path('category/', views.categories_list, name='categories_list'),
    path('flashcard/', views.flashcards_list, name='flashcards_list'),
]