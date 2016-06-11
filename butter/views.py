from butter.payment_processors.okpay import OkPay
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import *
from .forms import *

payment_processors = {
    'okpay': OkPay()
}


def index(request):
    if request.method == 'POST':
        form = TxForm(request.POST)
        if form.is_valid():
            # Save the incomplete transaction for the records
            # TODO - don't hard code currencies
            tx = Transactions.objects.create(
                payment_processor=request.POST['payment_processor'],
                tx_type=request.POST['tx_type'],
                currency='NBT',
                amount=request.POST['amount'],
                address=request.POST['address']
            )
            # send the request to the Payment processor
            url = payment_processors['okpay'].generate_payment_url(
                tx,
                request.POST,
                'NBT'
            )
            return HttpResponseRedirect(url)
    else:
        form = TxForm()

    # get the available funds
    context = {
        'form' : form,
        'buy_amount': 20,
        'sell_amount': 50,
        'currency_code': 'NBT',
        'currency': 'NuBit',
        'currency_plural': 'NuBits'
    }
    return render(request, 'butter/index.html', context)
