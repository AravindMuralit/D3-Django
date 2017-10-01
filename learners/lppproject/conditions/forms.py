from django import forms
from .models import condPost, rulePost


class condFilRq (forms.ModelForm):

    class Meta:
        model = condPost
        fields = ('name','field')