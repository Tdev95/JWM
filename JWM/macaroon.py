from pymacaroons import Macaroon as PyMacaroon
from pymacaroons.serializers import JsonSerializer
from base64 import b64encode, b64decode


class Macaroon:
    """
    JWM Macaroon class that wraps PyMacaroons.
    """

    def __init__(self, location, identifier=None, key=None, signature=None):
        self.pym = PyMacaroon(location=location, identifier=identifier,
                              key=key, signature=signature)

    # Caveats
    def add_first_party_caveat(self, key, value):
        """
        Add a first party caveat

        :param key: Caveat key
        :param value: Value corresponding to key
        """
        self.pym.add_first_party_caveat(f'{key}:{value}')

    def add_third_party_caveat(self, location, caveat_key, identifier):
        """
        Add a third party caveat

        :param location: location of third party
        :param caveat_key:
        :param identifier: identifier that tells third party what key to use
        """
        self.pym.add_third_party_caveat(location, caveat_key, identifier)

    # Binding
    def prepare_for_request(self, discharge_macaroon):
        """
        Binds a discharge macaroon to the macaroon's current signature

        :param discharge_macaroon: Discharge macaroon to binds
        :type discharge_macaroon: Macaroon
        """
        dm = self.pym.prepare_for_request(discharge_macaroon.pym)
        return Macaroon(location=dm.location, identifier=dm.identifier, signature=dm.signature)

    # Serialization
    def serialize(self):
        """
        Serializes the Macaroon

        :returns: serialized macaroon
        """
        return b64encode(str.encode(
            self.pym.serialize(serializer=JsonSerializer()))).decode()

    @classmethod
    def deserialize(cls, encoded_macaroon):
        """
        Deserializes a base 64 JSON encoded macaroon

        :returns: A new Macaroon object
        :rtype: Macaroon
        """
        m = PyMacaroon.deserialize(
            b64decode(str.encode(encoded_macaroon)).decode(), serializer=JsonSerializer())
        return Macaroon(location=m.location, identifier=m.identifier, signature=m.signature)

    # Properties
    """
    Inspect the state of the Macaroon (used for debugging)
    """

    def inspect(self):
        return self.pym.inspect()

    @property
    def signature(self):
        return self.pym.signature

    @property
    def identifier(self):
        return self.pym.identifier

    @property
    def caveats(self):
        return self.pym.caveats
