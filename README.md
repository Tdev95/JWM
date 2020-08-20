# JSON Web Macaroons (JWM)

## What are JSON Web Macaroons?
JSON Web Macaroons (JWM) aims to be JWT (JSON Web Tokens) for macaroons. It is a bearer token that has a signature that can be verified and it contains claims, but because it is implemented as a macaroon it allows for all the awesome features associated with macaroons. JWM is implemented on top of PyMacaroons.

The JWM format is defined as follows:

[header].[payload]

where header is {'typ', 'jwm'} and payload is a JSON list of JSON macaroon objects where the first macaroon is the authorizing macaroon and the following macaroons are discharge macaroons.

The header and authorizing macaroon are mandatory, whereas discharge macaroons are optional.
The format stores all the necessary information to verify and validate a request.
Unlike regular macaroons, macaroons that are part of a JWM object have their caveats shaped as a key-value pair, similar to JWT claims.

## Installation

Because the repository is currently still private, installation through the python package index is not possible. Therefore temporarily installation has to be done manually using the wheel (.whl) file.
```
pip install JWM-1.0-py3-none-any.whl
```

## Usage

### Creating a JWM

```python
# example taken from pymacaroons
am = Macaroon(
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
```
### Serialization

```python
# serialize
am = Macaroon(location='example.com',
             identifier='use super_secret_key', key='super_secret_key')
jwm = JWM(am)
data = jwm.serialize()
# ... and deserialize
jwm2 = JWM.deserialize(data)
```

### Binding Discharge Macaroons

JWM provides two methods of binding macaroons. One can either bind discharge macaroons to an authorizing macaroon before creating the JWM, or bind the discharge macaroon while attaching it to the JWM.

```python
# the next examples are meant to illustrate the concepts
# for working examples, look at the test cases
am = Macaroon()
am.add_third_party_caveat()
dm = Macaroon()
am.prepare_for_request(dm)
jwm = JWM(am, [dm])
```

```python
am = Macaroon()
am.add_third_party_caveat()
jwm = JWM(authorizing_macaroon=am)
dm = Macaroon()
jwm.attach_and_bind_discharge_macaroon(dm)
```

### Verify signatures and Validate claims
```python
# use the key corresponding to the identifier of the authorizing macaroon
v = Verifier()
verified = v.verify(jwm, key)
```

## Documentation

[WIP] Documentation is present in the code and can be built using Sphinx, readthedocs.io is currently being considered as an option to host the documentation when this repository goes public. Check the docs folder for progress so far

## References
- [Macaroon Paper](http://research.google.com/pubs/pub41892.html)
- [pymacaroons](https://github.com/ecordell/pymacaroons)
