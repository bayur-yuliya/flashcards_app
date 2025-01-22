from django import forms

from .models import Flashcard, Category


class FlashcardForm(forms.ModelForm):
    first_side = forms.Textarea()
    second_side = forms.Textarea()
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        initial=0
        )

    class Meta:
        model = Flashcard
        fields = ('first_side', 'second_side', 'category',)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)
