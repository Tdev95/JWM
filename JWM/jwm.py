from pymacaroons import Verifier
from base64 import b64encode, b64decode
import json

from JWM.macaroon import Macaroon
from JWM.exceptions import InvalidHeaderException, MissingBodyException


class JWM:
    """ JSON Web Macaroons format"""

    def __init__(self, authorizing_macaroon, discharge_macaroons=None):
        """
        :param authorizing_macaroon: An authorizing Macaroon
        :type authorizing_macaroon: Macaroon
        :param discharge_macaroons: A list of discharge Macaroons
        :type discharge_macaroons: list of Macaroons
        """
        self.header = '{"typ": "jwm"}'
        self.authorizing_macaroon = authorizing_macaroon
        self.discharge_macaroons = []
        if discharge_macaroons is not None:
            self.discharge_macaroons += discharge_macaroons

    def attach_discharge_macaroon(self, discharge_macaroon):
        """
        Attaches a discharge macaroon to the JWM

        :param discharge_macaroon: Discharge Macaroon to attach
        :type discharge_macaroon: Macaroon
        """
        self.discharge_macaroons.append(discharge_macaroon)

    def attach_and_bind_discharge_macaroon(self, discharge_macaroon):
        """
        Attaches a discharge macaroon to the JWM and binds it to the \
        signature of the authorizing macaroon

        :param discharge_macaroon: Discharge Macaroon to attach and bind
        :type discharge_macaroon: Macaroon
        """
        bm = self.authorizing_macaroon.prepare_for_request(discharge_macaroon)
        self.discharge_macaroons.append(bm)

    def serialize(self):
        """
        Serializes the JWM

        :returns: serialized JWM
        :rtype: string
        """
        ser = b64encode(str.encode(self.header)).decode()
        for macaroon in ([self.authorizing_macaroon] + self.discharge_macaroons):
            ser += f'.{macaroon.serialize()}'
        return ser

    @classmethod
    def deserialize(cls, string):
        """
        Builds (Deserializes) a JWM from a string

        :param string: String to be deserialized
        :type string: string
        :returns: new JWM object
        :rtype: JWM

        :raises: MissingBodyException, InvalidHeaderException
        """
        # decode JWM
        values = string.split('.')

        if len(values) < 2:
            raise MissingBodyException("No body found")

        # process header
        header = json.loads(b64decode(values[0]).decode())

        if header["typ"] != "jwm":
            raise InvalidHeaderException('No JWM header')

        # process body
        authorizing_macaroon = Macaroon.deserialize(values[1])
        discharge_macaroons = []
        for encoded_macaroon in values[2:]:
            discharge_macaroons.append(Macaroon.deserialize(encoded_macaroon))

        # build and return JWM object
        return JWM(authorizing_macaroon=authorizing_macaroon,
                   discharge_macaroons=discharge_macaroons)

    def verify(self, key, validate_predicates=False):
        """
        Verify the signature of a JWM using the discharge macaroons

        :param key: Key correspoding to the authorizing macaroon identifier
        :type key: string
        :param validate_predicates: Validate whether first party predicates are key value predicates
        :type validate_predicates: bool
        """

        # create Verifier
        v = Verifier()

        # validator that checks for key:value shape of predicates
        def kvp_validator(predicate):
            return len(predicate.split(':')) == 2

        # validator that only check hashes, ignore predicates
        def true_validator(predicate):
            return True

        if(validate_predicates):
            v.satisfy_general(kvp_validator)
        else:
            v.satisfy_general(true_validator)

        # get pymacaroon representation of discharge macaroons for verification
        discharge_macaroons = None
        if(self.discharge_macaroons):
            discharge_macaroons = []
            for dm in self.discharge_macaroons:
                discharge_macaroons.append(dm.pym)

        return v.verify(self.authorizing_macaroon.pym, key, discharge_macaroons=discharge_macaroons)
