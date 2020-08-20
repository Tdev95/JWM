import unittest
from JWM.macaroon import Macaroon
from JWM.verifier import Verifier
from JWM.jwm import JWM


class TestVerifier(unittest.TestCase):
    # keys used
    keys = {
        'key-for-bob': 'asdfasdfas-a-very-secret-signing-key',
        'other-secret-key': 'this is a different super-secret key; never use the same secret twice'
    }

    # create JWMs used in different tests
    # first JWM
    am = Macaroon(
        location='cool-picture-service.example.com',
        identifier='key-for-bob',
        key=keys['key-for-bob']
    )
    am.add_first_party_caveat('specific_claim', 'value')
    jwm = JWM(am)

    # second JWM
    am2 = Macaroon(
        location='http://mybank/',
        identifier='we used our other secret key',
        key=keys['other-secret-key']
    )
    am2.add_first_party_caveat('account', '3735928559')
    caveat_key = '4; guaranteed random by a fair toss of the dice'
    identifier = 'this was how we remind auth of key/pred'
    am2.add_third_party_caveat('http://auth.mybank/', caveat_key, identifier)

    dm = Macaroon(
        location='http://auth.mybank/',
        key=caveat_key,
        identifier=identifier
    )
    dm.add_first_party_caveat('time', '< 2015-01-01T0000')
    protected = am2.prepare_for_request(dm)

    jwm2 = JWM(authorizing_macaroon=am2, discharge_macaroons=[protected])

    def test_empty_verifier(self):
        """
        test Verifier without validators
        a Verifier without validators should validate any JWM
        """

        v = Verifier()
        verified = v.verify(TestVerifier.jwm, TestVerifier.keys['key-for-bob'])
        self.assertEqual(verified, True)

    def test_verifier(self):
        """
        Attaches a validator to a Verifier
        and tries to validate a JWM
        """
        v = Verifier()

        def specific_kvp_validator(value):
            return True

        v.add_validator("specific_claim", specific_kvp_validator)

        verified = v.verify(
            TestVerifier.jwm,
            TestVerifier.keys[TestVerifier.jwm.authorizing_macaroon.identifier]
        )
        self.assertEqual(verified, True)

    def test_verifier_with_discharge(self):
        """
        verify a jwm whose authorizing macaroon has a third party caveat
        """
        v = Verifier()
        verified = v.verify(TestVerifier.jwm2, TestVerifier.keys['other-secret-key'])
        self.assertEqual(verified, True)
