import unittest
# from src import jwm, macaroon

from JWM.macaroon import Macaroon
from JWM.jwm import JWM
from JWM.verifier import Verifier


class TestJWM(unittest.TestCase):
    def test_serialize(self):
        m = Macaroon(location='example.com',
                     identifier='use super_secret_key', key='super_secret_key')
        jwm = JWM(m)
        self.assertEqual(jwm.serialize(), 'eyJ0eXAiOiAiandtIn0.W3siaWRlbnRpZmllciI6ICJ1c2Ugc3VwZXJfc2VjcmV0X2tleSIsICJzaWduYXR1cmUiOiAiMmNiMDE5MjM3YjgyYzc2NTU3MjRjYWY2YjdiYWIzNmMyZmNmMzQyMTcxYzFhMDVkOWQ0OTg5N2MwMGQ4OTNmMSIsICJsb2NhdGlvbiI6ICJleGFtcGxlLmNvbSJ9XQ')

    def test_deserialize(self):
        am = Macaroon(location='example.com',
                      identifier='use super_secret_key', key='super_secret_key')
        am.add_first_party_caveat('key', 'value')
        jwm = JWM(am)
        self.assertEqual(jwm.authorizing_macaroon.signature, JWM.deserialize(
            jwm.serialize()).authorizing_macaroon.signature)
