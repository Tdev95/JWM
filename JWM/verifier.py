from JWM.utils.custom_verifier import CustomVerifier


class Verifier():
    """
    Wrapper class for CustomVerifier that can
    Verify and Validate the contents of a JWM.

    Given a JWM, validate the contents of its claims
    and verify the Macaroon is correctly signed.

    Provides an easy-to-use interface that ensures
    the claims in the Macaroon are understood by the user.
    """

    def __init__(self, critical_claims=None, unique_claims=None):
        """
        Create a new Verifier object

        :param critical_claims: list of claim names that are required
        :param unique_claims: list of claim names that can occur at most once
        """
        self._custom_verifier = CustomVerifier()

    def add_critical_claim(self, claim):
        """
        Add a critical claim to the Verifier

        :param claim: critical claim to be added
        """
        self._custom_verifier.add_critical_claim(claim)

    def add_unique_claim(self, claim):
        """
        Add a unique claim to the Verifier

        :param claim: unique claim to be added
        """
        self._custom_verifier.add_unique_claim(claim)

    def verify(self, jwm, key):
        """
        Verify the signature and Validate the claims of a JWM.

        This will iterate through all claims in the given Macaroon
        and determine whether all claims a valid, given the current set of
        validators.

        If critical_claims are specified, then validation will fail if one
        or more claim in this list is not present in the token.

        If unique_claims are specified, then validation will fail if one
        or more claim in this list is present more than once in the token.

        This will throw an exception if the token is invalid or has an invalid signature
        and return True otherwise.

        :param jwm: JWM to be verified
        :param key: key corresponding to the JWM identifier
        """
        return self._custom_verifier.verify(jwm.authorizing_macaroon.to_pymacaroon(),
                                            key,
                                            [dm.to_pymacaroon() for dm in jwm.discharge_macaroons])

    def add_validator(self, claim, callback):
        """
        Add a validation callback for a given claim. When the given claim is
        encountered in a Macaroon, callback object will be called with the
        following signature::

        >>> callback(value)

        where value is the value of the Macaroon's claim converted to a python
        object.

        The validator should return True if the value is acceptable and False
        otherwise.

        :param claim: claim the callback should be attached to
        :param callback: validation callback to be called during validation
        """
        self._custom_verifier.add_validator(claim, callback)
