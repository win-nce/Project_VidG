from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Report, Review, Reaction

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class ReportForm(forms.ModelForm):
    description = forms.CharField(
        max_length=1024,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Опишите проблему"
            }
        )
    )

    class Meta:
        model = Report
        fields = ['theme', 'description']

        widgets = {
            'theme': forms.Select(
                attrs={
                    "class": "form-select"
                }
            )
        }



class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class ReportForm(forms.ModelForm):
    description = forms.CharField(
        max_length=1024,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Опишите проблему"
            }
        ),
        required=False
    )

    class Meta:
        model = Report
        fields = ['theme', 'description']
        widgets = {
            'theme': forms.Select(attrs={"class": "form-select"})
        }


class ReviewForm(forms.ModelForm):
    content = forms.CharField(
        label="Ваш отзыв",
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 5,
            "placeholder": "Напишите ваш отзыв здесь"
        })
    )

    class Meta:
        model = Review
        fields = ['content']


class ReactionForm(forms.ModelForm):
    reaction_type = forms.ChoiceField(
        choices=(
            ('like', 'Нравится'),
            ('dislike', 'Ненравится')
        ),
        widget=forms.RadioSelect,
        label="Ваша реакция"
    )

    class Meta:
        model = Reaction
        fields = ['reaction_type']
