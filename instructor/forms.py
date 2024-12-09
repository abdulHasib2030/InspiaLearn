from category.models import Category
from django import forms
from instructor.models import EXPERIENCE

class QuestionForm1(forms.Form):
    question1 = forms.ModelChoiceField(queryset=Category.objects.all(), label="Category")

class QuestionForm2(forms.Form):
    question2 = forms.ChoiceField(choices=EXPERIENCE, label="Experience Level")

class QuestionForm3(forms.Form):
    question3 = forms.BooleanField(required=True, label="I agree to the Terms and Conditions")
