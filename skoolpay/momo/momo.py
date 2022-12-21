""" Defines the momo base class"""

class Momo:
    """
        mobile money base class
        get_network: method that verifies a mobile number
            and searchs for the network provider
    """
    codes = {
        'mtn':['096', '076'],
        'airtel':['097', '077']
    }

    def verify(self, num: str) -> str:

        if num is not None:
            if len(num) != 10:
                return 'Unknown'
            num_code = num[:3]

            if num_code in self.codes['mtn']:
                return 'mtn'
            elif num_code in self.codes['airtel']:
                return 'airtel'
            else:
                return 'Unknown'
        return 'Unknown'

    def get_network(self, mobile: str) -> str:
        v_num = self.verify(mobile)
        return v_num