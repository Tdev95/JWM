# JSON Web Macaroons (JWM)

## What are JSON Web Macaroons?
JSON Web Macaroons (JWM) aims to be JWT (JSON Web Tokens) for macaroons. It is a bearer token in the sense that it has a signature that can be verified and it contains claims, but because it is implemented as a macaroon it allows for all the awesome features associated with macaroons. JWM is implemented on top of PyMacaroons.

The JWM format is defined as follows:

[header].[authorizing_macaroon].[discharge_macaroon]

The header and authorizing macaroon are mandatory, whereas discharge macaroons are optional.
The format stores all the necessary information to verify and validate a request.
Unlike regular macaroons, macaroons that are part of a JWM object have their caveats shaped as a key-value pair, similar to JWT claims.

## Usage

### Creating a JWM

```python
am = Macaroon()
am.add_first_party_caveat()
jwm = JWM(authorizing_macaroon=am)
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
# the next two examples are meant to illustrate the concept
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

### Verify signatures
```python
# use the key corresponding to the identifier of the authorizing macaroon
key = keys[am.identifier]
jwm.verify(key)
```

## Documentation

[WIP] Documentation is present in the code and can be built using Sphinx, readthedocs.io is currently being considered as an option to host the documentation when this repository goes public. Check the docs folder for progress so far

## References
- [Macaroon Paper](http://research.google.com/pubs/pub41892.html)
- [pymacaroons](https://github.com/ecordell/pymacaroons)
