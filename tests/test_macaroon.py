import unittest
from JWM import Macaroon


class TestMacaroon(unittest.TestCase):
    def test_caveats(self):
        am = Macaroon(location='example.com',
                      identifier='use super_secret_key', key='super_secret_key')
        am.add_first_party_caveat('key', 'value')
        am.add_first_party_caveat('key2', 'value2')
        caveat_key = '4; guaranteed random by a fair toss of the dice'
        identifier = 'this was how we remind auth of key/pred'
        am.add_third_party_caveat('http://auth.mybank/', caveat_key, identifier)
        for caveat in am.caveats:
            print(caveat.to_dict())
