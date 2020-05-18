# JSON Web Macaroons (JWM)

## What are JSON Web Macaroons?
JSON Web Macaroons (JWM) aims to be JWT (JSON Web Tokens) for macaroons. It is a bearer token in the sense that it has a signature that can be verified and it contains claims, but because it is implemented as a macaroon it allows for all the awesome features associated with macaroons. JWM is implemented on top of PyMacaroons.

The JWM format is defined as follows:

[header].[authorizing_macaroon].[discharge_macaroon]

The header and authorizing macaroon are mandatory, whereas discharge macaroons are optional.
The format stores all the necessary information to verify and validate a request.
Unlike regular macaroons, macaroons that are part of a JWM object have their caveats shaped as a key-value pair, similar to JWT claims.

example JWM:

## Usage

### Creating a JWM

```python
from jwm import JWM, Macaroon

am = Macaroon()
am.add_first_party_caveat()
jwm = JWM(authorizing_macaroon=am)
```
### Serialization

```python
am = Macaroon()
am.serialize()

jwm
```

### Binding Discharge Macaroons

JWM provides two methods of binding macaroons. One can either bind discharge macaroons to an authorizing macaroon before creating the JWM, or bind the discharge macaroon while attaching it to the JWM.

```python
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
jwm = JWM(Macaroon())
jwm.verify()
```

## Documentation

[WIP] Still figuring out sphinx, check the docs folder for progress so far

## References
- [Macaroon Paper] (http://research.google.com/pubs/pub41892.html)
- [pymacaroons] (https://github.com/ecordell/pymacaroons)
