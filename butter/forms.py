from django import forms
from brekky import globals as globs


class TxForm(forms.Form):
    tx_type = forms.ChoiceField(
        choices=globs.TX_TYPES,
        widget=forms.RadioSelect(),
        error_messages={
            'required': 'You need to choose to BUY or SELL'
        }
    )
    amount = forms.DecimalField(
        max_digits=20,
        error_messages={
            'required': 'A positive amount is required'}
    )
    address = forms.CharField(
        max_length=255,
        min_length=1,
        required=False,
    )
    payment_processor = forms.ChoiceField(
        choices=globs.PAYMENT_PROCESSORS,
        widget=forms.RadioSelect(),
        error_messages={
            'required': 'You must choose a Payment Processor'
        }
    )


class OKPay(forms.Form):
    """
    Field required to get a valid OKPay wallet
    """
    wallet_id = forms.CharField(
        max_length=255,
        min_length=1,
        required=True,
        error_messages={
            'required': 'You must provide a Wallet ID.'
                        'This can be you Wallet ID number, your email address '
                        'or your phone number. '
                        'Brekky does not store this information. '
                        'It is just used to verify that your wallet exists '
                        'before funds are sent.'
        }
    )