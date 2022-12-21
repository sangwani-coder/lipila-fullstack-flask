from skoolpay.momo.momo import Momo


class Airtel(Momo):
    def make_payment(self, account, amount):
        return 'success'