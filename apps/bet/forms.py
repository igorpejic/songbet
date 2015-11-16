from django import forms


BET_CHOICES = (
    ('1', 'Will rise'),
    ('x', 'Will stay'),
    ('2', 'Will fall'),
)


class NormalBetForm(forms.Form):
    song = forms.CharField()
    data = forms.ChoiceField(BET_CHOICES)
