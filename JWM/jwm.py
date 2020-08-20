from base64 import b64encode, b64decode
import json

from JWM.macaroon import Macaroon
from JWM.exceptions import DeserializationException


class JWM:
    """JSON Web Macaroons format"""

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
        header = b64encode(str.encode(self.header)).decode()
        header = header.split('=')[0]  # no padding

        payload = ''
        for macaroon in ([self.authorizing_macaroon] + self.discharge_macaroons):
            payload += macaroon.serialize() + ','
        payload = b64encode(('[' + payload[:-1] + ']').encode()).decode()
        payload = payload.split('=')[0]  # no padding
        # print(f'packet = {header}.{payload}')
        return f'{header}.{payload}'

    @classmethod
    def deserialize(cls, string):
        """
        Builds (Deserializes) a JWM from a string

        :param string: String to be deserialized
        :type string: string
        :returns: new JWM object
        :rtype: JWM

        :raises: DeserializationException
        """
        # decode JWM
        values = string.split('.')

        if len(values) != 2:
            raise DeserializationException("Unable to detect header and body")

        # process header
        header = json.loads(b64decode(cls._pad(values[0])).decode())

        if header["typ"] != "jwm":
            raise DeserializationException('Invalid header')

        # process payload
        payload = json.loads(b64decode(cls._pad(values[1])))
        if isinstance(payload, list) and len(payload) >= 1:
            authorizing_macaroon = Macaroon.deserialize(json.dumps(payload[0]))
            discharge_macaroons = []
            for macaroon in payload[1:]:
                discharge_macaroons.append(Macaroon.deserialize(json.dumps(macaroon)))
        else:
            raise DeserializationException('Invalid payload')

        # build and return JWM object
        return JWM(authorizing_macaroon=authorizing_macaroon,
                   discharge_macaroons=discharge_macaroons)

    @classmethod
    def _pad(cls, string):
        pd = len(string) % 4
        if pd == 3:
            return string + '='
        if pd == 2:
            return string + '=='
        if pd == 1:
            raise DeserializationException('Invalid base64 string')
        return string
