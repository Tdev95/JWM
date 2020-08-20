.. JWM documentation master file, created by
   sphinx-quickstart on Thu May 14 13:33:48 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to JWM's documentation!
===============================

JSON Web Macaroons (JWM) aims to be JWT (JSON Web Tokens) for macaroons. It is a bearer token that has a signature that can be verified and it contains claims, but because it is implemented using macaroons it allows for all the awesome features associated with macaroons. JWM is implemented on top of PyMacaroons.

.. toctree::
   :maxdepth: 4

   jwm
   verifier
   macaroon
   caveat
