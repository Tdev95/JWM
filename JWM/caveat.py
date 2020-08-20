class Caveat():
    """
    Represents a caveat as found in Macaroons
    """

    def __init__(self, caveat_id, verification_key_id=None, location=None):
        self.caveat_id = caveat_id
        self.verification_key_id = verification_key_id
        self.location = location

    def is_first_party_caveat(self):
        """
        returns True if the caveat is a first party caveat
        return False otherwise
        """
        return (self.verification_key_id is None) and (self.location is None)

    def is_third_party_caveat(self):
        """
        returns True if the caveat is a third party caveat
        return False otherwise
        """
        return not self.is_first_party_caveat()

    def __repr__(self):
        repr = f"Caveat('{self.caveat_id}'"
        if self.verification_key_id is not None:
            repr += f', verification_key_id={self.verification_key_id}'
        if self.location is not None:
            repr += f", location='{self.location}'"
        repr += ')'
        return repr
