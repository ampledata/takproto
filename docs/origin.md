

``takproto`` is a fork & complete re-write of @dB-SPL's 
`takprotobuf <https://github.com/dB-SPL/takprotobuf>`_.

Notable differences between the original ``takprotobuf`` & this module ``takproto``:

1. Rebuild proto files using `Protocol Buffers v21 <https://protobuf.dev/>`_.
2. Added support for encoding & decoding plain XML, Mesh & Stream TAK Protocol formats.
3. Remove dependency on ``untangle`` module, allowing compatibility with Python 3.6 
   through 3.10. Unfortunately many single-board computers (i.e. Raspberry Pi) still 
   ship with Python 3.6, this change allows ``takproto`` to run on those systems.
4. Added ``xmlDetails`` detection for supporting undefined Protobuf elements in XML.
5. > 90% test coverage with **new** Unit Tests.
6. PEP-8 & Black style, linting, documentation & formatting of code.

As much as possible @db-SPL's licensing terms were honored in this fork.
