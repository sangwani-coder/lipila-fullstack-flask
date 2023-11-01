from momo.momo import Momo


class Airtel(Momo):
    def make_payment(self, account, amount):
        return True