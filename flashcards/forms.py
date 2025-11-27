from django import forms

from .models import Flashcard, Category


class FlashcardForm(forms.ModelForm):
    first_side = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "maxlength": 250,
                "class": "card_textarea",
                "placeholder": "Первая сторона карточки",
            }
        )
    )
    second_side = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "maxlength": 250,
                "class": "card_textarea",
                "placeholder": "Вторая сторона карточки",
            }
        )
    )
    category = forms.ModelChoiceField(queryset=Category.objects.all(), initial=0)

    class Meta:
        model = Flashcard
        fields = (
            "category",
            "first_side",
            "second_side",
        )

    def clean_first_side(self):
        first_side = self.cleaned_data["first_side"]
        lines = first_side.split(" \n")
        return lines

    def clean_second_side(self):
        second_side = self.cleaned_data["second_side"]
        lines = second_side.split(" \n")
        return lines

    def save(self, commit=True):
        instance = super().save(commit=False)

        instance.first_side = self.clean_first_side()
        instance.second_side = self.clean_second_side()

        if commit:
            instance.save()
        return instance


class CategoryForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={"class": "category-input"})
    )

    class Meta:
        model = Category
        fields = ("name",)


class CategoryFindForm(forms.Form):
    model_choice = forms.ModelChoiceField(queryset=Category.objects.all(), initial=0)
