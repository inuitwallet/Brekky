
class Payza(object):
    def __init__(self):
        pass

    @staticmethod
    def generate_payment_url(self, tx, post_data, currency):
        """
        generate a payment url to allow a user to send funds by this processor
        :param tx: a butter Transactions object
        :param post_data: the request POST data dict that created this tx
        :return:
        """
        # TODO - don't hard code OK_Receiver
        # TODO - don't hard code price or currencies
        return 'https://checkout.okpay.com/?' \
               'ok_receiver=OK882706663&' \
               'ok_item_1_name={}&' \
               'ok_currency=USD&' \
               'ok_item_1_type=digital&' \
               'ok_item_1_price=1&' \
               'ok_item_1_quantity={}&' \
               'ok_fees=1&' \
               'ok_invoice={}'.format(
                    '{}%20{}'.format(post_data['amount'], currency),
                    post_data['amount'],
                    tx.id
               )