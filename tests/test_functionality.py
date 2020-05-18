import unittest
# from src import jwm, macaroon

from JWM.macaroon import Macaroon
from JWM.jwm import JWM


class TestJWM(unittest.TestCase):
    def test_serialize(self):
        m = Macaroon(location='example.com',
                     identifier='use super_secret_key', key='super_secret_key')
        jwm = JWM(m)
        self.assertEqual(jwm.serialize(), 'eyJ0eXAiOiAiandtIn0=.eyJpZGVudGlmaWVyIjogInVzZSBzdXBlcl9zZWNyZXRfa2V5IiwgInNpZ25hdHVyZSI6ICIyY2IwMTkyMzdiODJjNzY1NTcyNGNhZjZiN2JhYjM2YzJmY2YzNDIxNzFjMWEwNWQ5ZDQ5ODk3YzAwZDg5M2YxIiwgImxvY2F0aW9uIjogImV4YW1wbGUuY29tIn0=')

    def test_deserialize(self):
        am = Macaroon(location='example.com',
                      identifier='use super_secret_key', key='super_secret_key')
        am.add_first_party_caveat('key', 'value')
        jwm = JWM(am)
        self.assertEqual(jwm.authorizing_macaroon.signature, JWM.deserialize(
            jwm.serialize()).authorizing_macaroon.signature)

    def test_verify(self):
        am = Macaroon(location='example.com',
                      identifier='use super_secret_key', key='super_secret_key')
        am.add_first_party_caveat('key', 'value')
        jwm = JWM(am)
        JWM.verify(jwm, 'super_secret_key')

    # example taken from pymacaroons
    def test_verify_with_discharge(self):
        m = Macaroon(
            location='http://mybank/',
            identifier='we used our other secret key',
            key='this is a different super-secret key; \
never use the same secret twice'
        )
        m.add_first_party_caveat('account', '3735928559')
        caveat_key = '4; guaranteed random by a fair toss of the dice'
        identifier = 'this was how we remind auth of key/pred'
        m.add_third_party_caveat('http://auth.mybank/', caveat_key, identifier)

        discharge = Macaroon(
            location='http://auth.mybank/',
            key=caveat_key,
            identifier=identifier
        )
        discharge.add_first_party_caveat('time', '< 2015-01-01T00:00')
        protected = m.prepare_for_request(discharge)

        jwm = JWM(authorizing_macaroon=m, discharge_macaroons=[protected])
        jwm.verify(
            'this is a different super-secret key; \
never use the same secret twice'
        )
