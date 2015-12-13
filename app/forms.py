from django import forms


class GiftCardForm(forms.Form):
    name = forms.CharField(label='From', max_length=100)
    amount = forms.IntegerField(label='Gift Card Amount',
                                max_value=1000, min_value=10)
