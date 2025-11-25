from django import forms

from .models import Flashcard, Category


class FlashcardForm(forms.ModelForm):
    first_side = forms.CharField(widget=forms.Textarea(attrs={"maxlength": 250}))
    second_side = forms.CharField(widget=forms.Textarea(attrs={"maxlength": 250}))
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        initial=0
        )

    class Meta:
        model = Flashcard
        fields = ('category', 'first_side', 'second_side',)


class CategoryForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
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
