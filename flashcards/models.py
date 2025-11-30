from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=250, unique=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.name


class Flashcard(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="flashcards"
    )
    first_side = models.TextField(blank=False)
    second_side = models.TextField(blank=False)

    def __str__(self):
        return f"{self.first_side} - {self.second_side}"
