from skoolpay.momo.momo import Momo


API_KEY = ''
AUTH_KEY = ''

class MTN(Momo):
    def make_payment(self, account, amount):
        return 'success'