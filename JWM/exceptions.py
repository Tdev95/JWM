class JWMException(Exception):
    pass


class DeserializationException(JWMException):
    pass


class VerificationFailure(Exception):
    """
    Verification of a Macaroon was attempted but failed for an unknown reason
    """


class CriticalClaimException(VerificationFailure):
    """
    The Verifier object did not find a critical claim in a Macaroon.
    """


class UniqueClaimException(VerificationFailure):
    """
    The Verifier object found a unique claim to be used more than once.
    """
