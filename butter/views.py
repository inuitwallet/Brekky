from decimal import Decimal

import requests
from brekky.bip32utils import BIP32Key
from butter.payment_processors.okpay import OkPay
from butter.utils import AddressCheck
from django.conf import settings
from django.http.response import HttpResponseServerError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from toast.models import Account
from .models import *
from .forms import *

payment_processors = {
    'okpay': OkPay()
}

BIP32_HARDEN = 0x80000000  # choose from hardened set of child keys

account = Account.objects.get(user=settings.BUTTER_USER_ID)
pubkey = BIP32Key.fromExtendedKey(account.extpub)


def get_nbt_balance():
    """
    get the balance from daio for the current butter address
    :param address:
    :return:
    """
    address = pubkey.ChildKey(int(account.level)).Address()
    r = requests.post(
        url='{}/balance'.format(settings.DAIO_URL),
        headers={'Authentication': settings.DAIO_TOKEN},
        data={'address': address}
    )
    try:
        response = r.json()
    except ValueError:
        return -1
    if response['success']:
        return Decimal(response['balance'])
    else:
        return -1


def index(request):
    """
    Display the single Butter front page and allow visitors to start a Buy or Sell
    transaction
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = TxForm(request.POST)
        if form.is_valid():
            if request.POST['tx_type'] == 'BUY':
                # address validation
                # is there an address?
                if not request.POST['address']:
                    messages.add_message(
                        request,
                        messages.ERROR,
                        'You have not provided an Address'
                    )
                    context = {
                        'form': form,
                        'currency_plural': 'NuBits',
                        'currency_code': 'NBT'
                    }
                    return render(request, 'butter/index.html', context)
                # check for valid checksum
                address_check = AddressCheck()
                if not address_check.check_checksum(request.POST['address']):
                    messages.add_message(
                        request,
                        messages.ERROR,
                        'You have provided an invalid Address'
                    )
                    context = {
                        'form': form,
                        'currency_plural': 'NuBits',
                        'currency_code': 'NBT',
                        'balance': get_nbt_balance(),
                    }
                    return render(request, 'butter/index.html', context)
                # get the current NBT balance
                balance = get_nbt_balance()
                amount = request.POST['amount']
                if balance <= 0:
                    messages.add_message(
                        request,
                        messages.ERROR,
                        'There are no funds available in Butter.'
                    )
                    context = {
                        'form': form,
                        'currency_plural': 'NuBits',
                        'currency_code': 'NBT',
                        'balance': balance,
                    }
                    return render(request, 'butter/index.html', context)
                if balance < Decimal(amount):
                    messages.add_message(
                        request,
                        messages.WARNING,
                        'There are insufficient funds available for your request.\n'
                        'Will transact the maximum available amount of {}'.format(balance)
                    )
                    amount = balance
                # Save the incomplete BUY transaction for the records
                # TODO - don't hard code currencies
                tx = Transactions.objects.create(
                    payment_processor=request.POST['payment_processor'],
                    tx_type=request.POST['tx_type'],
                    currency='NBT',
                    amount=amount,
                    address=request.POST['address']
                )
                # send the request to the Payment processor
                return redirect(
                    payment_processors['okpay'].generate_payment_url(
                        tx,
                        amount,
                        'NBT'
                    )
                )
            else:
                # Save the incomplete SELL transaction for the records
                tx = Transactions.objects.create(
                    payment_processor=request.POST['payment_processor'],
                    tx_type=request.POST['tx_type'],
                    currency='NBT',
                    amount=request.POST['amount']
                )
                # send the user to the next page to give their payment processor details
                return redirect(
                    'selling_page_2',
                    tx_id=tx.id
                )
    else:
        form = TxForm()

    # get the available funds
    context = {
        'form': form,
        'currency_plural': 'NuBits',
        'currency_code': 'NBT',
        'balance': get_nbt_balance(),
    }
    return render(request, 'butter/index.html', context)


def selling_page_2(request, tx_id):
    """
    If a selling transaction has been started, this view will display an address and
    request the details necessary from the user for the chosen payment processor
    :param request:
    :param tx_id:
    :return:
    """
    # get the transaction from the passed id
    tx = get_object_or_404(Transactions, id=tx_id)
    # get the payment_processor name from the tx
    payment_processor = None
    for pp in globs.PAYMENT_PROCESSORS:
        if pp[0] == tx.payment_processor:
            payment_processor = pp[1]

    if payment_processor is None:
        return HttpResponseServerError()

    if request.method == 'POST':
        form = globals()[payment_processor](request.POST)
        if form.is_valid():
            if payment_processor == 'OKPay':
                # check their wallet exists
                # get our balance
                # alert if amount we can buy is less than the amount they want to sell
                # display address for coins to be sent to
                # wait for received tx
                # initiate payment through OKPay
                pass
            pass

    else:
        form = globals()[payment_processor]()

    context = {
        'form': form,
        'payment_processor': payment_processor
    }
    return render(request, 'butter/selling-page-2.html', context)
