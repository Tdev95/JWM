from pymacaroons import Verifier as PyMacaroonsVerifier
from pymacaroons.caveat_delegates import FirstPartyCaveatVerifierDelegate
from pymacaroons.utils import convert_to_string
from JWM.exceptions import CriticalClaimException, UniqueClaimException
import json


class CustomFirstPartyCaveatVerifierDelegate(FirstPartyCaveatVerifierDelegate):
    """
    Custom FirstParyCaveatVerifierDelegate that hooks into PyMacaroons implementation
    Supports claims that are key-value pairs
    Optimizes PyMacaroons verifier by only checking for callbacks specific to the claim
    Provides info on valid claims to the verifier though _increment
    """

    def verify_first_party_caveat(self, verifier, caveat, signature):
        try:
            kvp = json.loads(convert_to_string(caveat.caveat_id))
        except json.decoder.JSONDecodeError:
            raise TypeError('claim is not a key value pair')

        if not isinstance(kvp, dict) or len(kvp.keys()) != 1:
            raise TypeError('claim is not a key value pair')

        # we use first key in kvp dict
        key = list(kvp.keys())[0]

        # If callbacks are registered to the key, the caveat is met iff
        # there at least one callback function that returns True
        # If no callbacks are registered to the key, the caveat is met
        caveat_met = False
        if key in verifier.callbacks:
            caveat_met = sum(callback(kvp[key]) for callback in verifier.callbacks[key])
            if caveat_met:
                verifier._increment(key)
        else:
            caveat_met = True

        return caveat_met


class CustomVerifier(PyMacaroonsVerifier):
    """
    Custom Verifier Class that supports critical and unique claims
    Hooks into PyMacaroon verifier implementation so can break easily
    """

    def __init__(self, critical_claims=None, unique_claims=None):
        super().__init__()

        # use my own delegate that tracks claim names
        self.first_party_caveat_verifier_delegate = CustomFirstPartyCaveatVerifierDelegate()
        self.callbacks = {}

        self.unique_claims = set()
        self.critical_claims = set()
        self.count = {}

        if critical_claims is not None:
            for claim in critical_claims:
                self.add_critical_claim(claim)

        if unique_claims is not None:
            for claim in unique_claims:
                self.add_unique_claim(claim)

    def add_critical_claim(self, claim):
        self.critical_claims.add(claim)

    def add_unique_claim(self, claim):
        self.unique_claims.add(claim)

    def verify(self, macaroon, key, discharge_macaroons=None):
        v = super().verify(macaroon, key, discharge_macaroons)

        if not self._critical_claims_satisfied():
            raise CriticalClaimException()
        if not self._unique_claims_satisfied():
            raise UniqueClaimException()
        self._reset_count()
        return v

    def add_validator(self, claim, callback):
        if claim in self.callbacks:
            self.callbacks[claim].append(callback)
        else:
            self.callbacks[claim] = [callback]

    def _critical_claims_satisfied(self):
        for claim in self.critical_claims:
            if claim not in self.count:
                return False
        return True

    def _unique_claims_satisfied(self):
        for claim in self.unique_claims:
            if claim in self.count and self.count[claim] != 1:
                return False
        return True

    def _reset_count(self):
        self.count = {}

    def _increment(self, claim):
        if claim in self.count:
            self.count[claim] += 1
        else:
            self.count[claim] = 0
