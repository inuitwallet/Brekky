from butter.payment_processors.okpay import OkPay
from django.http.response import HttpResponseServerError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import *
from .forms import *

payment_processors = {
    'okpay': OkPay()
}


def index(request):
    """
    Display the single Butter front page and allow visitors to start a Buy a=or Sell
    transaction
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = TxForm(request.POST)
        if form.is_valid():
            if request.POST['tx_type'] == 'BUY':
                # address validation
                if not request.POST['address']:
                    print('no address')
                    messages.add_message(
                        request,
                        messages.ERROR,
                        'You have provided an invalid Address'
                    )
                    context = {
                        'form': form,
                        'currency_plural': 'NuBits',
                        'currency_code': 'NBT'
                    }
                    return render(request, 'butter/index.html', context)
                # TODO - check the amount of currency we have available for trade and
                # TODO - alert if less than requested amount.
                # Save the incomplete BUY transaction for the records
                # TODO - don't hard code currencies
                tx = Transactions.objects.create(
                    payment_processor=request.POST['payment_processor'],
                    tx_type=request.POST['tx_type'],
                    currency='NBT',
                    amount=request.POST['amount'],
                    address=request.POST['address']
                )
                # send the request to the Payment processor
                return redirect(
                    payment_processors['okpay'].generate_payment_url(
                        tx,
                        request.POST,
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
        'currency_code': 'NBT'
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
