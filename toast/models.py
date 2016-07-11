from __future__ import unicode_literals

import requests
from django.conf import settings
from django.contrib.auth.models import User

from django.db import models


class Account(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    wallet_id = models.IntegerField()
    mnemonic = models.CharField(
        max_length=255,
    )
    extpub = models.CharField(
        max_length=255,
    )
    level = models.IntegerField(
        default=0
    )

    def __init__(self, *args, **kwargs):
        super(Account, self).__init__(*args, **kwargs)

        self.get_daio_account()

    def get_daio_account(self):
        r = requests.get(
            url='{}/new'.format(settings.DAIO_URL),
            headers={
                'Authentication': settings.DAIO_TOKEN
            }
        )
        try:
            response = r.json()
            self.wallet_id = response['id']
            self.mnemonic = response['mnemonic']
            self.extpub = response['extpub']
        except ValueError:
            pass
