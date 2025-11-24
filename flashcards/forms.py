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
        fields = ('category', 'first_side', 'second_side',)


class CategoryForm(forms.ModelForm):
    name = forms.CharField(
        max_length=250,
        widget=forms.TextInput(attrs={'class': 'category-input'})
    )

    class Meta:
        model = Category
        fields = ('name',)


class CategoryFindForm(forms.Form):
    model_choice = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        initial=0
    )
