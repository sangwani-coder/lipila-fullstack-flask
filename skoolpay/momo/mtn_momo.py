from skoolpay.momo.momo import Momo


class MTN(Momo):
    def make_payment(self, account, amount):
        return 'success'