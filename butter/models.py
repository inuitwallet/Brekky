from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from brekky import globals as globs


class Transactions(models.Model):
    """
    A butter transaction simply records some cash flow activity within Butter.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='butter_txs',
        related_query_name='butter_tx',
        null=True,
        blank=True
    )

    payment_processor = models.CharField(
        max_length=255,
        choices=globs.PAYMENT_PROCESSORS,
        help_text='The payment processing service that was used to make this transaction.'
    )

    payment_processor_id = models.CharField(
        max_length=255,
        help_text='The transaction id provided by the payment processor',
        blank=True
    )

    tx_type = models.CharField(
        max_length=255,
        choices=globs.TX_TYPES,
        help_text='The type of transaction this is. '
                  'It is always in reference to the Nu currency.'
    )

    currency = models.CharField(
        max_length=255,
        choices=globs.CURRENCIES,
        help_text='The Nu currency this transaction relates to.'
    )

    amount = models.DecimalField(
        max_digits=20,
        decimal_places=6,
        help_text='The amount of Nu currency transacted.'
    )

    address = models.CharField(
        max_length=255,
        help_text='The Nu address associated with this transaction. '
                  'This will either be used to receive funds from a customer '
                  'or be provided by a customer to receive their Nu tokens. ',
        blank=True
    )

    complete = models.BooleanField(
        default=False
    )

    def __str__(self):
        return '{} {}: {}'.format(
            self.amount,
            self.currency,
            'complete' if self.complete else 'incomplete')