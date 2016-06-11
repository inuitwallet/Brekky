from django import forms
from brekky import globals as globs


class TxForm(forms.Form):
    tx_type = forms.ChoiceField(
        choices=globs.TX_TYPES,
        widget=forms.RadioSelect()
    )
    amount = forms.DecimalField(
        max_digits=20
    )
    address = forms.CharField(
        max_length=255,
        min_length=10,
    )
    payment_processor = forms.ChoiceField(
        choices=globs.PAYMENT_PROCESSORS,
        widget=forms.RadioSelect()
    )
